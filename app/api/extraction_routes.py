from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.extractor_service import extract_text
import shutil
import os

router = APIRouter()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/extract-metrics")
# async def upload_and_extract(file: UploadFile = File(...)):
#     file_location = os.path.join(UPLOAD_DIR, file.filename)

#     try:
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         metrics_result = extract_text(file_location)

#         return JSONResponse(content={
#             "filename": file.filename,
#             "metrics": metrics_result
#         })
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if os.path.exists(file_location):
#             os.remove(file_location)

# @router.get("/")
# def root():
#     return {"message": "RemedyLabBackBone API is running."}
