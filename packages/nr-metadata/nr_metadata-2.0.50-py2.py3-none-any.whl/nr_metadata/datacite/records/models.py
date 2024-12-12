from invenio_db import db
from invenio_records.models import RecordMetadataBase


class DataciteMetadata(db.Model, RecordMetadataBase):
    """Model for DataciteRecord metadata."""

    __tablename__ = "datacite_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
