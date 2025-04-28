from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    role_id: int

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class RoleInUser(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserWithRoleResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RoleInUser

    class Config:
        orm_mode = True

class SimpleUserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
