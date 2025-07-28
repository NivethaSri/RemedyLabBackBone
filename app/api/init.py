from fastapi import APIRouter
from .auth_routes import router as auth_router
from .doctor_routes import router as doctor_router
from .patient_routes import router as patient_router
from .health_report_routes import router as health_report_router
from .recommendation_routes import router as recommendation_router
from .extraction_routes import router as extraction_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(doctor_router, prefix="/doctor", tags=["Doctor"])
api_router.include_router(patient_router, prefix="/patient", tags=["Patient"])
api_router.include_router(
    health_report_router, prefix="/health-report", tags=["HealthReport"]
)
api_router.include_router(
    recommendation_router, prefix="/ai/doctor", tags=["Recommendation"]
)
# api_router.include_router(extraction_router, prefix="/extract", tags=["Extraction"])
