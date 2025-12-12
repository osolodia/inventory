from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.db.database import SessionLocal
from app.models.models import Product
from app.schemas.schemas import ProductOut, ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    result = []
    for p in products:
        result.append(
            ProductOut(
                id=p.id,
                article=p.article,
                name=p.name,
                purchase_price=float(p.purchase_price) if p.purchase_price else None,
                sell_price=float(p.sell_price) if p.sell_price else None,
                is_active=bool(p.is_active),
                category_id=p.category_id,
                unit_id=p.unit_id
            )
        )
    return result

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductOut(
        id=p.id,
        article=p.article,
        name=p.name,
        purchase_price=float(p.purchase_price) if p.purchase_price else None,
        sell_price=float(p.sell_price) if p.sell_price else None,
        is_active=bool(p.is_active),
        category_id=p.category_id if p.category_id else None,
        unit_id=p.unit_id if p.unit_id else None
    )
    
"""@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return ProductOut(
        id=db_product.id,
        article=db_product.article,
        name=db_product.name,
        purchase_price=float(db_product.purchase_price) if db_product.purchase_price else None,
        sell_price=float(db_product.sell_price) if db_product.sell_price else None,
        is_active=bool(db_product.is_active),
        category=db_product.category.name if db_product.category else None,
        unit=db_product.unit.name if db_product.unit else None
    )"""

@router.post("/create")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        # Вызов хранимой процедуры
        sql = text("""
            CALL create_product(
                :article, :name, :purchase, :sell,
                :category, :unit
            )
        """)
        
        result = db.execute(sql, {
            'article': product.article,
            'name': product.name,
            'purchase_price': product.purchase_price,
            'sell_price': product.sell_price,
            'is_active': 1,
            'category_id': product.category_id,
            'unit_id': product.unit_id,
        })
        
        db.commit()
        
        # Получаем сообщение из процедуры
        message = result.fetchone()
        
        return {
            "success": True,
            "message": message[0] if message else "Продукт создан успешно"
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
    
@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    
    return ProductOut(
        id=db_product.id,
        article=db_product.article,
        name=db_product.name,
        purchase_price=float(db_product.purchase_price) if db_product.purchase_price else None,
        sell_price=float(db_product.sell_price) if db_product.sell_price else None,
        is_active=bool(db_product.is_active),
        category=db_product.category.name if db_product.category else None,
        unit=db_product.unit.name if db_product.unit else None
    )

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

@router.get("/{product_id}/quantity")
def get_product_quantity(
    product_id: int,
    zone_id: int,
    db: Session = Depends(get_db)
):
    try:
        sql = text("""
            SELECT get_inventory_quantity(:product_id, :zone_id) as quantity
            """)
            
        result = db.execute(sql, {
            'product_id': product_id,
            'zone_id': zone_id
        })
            
        quantity = result.scalar()
            
        return {
            "quantity": int(quantity) if quantity is not None else 0
        }
        
            
    except Exception as e:
        # Для отладки выведем полную ошибку
        import traceback
        error_details = traceback.format_exc()
        print(f"Ошибка в get_product_quantity: {error_details}")
        
        # Возвращаем 0 при ошибке, чтобы фронтенд не падал
        return {
            "quantity": 0,
            "error": str(e)
        }