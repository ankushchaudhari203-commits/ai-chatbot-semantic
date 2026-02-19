from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.routes.chat import router as chat_router
from app.routes.admin import router as admin_router
from app.db.database import init_db
from app.core.logger import setup_logger



# 1️⃣ Create FastAPI instance FIRST
app = FastAPI(title="Pizza Chatbot API")

# 2️⃣ Setup logger
logger = setup_logger()


# 3️⃣ Register startup event AFTER app is defined
@app.on_event("startup")
def startup_event():
    logger.info("Initializing database...")
    init_db()


# 4️⃣ Register routes
app.include_router(chat_router)
app.include_router(admin_router)


# 5️⃣ Health endpoints
@app.get("/")
def health_check():
    return {"status": "Pizza Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# 6️⃣ Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
