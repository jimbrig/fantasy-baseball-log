from datetime import date
from typing import List, Optional
from sqlalchemy import Column, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON

from .base import Base

# Decision types
DECISION_TYPES = ('draft', 'waiver', 'trade', 'lineup', 'general')


class Decision(Base):
    """Decision model for tracking fantasy baseball decisions"""

    # Basic fields
    title = Column(String(255), nullable=False)
    type = Column(Enum(*DECISION_TYPES), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    description = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    result = Column(Text, nullable=True)

    # Content in markdown format
    content = Column(Text, nullable=True)

    # JSON fields for additional data
    metadata = Column(JSON, nullable=True)
    categories = Column(JSON, nullable=True)  # List of categories affected
    players = Column(JSON, nullable=True)  # Players involved

    # Relationships
    # tags = relationship("Tag", secondary="decision_tags", back_populates="decisions")

    def __repr__(self):
        return f"<Decision {self.id}: {self.title}>"


# For future implementation
# class Tag(Base):
#     """Tags for categorizing decisions"""
#
#     name = Column(String(50), nullable=False, unique=True)
#     color = Column(String(7), nullable=True)  # Hex color code
#
#     # Relationships
#     decisions = relationship("Decision", secondary="decision_tags", back_populates="tags")
#
#     def __repr__(self):
#         return f"<Tag {self.id}: {self.name}>"
#
#
# class DecisionTag(Base):
#     """Association table for Decision-Tag many-to-many relationship"""
#
#     decision_id = Column(Integer, ForeignKey("decision.id"), primary_key=True)
#     tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
