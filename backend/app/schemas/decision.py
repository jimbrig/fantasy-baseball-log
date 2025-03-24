from datetime import date
from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field

# Decision type literal
DecisionType = Literal["draft", "waiver", "trade", "lineup", "general"]


class DecisionBase(BaseModel):
    """Base schema for decision data"""
    title: str
    type: DecisionType
    date: date = Field(default_factory=date.today)
    description: Optional[str] = None
    impact: Optional[str] = None
    result: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[List[str]] = None
    players: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class DecisionCreate(DecisionBase):
    """Schema for creating a new decision"""
    pass


class DecisionUpdate(BaseModel):
    """Schema for updating an existing decision"""
    title: Optional[str] = None
    type: Optional[DecisionType] = None
    date: Optional[date] = None
    description: Optional[str] = None
    impact: Optional[str] = None
    result: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[List[str]] = None
    players: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class DecisionInDB(DecisionBase):
    """Schema for decision as stored in the database"""
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class Decision(DecisionInDB):
    """Schema for decision response"""
    pass


class DecisionList(BaseModel):
    """Schema for list of decisions"""
    items: List[Decision]
    total: int
