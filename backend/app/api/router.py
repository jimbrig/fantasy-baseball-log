from fastapi import APIRouter

from app.core.config import settings
from app.api.endpoints import decisions_router

# Create main API router
api_router = APIRouter(prefix=settings.API_V1_STR)

# Include all endpoint routers
api_router.include_router(decisions_router, prefix="/decisions", tags=["decisions"])

# Add more routers here as needed
# api_router.include_router(yahoo_router, prefix="/yahoo", tags=["yahoo"])
