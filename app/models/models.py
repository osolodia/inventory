from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(45), nullable=False)
    date = Column(Date, nullable=False)
    comment = Column(String(45))

    company_id = Column(Integer, ForeignKey("companies.id"))
    document_type_id = Column(Integer, ForeignKey("documenttypes.id"), nullable=False)
   
    company = relationship("Company", back_populates="documents")
    document_type = relationship("DocumentType", back_populates="documents")

class DocumentType(Base):
    __tablename__ = "documenttypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)

    documents = relationship("Document", back_populates="document_type")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)
    
    company_type_id = Column(Integer, ForeignKey("companytypes.id"), nullable=False)

    documents = relationship("Document", back_populates="company")
    
    company_type = relationship("CompanyType", back_populates="companies")

class CompanyType(Base):
    __tablename__ = "companytypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)

    companies = relationship("Company", back_populates="company_type")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    login = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)

    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)

    passport_series = Column(Integer, nullable=False)
    passport_number = Column(Integer, nullable=False)

    email = Column(String(45), nullable=True)
    number_phone = Column(String(45), nullable=True)
    date_birth = Column(String(45), nullable=True)

    position_id = Column(Integer, ForeignKey("positions.id"))
    subdivision_id = Column(Integer, ForeignKey("subdivisions.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(Integer, nullable=False)
    name = Column(String(45), nullable=False)
    purchase_price = Column(Numeric(20, 0))
    sell_price = Column(Numeric(20, 0))
    is_active = Column(Boolean, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    
    category = relationship("Category", back_populates="products")
    unit = relationship("Unit", back_populates="products")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    products = relationship("Product", back_populates="category")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    products = relationship("Product", back_populates="unit")

class StorageCondition(Base):
    __tablename__ = "storageconditions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    zones = relationship("StorageZone", back_populates="storage_condition")

class StorageZone(Base):
    __tablename__ = "storagezones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    comment = Column(String)
    storage_condition_id = Column(Integer, ForeignKey("storageconditions.id"), nullable=False)

    storage_condition = relationship("StorageCondition", back_populates="zones")