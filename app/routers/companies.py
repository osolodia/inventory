from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.models import Company, CompanyType
from app.schemas.schemas import CompanyOut, CompanyCreate

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CompanyOut])
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    result = []
    for company in companies:
        result.append(
            CompanyOut(
                id=company.id,
                name=company.name,
                company_type=company.company_type.name if company.company_type else None
            )
        )
    return result

@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return CompanyOut(
        id=company.id,
        name=company.name,
        company_type=company.company_type.name if company.company_type else None
    )

@router.post("/", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return CompanyOut(
        id=db_company.id,
        name=db_company.name,
        company_type=db_company.company_type.name if db_company.company_type else None
    )

@router.put("/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_company.name = company.name
    db_company.company_type_id = company.company_type_id
    db.commit()
    db.refresh(db_company)
    
    return CompanyOut(
        id=db_company.id,
        name=db_company.name,
        company_type=db_company.company_type.name if db_company.company_type else None
    )

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"detail": "Company deleted"}
