import asyncio
import logging
from uuid import uuid4
from datetime import datetime, timezone
from threedi_api_client.api import ThreediApi
from threedi_api_client.versions import V3BetaApi
from threedi_cmd.parser import ScenarioParser

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    organisation = "61f5a464c35044c19bc7d4b42d7f58cb"
    simulation_name = "run_" + uuid4().hex

    file_path = "./threedi_cmd/test_data/9_2D_FourCell_Rain/9_2D_FourCell_Rain_converted.yaml"
    client: V3BetaApi = ThreediApi(env_file="staging.env", version="v3-beta")

    context = {
        "organisation_uuid": organisation,
        "simulation_name": simulation_name,
        "datetime_now": datetime.now(timezone.utc).isoformat(),
    }

    parser = ScenarioParser("./" + file_path)
    scenario = parser.parse(client, "./", context=context)

    # Save simulation before using it in the websocket
    scenario.simulation.save()

    await scenario.execute()


if __name__ == "__main__":
    asyncio.run(main())
