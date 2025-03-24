from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from app.db.models import Decision
from app.schemas.decision import DecisionCreate, DecisionUpdate, DecisionType


class DecisionRepository:
    """Repository for decision database operations"""

    def get_by_id(self, db: Session, decision_id: int) -> Optional[Decision]:
        """Get a decision by ID"""
        return db.query(Decision).filter(Decision.id == decision_id).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        decision_type: Optional[DecisionType] = None,
    ) -> List[Decision]:
        """Get all decisions with optional filtering"""
        query = db.query(Decision)

        # Apply filters if provided
        if decision_type:
            query = query.filter(Decision.type == decision_type)

        # Apply pagination
        return query.order_by(Decision.date.desc()).offset(skip).limit(limit).all()

    def count(
        self,
        db: Session,
        decision_type: Optional[DecisionType] = None,
    ) -> int:
        """Count decisions with optional filtering"""
        query = db.query(Decision)

        # Apply filters if provided
        if decision_type:
            query = query.filter(Decision.type == decision_type)

        return query.count()

    def create(self, db: Session, decision_create: DecisionCreate) -> Decision:
        """Create a new decision"""
        # Convert Pydantic model to dict, excluding None values
        decision_data = decision_create.model_dump(exclude_unset=True)

        # Create DB model instance
        db_decision = Decision(**decision_data)

        # Add to session and commit
        db.add(db_decision)
        db.commit()
        db.refresh(db_decision)

        return db_decision

    def update(
        self, db: Session, decision_id: int, decision_update: DecisionUpdate
    ) -> Optional[Decision]:
        """Update an existing decision"""
        # Get existing decision
        db_decision = self.get_by_id(db, decision_id)
        if not db_decision:
            return None

        # Convert Pydantic model to dict, excluding None values
        update_data = decision_update.model_dump(exclude_unset=True)

        # Update model instance
        for key, value in update_data.items():
            setattr(db_decision, key, value)

        # Commit changes
        db.commit()
        db.refresh(db_decision)

        return db_decision

    def delete(self, db: Session, decision_id: int) -> bool:
        """Delete a decision"""
        db_decision = self.get_by_id(db, decision_id)
        if not db_decision:
            return False

        db.delete(db_decision)
        db.commit()

        return True

    def get_by_date_range(
        self,
        db: Session,
        start_date: date,
        end_date: date,
        decision_type: Optional[DecisionType] = None,
    ) -> List[Decision]:
        """Get decisions within a date range"""
        query = db.query(Decision).filter(
            Decision.date >= start_date,
            Decision.date <= end_date,
        )

        # Apply type filter if provided
        if decision_type:
            query = query.filter(Decision.type == decision_type)

        return query.order_by(Decision.date.desc()).all()


# Create a singleton instance
decision_repository = DecisionRepository()
