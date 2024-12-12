from invenio_db import db
from invenio_records.models import RecordMetadataBase


class DocumentsMetadata(db.Model, RecordMetadataBase):
    """Model for DocumentsRecord metadata."""

    __tablename__ = "documents_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
