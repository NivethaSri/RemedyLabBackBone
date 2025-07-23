from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    userID: str
    userType: str
    email: str
    message: str
