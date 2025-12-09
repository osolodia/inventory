from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
                category=p.category.name if p.category else None,
                unit=p.unit.name if p.unit else None
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
        category=p.category.name if p.category else None,
        unit=p.unit.name if p.unit else None
    )

@router.post("/", response_model=ProductOut)
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
