from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.models import DocumentLine
from app.schemas.schemas import DocumentLineCreate

router = APIRouter(
    prefix="/documentlines",
    tags=["documentlines"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[DocumentLine])
def get_documentlines(document_id: int, db: Session = Depends(get_db)):
    docs = db.query(DocumentLine).filter(DocumentLine.document_id == document_id)
    result = []
    for doc in docs:
        result.append(
            DocumentLine(
                id=doc.id,
                quantity=doc.quantity,
                actual_quantity=doc.actual_quantity if doc.actual_quantity else None,
                product_id=doc.product_id,
                document_id=doc.document_id,
                storage_zone_sender_id=doc.storage_zone_sender_id if doc.storage_zone_sender_id else None,
                storage_zone_receiver_id=doc.storage_zone_receiver_id if doc.storage_zone_receiver_id else None
            )
        )
    return result

@router.post("/", response_model=DocumentLine)
def create_documentline(documentline: DocumentLineCreate, db: Session = Depends(get_db)):
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
