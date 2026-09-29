from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

class CreateUser(BaseModel):
    name: str = Field(min_length = 5, max_length = 10)
    age: int = Field(le=10, ge=5)
    email: EmailStr
    hobbies: list[str] = Field(max_length=2, default_factory=list)

class UserResponse(BaseModel):
    name: str = Field(min_length=5, max_length=10)
    age: int = Field(le = 10, ge = 5)
    email: EmailStr
    hobbies: list[str] = Field(max_length= 2, default_factory=list)


app = FastAPI();

@app.post("/health", response_model = UserResponse, status_code = 201)
def root(body: CreateUser):
    return body
