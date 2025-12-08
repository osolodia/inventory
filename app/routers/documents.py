from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.models import Document
from app.schemas.schemas import DocumentOut, DocumentCreate, DocumentUpdate

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[DocumentOut])
def get_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    result = []
    for doc in docs:
        result.append(
            DocumentOut(
                id=doc.id,
                number=doc.number,
                date=doc.date.isoformat(),
                comment=doc.comment,
                company=doc.company.name if doc.company else None,
                document_type=doc.document_type.name if doc.document_type else None
            )
        )
    return result

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentOut(
        id=doc.id,
        number=doc.number,
        date=doc.date.isoformat(),
        comment=doc.comment,
        company=doc.company.name if doc.company else None,
        document_type=doc.document_type.name if doc.document_type else None
    )

@router.post("/", response_model=DocumentOut)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(**document.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    
    return DocumentOut(
        id=db_doc.id,
        number=db_doc.number,
        date=db_doc.date.isoformat(),
        comment=db_doc.comment,
        company=db_doc.company.name if db_doc.company else None,
        document_type=db_doc.document_type.name if db_doc.document_type else None
    )

@router.put("/{document_id}", response_model=DocumentOut)
def update_document(document_id: int, document: DocumentUpdate, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    for key, value in document.dict(exclude_unset=True).items():
        setattr(db_doc, key, value)
    
    db.commit()
    db.refresh(db_doc)
    
    return DocumentOut(
        id=db_doc.id,
        number=db_doc.number,
        date=db_doc.date.isoformat(),
        comment=db_doc.comment,
        company=db_doc.company.name if db_doc.company else None,
        document_type=db_doc.document_type.name if db_doc.document_type else None
    )

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(db_doc)
    db.commit()
    return {"detail": "Document deleted"}
