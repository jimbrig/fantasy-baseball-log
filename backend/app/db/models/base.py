from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all database models"""

    id: Any
    __name__: str

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Common timestamp fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs: Any) -> None:
        """Update model instance with provided values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
