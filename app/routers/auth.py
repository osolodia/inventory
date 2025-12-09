from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from typing import Optional
import secrets
from app.db.database import SessionLocal
from app.models.models import Employee
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Конфигурация JWT
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Модели данных
class UserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    role_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки пользователя
def authenticate_user(db: Session, login: str, password: str):
    user = db.query(Employee).filter(Employee.login == login).first()
    if not user:
        return None
    if user.password != password:  # В реальном приложении используйте хеширование!
        return None
    return user

@router.post("/login", response_model=dict)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Ищем пользователя в базе данных
    user = authenticate_user(db, user_data.login, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "login": user.login,
            "name": f"{user.first_name} {user.last_name}",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role_id": user.role_id
        }
    }

security = HTTPBearer()

@router.get("/validate")
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials  # Получаем токен из заголовка Authorization
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Получаем пользователя из базы
    user = db.query(Employee).filter(Employee.login == login).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "id": user.id,
        "login": user.login,
        "name": f"{user.first_name} {user.last_name}",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role_id": user.role_id
    }