from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
