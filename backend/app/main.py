from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Поток API",
    description="Backend для приложения-дневника с ИИ-обработкой",
    version="0.1.0"
)

# Настройка CORS для кроссплатформенного клиента
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Поток API работает", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
