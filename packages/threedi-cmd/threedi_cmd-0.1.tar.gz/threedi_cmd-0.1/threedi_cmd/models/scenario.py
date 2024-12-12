import asyncio
import logging
import time
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List

from threedi_api_client.openapi.exceptions import ApiException
from threedi_api_client.openapi.models import Schematisation, Simulation, ThreediModel
from threedi_api_client.threedi_api_client import ThreediApiClient
from threedi_api_client.versions import V3BetaApi

from threedi_cmd.console import console
from threedi_cmd.models.base import (
    BaseWrapper,
    ModelWrapper,
    SchematisationWrapper,
    SimulationTemplateWrapper,
    SimulationWrapper,
)
from threedi_cmd.websockets.clients import WebsocketClient
from threedi_cmd.websockets.settings import WebSocketSettings

logger = logging.getLogger(__name__)


class LoadScenarioError(Exception):
    pass


class FailedStep(Exception):
    pass


class ResolveError(Exception):
    pass


class Scenario:
    base_object: Any = None
    steps: Any = []

    # Internal instances administration
    _refs: Dict = None

    def __init__(
        self,
        data: Dict,
        threedi_api_client: ThreediApiClient,
        wrappers: List[BaseWrapper],
        websocket_settings: WebSocketSettings,
        base_path: Path = None,
        context: Dict = None,
    ):
        self._refs = {}
        self.wrappers = wrappers
        self.websocket_settings: WebSocketSettings = websocket_settings
        self.threedi_api_client: ThreediApiClient = threedi_api_client
        self._base_path = base_path
        self.context = context
        scenario = data.get("scenario")
        if not scenario:
            raise LoadScenarioError("Could not load scenario")
        steps_data = scenario.get("steps", [])
        self.create_base_object(scenario)
        self.steps = self.create_steps(steps_data)

    def create_base_object(self, scenario: Dict):
        pass

    @property
    def instance_kwargs(self):
        raise NotImplementedError("Implement in subclass")

    def cleanup(self):
        raise NotImplementedError("Implement in subclass")

    @property
    def websocket_endpoint_uri(self):
        raise NotImplementedError("Implement in subclass")

    @cached_property
    def websocket_client(self):
        return WebsocketClient(settings=self.websocket_settings)

    def create_steps(self, steps_data: List) -> List[ModelWrapper]:
        """:raises ResolveError if the scenario name can not be found in `steps_data`"""
        steps = []
        if steps_data is None:
            return steps

        for item in steps_data:
            key, data = tuple(item.items())[0]
            found = [x for x in self.wrappers if x.scenario_name == key]

            if not found:
                raise ResolveError(f"Cannot resolve {key} in self.metas")
            wrapper_class = found[0]

            wrapped_instance = wrapper_class(
                data,
                self.threedi_api_client,
                base_path=self._base_path,
                refs=self._refs,
                **self.instance_kwargs,
            )
            steps.append(wrapped_instance)
        return steps

    async def _run(self):
        from .waitfor import WaitForTimeout

        queue = self.websocket_client.queue
        try:
            # 'Execute' step items
            for i, item in enumerate(self.steps, start=1):
                await item.execute(queue)
        except ApiException as e:
            msg = f":collision: Failed step {i}: {item} due to APIException: {e.body}"
            raise FailedStep(msg)
        except WaitForTimeout as e:
            msg = f" :collision: Failed step {i}: {item} due to WaitForTimeout: {e}"
            raise FailedStep(msg)
        except Exception as e:
            msg = f" :collision: Failed step {i}: {item} due to: {e}"
            raise FailedStep(msg)
        finally:
            # Always try to cleanup the simulation
            self.cleanup()

        # Done, close the websocket connection
        try:
            await self.websocket_client.close()
        except Exception as e:
            console.print(e, style="error")

    async def execute(self):
        # Create base object (Simulation or Schematisation)
        if self.base_object.instance.id is None:
            self.base_object.save()

        listen_task = asyncio.create_task(
            self.websocket_client.listen(self.websocket_endpoint_uri)
        )
        try:
            await asyncio.wait_for(self.websocket_client.is_connected(), timeout=10)
        except asyncio.TimeoutError:
            console.print(
                "Could not establish WebSocket connection within 10 seconds",
                style="error",
            )
            listen_task.cancel()
            await asyncio.gather(listen_task)
            return
        run_task = asyncio.create_task(self._run())

        finished, _ = await asyncio.wait(
            [listen_task, run_task], return_when=asyncio.FIRST_EXCEPTION
        )

        for result in finished:
            if not result:
                continue
            if result.exception():
                raise result.exception()


class SimulationScenario(Scenario):
    base_object: Simulation = None

    @property
    def simulation(self):
        return self.base_object

    def cleanup(self):
        try:
            self.shutdown_simulation()
        except Exception:
            pass

    def _create_threedimodel(
        self,
        revision_id: int,
        schematisation_id: int,
        timeout: int = 1800,
        backoff: int = 10,
    ) -> ThreediModel:
        def get_make_simulation_template_task_id():
            tasks = self.threedi_api_client.threedimodels_tasks_list(threedimodel.id)
            for task in tasks.results:
                if task.name == "make_simulation_templates":
                    logger.info(f"Found make_simulation_template task {task.id}")
                    return task.id

        # Need to create new threedimodel
        threedimodel: ThreediModel = (
            self.threedi_api_client.schematisations_revisions_create_threedimodel(
                id=revision_id, schematisation_pk=schematisation_id, data={}
            )
        )
        logger.info(f"Wait for threedimodel {threedimodel.id} to become valid")

        # Wait for threedimodel simulation template tasks to complete
        simulation_template_task_id = None
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            time.sleep(backoff)
            if simulation_template_task_id is None:
                simulation_template_task_id = get_make_simulation_template_task_id()
            else:
                task = self.threedi_api_client.threedimodels_tasks_read(
                    simulation_template_task_id, threedimodel.id
                )
                if task.status == "success":
                    break
                if task.status == "failure":
                    raise Exception(f"Make Simulation Template task {task.id} failed")

        time.sleep(backoff)  # Give the threedimodel some time to set status to valid
        threedimodel = self.threedi_api_client.threedimodels_read(threedimodel.id)
        assert (
            threedimodel.is_valid
        ), f"Threedimodel is not valid within timeout {threedimodel}"

        return threedimodel

    def get_or_create_threedimodel(
        self, scenario: Dict, timeout: int = 1800, backoff: int = 10
    ) -> ThreediModel:
        """
        timeout: seconds to wait until threedimodel should be finished.
        """
        threedimodel_attr = self.context.get("threedimodel", None)

        if threedimodel_attr is None:
            threedimodel_attr = scenario.get("simulation", {}).get("threedimodel", None)

        if isinstance(threedimodel_attr, ThreediModel):
            return threedimodel_attr

        try:
            threedimodel_id = int(threedimodel_attr)
        except (ValueError, TypeError):
            threedimodel_id = None

        if threedimodel_id is not None:
            return self.threedi_api_client.threedimodels_read(id=threedimodel_id)

        if (
            isinstance(threedimodel_attr, dict)
            and "revision_id" in threedimodel_attr
            and "schematisation_id" in threedimodel_attr
        ):
            # Check if we can create it using schematisation_id and revision_id
            revision_id = threedimodel_attr.get("revision_id")
            schematisation_id = threedimodel_attr.get("schematisation_id")

            threedimodel_results = self.threedi_api_client.threedimodels_list(
                revision__schematisation__id=schematisation_id,
                disabled=False,
                is_valid=True,
            )
            if threedimodel_results.count > 0:
                threedimodel: ThreediModel = threedimodel_results.results[0]

                current_threedi_version = (
                    self.threedi_api_client.status_current_version().threedi_version
                )

                # Check if need to update
                auto_update = (
                    str(threedimodel_attr.get("auto_update", False)).lower() == "true"
                )
                if not auto_update or (
                    threedimodel.threedi_version == current_threedi_version
                ):
                    return threedimodel

                # Delete this threedimodel
                self.threedi_api_client.threedimodels_delete(id=threedimodel.id)

            # Cleanup any existing threedimodels that might have slipped through our nets
            threedimodel_results = self.threedi_api_client.threedimodels_list(
                revision__schematisation__id=schematisation_id,
                disabled=False,
            ).results
            threedimodel_results += self.threedi_api_client.threedimodels_list(
                revision__schematisation__id=schematisation_id,
                disabled=False,
                is_valid=False,
            ).results
            for threedimodel in threedimodel_results:
                self.threedi_api_client.threedimodels_delete(id=threedimodel.id)

            threedimodel = self._create_threedimodel(
                revision_id, schematisation_id, timeout=timeout, backoff=backoff
            )

        return threedimodel

    def create_base_object(self, scenario: Dict):
        simulation_data = scenario.get("simulation")

        if "tags" not in simulation_data:
            simulation_data["tags"] = ["automatic-test"]
        elif "automatic-test" not in simulation_data.get("tags", []):
            simulation_data["tags"].append("automatic-test")

        threedimodel = self.get_or_create_threedimodel(scenario)

        assert (
            threedimodel is not None
        ), f"Could not retrieve threedimodel for {scenario} {self.context}"

        threedimodel: ThreediModel

        if threedimodel.schematisation_id is not None:
            # New threedimodel, use simulation template...
            self.threedi_api_client: V3BetaApi
            templates = self.threedi_api_client.simulation_templates_list(
                simulation__threedimodel__id=threedimodel.id
            )

            if templates.count == 0:
                raise Exception(f"No templates found for threedimodel: {threedimodel.id}")

            # Inject into simulation_data & pop threedimodel
            simulation_data.pop("threedimodel", None)
            simulation_data["template"] = templates.results[0].id

            self.base_object = SimulationTemplateWrapper(
                simulation_data, self.threedi_api_client
            )
            self.base_object.save()
        else:
            self.base_object = SimulationWrapper(simulation_data, self.threedi_api_client)

    @property
    def websocket_endpoint_uri(self):
        return f"simulations/{self.simulation.instance.id}/?scenario_test_framework=true"

    @property
    def instance_kwargs(self):
        return {"simulation": self.simulation.instance}

    def shutdown_simulation(self):
        console.print("• Requesting simulation shutdown")
        api: V3BetaApi = self.threedi_api_client

        api.simulations_actions_create(self.simulation.instance.id, {"name": "shutdown"})


class SchematisationScenario(Scenario):
    base_object: Schematisation = None

    def cleanup(self):
        pass

    @property
    def schematisation(self):
        return self.base_object

    def create_base_object(self, scenario: Dict):
        schematisation_data = scenario.get("schematisation")
        self.base_object = SchematisationWrapper(
            schematisation_data, self.threedi_api_client
        )

    @property
    def websocket_endpoint_uri(self):
        return (
            f"schematisations/{self.schematisation.instance.id}/"
            + "?scenario_test_framework=true"
        )

    @property
    def instance_kwargs(self):
        return {"schematisation": self.schematisation.instance}
