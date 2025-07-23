from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def some_function():
    return {"status": "ok"}
