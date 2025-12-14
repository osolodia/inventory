# app/routers/reference.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Role as RoleModel, Position as PositionModel, Subdivision as SubdivisionModel
from app.schemas.schemas import Role as RoleSchema, Position as PositionSchema, Subdivision as SubdivisionSchema
from app.db.database import SessionLocal

router = APIRouter(prefix="", tags=["reference"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/roles", response_model=list[RoleSchema])
def read_roles(db: Session = Depends(get_db)):
    return db.query(RoleModel).all()

@router.get("/positions", response_model=list[PositionSchema])
def read_positions(db: Session = Depends(get_db)):
    return db.query(PositionModel).all()

@router.get("/subdivisions", response_model=list[SubdivisionSchema])
def read_subdivisions(db: Session = Depends(get_db)):
    return db.query(SubdivisionModel).all()

