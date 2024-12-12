from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from nr_metadata.datacite.records.dumpers.dumper import DataciteDumper
from nr_metadata.datacite.records.models import DataciteMetadata


class DataciteIdProvider(RecordIdProviderV2):
    pid_type = "dtct"


class DataciteRecord(InvenioRecord):

    model_cls = DataciteMetadata

    schema = ConstantField("$schema", "local://datacite-1.0.0.json")

    index = IndexField(
        "datacite-datacite-1.0.0",
    )

    pid = PIDField(
        provider=DataciteIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = DataciteDumper()
