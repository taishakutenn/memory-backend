from fastapi import FastAPI
import uvicorn

# Добавляем глобальные объекты
from api.main_routes import main_router  # Хендлеры для запросов к апи
from app.core.main_exception_handlers import register_exception_handlers  # Хендлеры ошибок

app = FastAPI()
app.include_router(main_router)
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
