from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.models import Employee
from app.schemas.schemas import EmployeeOut, EmployeeUpdate, EmployeeCreate

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    result = []
    for employee in employees:
        result.append(
            EmployeeOut(
                id=employee.id,
                login=employee.login,
                password=employee.password,
                first_name=employee.first_name,
                last_name=employee.last_name,
                role_id=employee.role_id
            )
        )
    return result

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return EmployeeOut(
        id=employee.id,
        login=employee.login,
        password=employee.password,
        first_name=employee.first_name,
        last_name=employee.last_name,
        role_id=employee.role_id
    )

@router.post("/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return EmployeeOut(
        id=employee.id,
        login=employee.login,
        password=employee.password,
        first_name=employee.first_name,
        last_name=employee.last_name,
        role_id=employee.role_id
    )
"""
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
"""