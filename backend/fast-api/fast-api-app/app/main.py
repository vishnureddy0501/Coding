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

class TaskCreate(BaseModel):
    title: str = Field(description="enter title", min_length=2, max_length=5)
    completed: bool = False

try:
    data = {"title": "Study123"}
    task = TaskCreate(**data)
    result = {"id": 1, **task.model_dump()}
    print(data, task, result);
    print(type(data), type(task), type(result));
except:
    print("some error occured")