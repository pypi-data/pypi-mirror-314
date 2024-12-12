from invenio_db import db
from invenio_records.models import RecordMetadataBase


class DataMetadata(db.Model, RecordMetadataBase):
    """Model for DataRecord metadata."""

    __tablename__ = "data_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
