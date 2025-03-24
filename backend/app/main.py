from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api import api_router
from app.core.config import settings
from app.db import Base, engine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Fantasy Baseball API",
    description="API for Fantasy Baseball Decision Log",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Fantasy Baseball API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Fantasy Baseball API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Fantasy Baseball API")
