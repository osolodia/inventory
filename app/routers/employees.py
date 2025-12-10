from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
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
                passposrt_series = employee.passport_series,
                passport_number = employee.passport_number,
                email = employee.email,
                number_phone = employee.number_phone,
                date_birth = employee.date_birth,
                position_id=employee.position_id,
                subdivision_id=employee.subdivision_id,
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
        passposrt_series = employee.passport_series,
        passport_number = employee.passport_number,
        email = employee.email,
        number_phone = employee.number_phone,
        date_birth = employee.date_birth,
        position_id=employee.position_id,
        subdivision_id=employee.subdivision_id,
        role_id=employee.role_id
    )

@router.post("/create")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        # Вызов хранимой процедуры
        sql = text("""
            CALL create_employee(
                :login, :password, :first_name, :last_name,
                :passport_series, :passport_number, :email, :number_phone,
                :date_birth, :position_id, :subdivision_id, :role_id
            )
        """)
        
        result = db.execute(sql, {
            'login': employee.login,
            'password': employee.password,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'passport_series': employee.passport_series,
            'passport_number': employee.passport_number,
            'email': employee.email if employee.email else None,
            'number_phone': employee.number_phone if employee.number_phone else None,
            'date_birth': employee.date_birth if employee.date_birth else None,
            'position_id': employee.position_id,
            'subdivision_id': employee.subdivision_id,
            'role_id': employee.role_id
        })
        
        db.commit()
        
        # Получаем сообщение из процедуры
        message = result.fetchone()
        
        return {
            "success": True,
            "message": message[0] if message else "Сотрудник создан успешно"
        }
        
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        
        import traceback
        error_details = traceback.format_exc()
        print(f"Полная ошибка: {error_details}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка создания сотрудника: {str(e)}"
        )
    
        """# Обработка ошибок из процедуры
        if "Сотрудник с таким логином уже существует" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        
        raise HTTPException(status_code=500, detail=f"Ошибка создания сотрудника: {error_msg}")"""
