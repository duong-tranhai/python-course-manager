from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    role_id: int

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class RoleInUser(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class UserWithRoleResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RoleInUser

    model_config = {
        "from_attributes": True
    }

class SimpleUserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }
