from fastapi import FastAPI
from app.routers import products, documents, companies, companytypes, documenttypes, categories, units

app = FastAPI(title="Inventory API")

# Подключаем роутеры
app.include_router(products.router)
app.include_router(documents.router)
app.include_router(companies.router)
app.include_router(companytypes.router)
app.include_router(documenttypes.router)
app.include_router(categories.router)
app.include_router(units.router)

# Корневой эндпоинт (опционально)
@app.get("/")
def root():
    return {"message": "Inventory API is running"}
