from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserData(BaseModel):
    id: str
    name: Optional[str] = None
    email: str
    role: str  # doctor or patient
    specialization: Optional[str] = None
    experience: Optional[str] = None
    contactNumber: Optional[str] = None
    gender: Optional[str] = None  # ✅ Make Optional
    age : str   # ✅ NEW FIELD


class LoginResponse(BaseModel):
    status: str
    message: str
    data: UserData
    timestamp: str

class LoginRequest(BaseModel):
    email: str
    password: str




