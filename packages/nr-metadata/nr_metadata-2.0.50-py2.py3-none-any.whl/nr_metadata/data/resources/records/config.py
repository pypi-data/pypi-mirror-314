import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from nr_metadata.data.resources.records.ui import DataUIJSONSerializer


class DataResourceConfig(RecordResourceConfig):
    """DataRecord resource config."""

    blueprint_name = "data"
    url_prefix = "/nr-metadata-data/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_metadata.data.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DataUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
