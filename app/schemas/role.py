from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

class RoleResponse(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class AssignRoleRequest(RoleBase):
    user_id: int
    role_id: int