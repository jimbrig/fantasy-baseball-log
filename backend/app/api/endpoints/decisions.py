from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.repositories import decision_repository
from app.schemas.decision import (
    Decision,
    DecisionCreate,
    DecisionList,
    DecisionUpdate,
    DecisionType,
)

router = APIRouter()


@router.get("/{decision_id}", response_model=Decision)
async def get_decision(
    decision_id: int = Path(..., title="The ID of the decision to get"),
    db: Session = Depends(get_db),
):
    """Get a decision by ID"""
    decision = decision_repository.get_by_id(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.get("/", response_model=DecisionList)
async def list_decisions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    decision_type: Optional[DecisionType] = Query(None),
    db: Session = Depends(get_db),
):
    """List decisions with optional filtering"""
    decisions = decision_repository.get_all(
        db, skip=skip, limit=limit, decision_type=decision_type
    )
    total = decision_repository.count(db, decision_type=decision_type)
    return {"items": decisions, "total": total}


@router.post("/", response_model=Decision, status_code=201)
async def create_decision(
    decision_create: DecisionCreate,
    db: Session = Depends(get_db),
):
    """Create a new decision"""
    return decision_repository.create(db, decision_create)


@router.put("/{decision_id}", response_model=Decision)
async def update_decision(
    decision_update: DecisionUpdate,
    decision_id: int = Path(..., title="The ID of the decision to update"),
    db: Session = Depends(get_db),
):
    """Update an existing decision"""
    updated_decision = decision_repository.update(db, decision_id, decision_update)
    if not updated_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return updated_decision


@router.delete("/{decision_id}", status_code=204)
async def delete_decision(
    decision_id: int = Path(..., title="The ID of the decision to delete"),
    db: Session = Depends(get_db),
):
    """Delete a decision"""
    success = decision_repository.delete(db, decision_id)
    if not success:
        raise HTTPException(status_code=404, detail="Decision not found")
    return None
