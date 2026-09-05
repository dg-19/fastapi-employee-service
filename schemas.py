from pydantic import BaseModel, ConfigDict, Field

class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    salary: int = Field(gt=0)
    age: int = Field(ge=10, le=65)

class EmployeeUpdate(BaseModel):
    name: str
    email: str
    department: str
    salary: int
    age: int

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: int
    age: int

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
