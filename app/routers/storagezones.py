from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.models import StorageZone, StorageCondition
from app.schemas.schemas import StorageZoneOut, StorageZoneCreate

router = APIRouter(
    prefix="/storagezones",
    tags=["storagezones"]
)

# Получить все зоны хранения
@router.get("/", response_model=List[StorageZoneOut])
def read_storage_zones(db: Session = Depends(get_db)):
    zones = db.query(StorageZone).all()
    result = []
    for z in zones:
        result.append(StorageZoneOut(
            id=z.id,
            name=z.name,
            comment=z.comment,
            storage_condition=z.storage_condition.name if z.storage_condition else None
        ))
    return result

# Создать новую зону хранения
@router.post("/", response_model=StorageZoneOut)
def create_storage_zone(data: StorageZoneCreate, db: Session = Depends(get_db)):
    condition = db.query(StorageCondition).filter(StorageCondition.id == data.storage_condition_id).first()
    if not condition:
        raise HTTPException(status_code=404, detail="StorageCondition не найден")
    
    zone = StorageZone(
        name=data.name,
        comment=data.comment,
        storage_condition_id=data.storage_condition_id
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return StorageZoneOut(
        id=zone.id,
        name=zone.name,
        comment=zone.comment,
        storage_condition=condition.name
    )

# Обновить зону хранения
@router.put("/{zone_id}", response_model=StorageZoneOut)
def update_storage_zone(zone_id: int, data: StorageZoneCreate, db: Session = Depends(get_db)):
    zone = db.query(StorageZone).filter(StorageZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="StorageZone не найден")
    
    condition = db.query(StorageCondition).filter(StorageCondition.id == data.storage_condition_id).first()
    if not condition:
        raise HTTPException(status_code=404, detail="StorageCondition не найден")

    zone.name = data.name
    zone.comment = data.comment
    zone.storage_condition_id = data.storage_condition_id

    db.commit()
    db.refresh(zone)

    return StorageZoneOut(
        id=zone.id,
        name=zone.name,
        comment=zone.comment,
        storage_condition=condition.name
    )

# Удалить зону хранения
@router.delete("/{zone_id}")
def delete_storage_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(StorageZone).filter(StorageZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="StorageZone не найден")
    db.delete(zone)
    db.commit()
    return {"detail": "Удалено"}
