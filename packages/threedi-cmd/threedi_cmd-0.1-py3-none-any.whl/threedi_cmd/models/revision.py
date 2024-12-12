from pathlib import Path
from typing import Dict
from .base import SchematisationChildWrapper, RevisionChildWrapper
from threedi_api_client.openapi.api import V3BetaApi
from threedi_api_client.openapi.models import (
    SchematisationRevision,
    SqliteFileUpload,
    RevisionRaster,
    Commit,
    Upload,
    Sqlite,
)
from .waitfor import WaitForModel


class RevisionWrapper(SchematisationChildWrapper):
    model = SchematisationRevision
    api_path: str = "revisions"
    scenario_name = "revision"


class WaitForSqliteUploadWrapper(WaitForModel):
    model = Sqlite
    scenario_name = "waitforsqliteupload"
    websocket_event_type = "event"

    def matches(self, websocket_instance):
        if (
            isinstance(websocket_instance, self.model)
            and websocket_instance.revision_id == self.instance.revision_id
        ):
            return websocket_instance.file["state"] == "uploaded"


class WaitForRasterUploadWrapper(WaitForModel):
    model = RevisionRaster
    scenario_name = "waitforrevisionrastereupload"
    websocket_event_type = "event"

    def matches(self, websocket_instance):
        if (
            isinstance(websocket_instance, self.model)
            and websocket_instance.id == self.instance.id
        ):
            return websocket_instance.file["state"] == "uploaded"


class SqliteWrapper(RevisionChildWrapper):
    model = SqliteFileUpload
    api_path: str = "revisions_sqlite_upload"
    scenario_name = "sqlite"
    filepath: Path = None

    def resolve_func_name(self, suffix: str):
        if suffix == "_create":
            suffix = ""
        return super().resolve_func_name(suffix)

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        wait_for_upload = WaitForSqliteUploadWrapper(
            data={"revision_id": self.revision.id},
            api_client=self._api_client,
        )
        return [wait_for_upload]


class RasterWrapper(RevisionChildWrapper):
    model = RevisionRaster
    api_path: str = "revisions_rasters"
    scenario_name = "raster"
    filepath: Path = None
    filename: str = None

    def initialize_instance(self, data: Dict):
        self.filename = data.pop("filename")
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    def save(self):
        super().save(upload_file=False)

        # Use raster to create raster upload
        api_client: V3BetaApi = self._api_client
        upload: Upload = Upload(filename=self.filename)
        upload = api_client.schematisations_revisions_rasters_upload(
            self.instance.id, self.revision.id, self.schematisation.id, upload
        )

        # Upload raster
        self._upload_file(upload.put_url)

    @property
    def extra_steps(self):
        wait_for_upload = WaitForRasterUploadWrapper(
            data=self.instance.to_dict(),
            api_client=self._api_client,
        )
        return [wait_for_upload]


class CommitWrapper(RevisionChildWrapper):
    model = Commit
    api_path: str = "revisions_commit"
    scenario_name = "commit"

    def resolve_func_name(self, suffix: str):
        if suffix == "_create":
            suffix = ""
        return super().resolve_func_name(suffix)


WRAPPERS = [
    RevisionWrapper,
    SqliteWrapper,
    RasterWrapper,
    CommitWrapper,
    WaitForSqliteUploadWrapper,
    WaitForRasterUploadWrapper,
]
