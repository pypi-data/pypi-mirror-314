from invenio_db import db
from invenio_records.models import RecordMetadataBase


class CommonMetadata(db.Model, RecordMetadataBase):
    """Model for CommonRecord metadata."""

    __tablename__ = "common_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
