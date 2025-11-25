from fastapi import APIRouter

from src.routers.v1.contacts.router import router as contacts_router
from src.routers.v1.leads.router import router as leads_router
from src.routers.v1.operators.router import router as operators_router
from src.routers.v1.sources.router import router as sources_router
from src.routers.v1.stats.router import router as stats_router

router = APIRouter(prefix="/api/v1")

router.include_router(contacts_router)
router.include_router(leads_router)
router.include_router(operators_router)
router.include_router(sources_router)
router.include_router(stats_router)