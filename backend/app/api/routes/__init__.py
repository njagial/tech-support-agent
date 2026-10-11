# API Routes Package
from fastapi import APIRouter

from app.api.routes import agent

api_router = APIRouter()

api_router.include_router(agent.router)
