from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.models import CompanyType
from app.schemas.schemas import CompanyTypeOut, CompanyTypeCreate

router = APIRouter(
    prefix="/companytypes",
    tags=["companytypes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CompanyTypeOut])
def get_company_types(db: Session = Depends(get_db)):
    return db.query(CompanyType).all()

@router.get("/{company_type_id}", response_model=CompanyTypeOut)
def get_company_type(company_type_id: int, db: Session = Depends(get_db)):
    company_type = db.query(CompanyType).filter(CompanyType.id == company_type_id).first()
    if not company_type:
        raise HTTPException(status_code=404, detail="CompanyType not found")
    return company_type

@router.post("/", response_model=CompanyTypeOut)
def create_company_type(company_type: CompanyTypeCreate, db: Session = Depends(get_db)):
    db_company_type = CompanyType(**company_type.dict())
    db.add(db_company_type)
    db.commit()
    db.refresh(db_company_type)
    return db_company_type

@router.put("/{company_type_id}", response_model=CompanyTypeOut)
def update_company_type(company_type_id: int, company_type: CompanyTypeCreate, db: Session = Depends(get_db)):
    db_company_type = db.query(CompanyType).filter(CompanyType.id == company_type_id).first()
    if not db_company_type:
        raise HTTPException(status_code=404, detail="CompanyType not found")
    
    db_company_type.name = company_type.name
    db.commit()
    db.refresh(db_company_type)
    return db_company_type

@router.delete("/{company_type_id}")
def delete_company_type(company_type_id: int, db: Session = Depends(get_db)):
    db_company_type = db.query(CompanyType).filter(CompanyType.id == company_type_id).first()
    if not db_company_type:
        raise HTTPException(status_code=404, detail="CompanyType not found")
    
    db.delete(db_company_type)
    db.commit()
    return {"detail": "CompanyType deleted"}
