from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import StorageCondition
from app.schemas.schemas import StorageConditionOut, StorageConditionCreate

router = APIRouter(
    prefix="/storageconditions",
    tags=["storageconditions"]
)

# Получить все условия хранения
@router.get("/", response_model=List[StorageConditionOut])
def read_storage_conditions(db: Session = Depends(get_db)):
    return db.query(StorageCondition).all()

# Создать новое условие хранения
@router.post("/", response_model=StorageConditionOut)
def create_storage_condition(data: StorageConditionCreate, db: Session = Depends(get_db)):
    condition = StorageCondition(name=data.name)
    db.add(condition)
    db.commit()
    db.refresh(condition)
    return condition

# Обновить условие хранения
@router.put("/{condition_id}", response_model=StorageConditionOut)
def update_storage_condition(condition_id: int, data: StorageConditionCreate, db: Session = Depends(get_db)):
    condition = db.query(StorageCondition).filter(StorageCondition.id == condition_id).first()
    if not condition:
        raise HTTPException(status_code=404, detail="StorageCondition не найден")
    condition.name = data.name
    db.commit()
    db.refresh(condition)
    return condition

# Удалить условие хранения
@router.delete("/{condition_id}")
def delete_storage_condition(condition_id: int, db: Session = Depends(get_db)):
    condition = db.query(StorageCondition).filter(StorageCondition.id == condition_id).first()
    if not condition:
        raise HTTPException(status_code=404, detail="StorageCondition не найден")
    db.delete(condition)
    db.commit()
    return {"detail": "Удалено"}
