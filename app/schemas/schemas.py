from pydantic import BaseModel
from typing import Optional, List

# CompanyType
class CompanyTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CompanyTypeCreate(BaseModel):
    name: str

# Company
class CompanyOut(BaseModel):
    id: int
    name: str
    company_type: Optional[str] = None 

    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    name: str
    company_type_id: int

# DocumentType
class DocumentTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class DocumentTypeCreate(BaseModel):
    name: str

# Document
class DocumentOut(BaseModel):
    id: int
    number: str
    date: str  
    comment: Optional[str] = None
    company: Optional[str] = None  
    document_type: Optional[str] = None  

    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    number: str
    date: str 
    comment: Optional[str] = None
    company_id: Optional[int] = None
    document_type_id: int

class DocumentUpdate(BaseModel):
    number: Optional[str] = None
    date: Optional[str] = None
    comment: Optional[str] = None
    company_id: Optional[int] = None
    document_type_id: Optional[int] = None

# Category 
class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str

# Unit
class UnitOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UnitCreate(BaseModel):
    name: str

# Product 
class ProductOut(BaseModel):
    id: int
    article: int
    name: str
    purchase_price: Optional[float] = None
    sell_price: Optional[float] = None
    is_active: Optional[bool] 
    category: Optional[str] = None  
    unit: Optional[str] = None  

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    article: int
    name: str
    purchase_price: Optional[float] = None
    sell_price: Optional[float] = None
    is_active: bool = True
    category_id: Optional[int] = None
    unit_id: Optional[int] = None

class ProductUpdate(BaseModel):
    article: Optional[int] = None
    name: Optional[str] = None
    purchase_price: Optional[float] = None
    sell_price: Optional[float] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    unit_id: Optional[int] = None