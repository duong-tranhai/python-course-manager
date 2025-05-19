from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import role as crud
from ..database import SessionLocal
from ..schemas import role as schema

router = APIRouter(prefix="/roles", tags=["Roles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.RoleResponse)
def create_role(role: schema.RoleBase, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@router.get("/", response_model=list[schema.RoleResponse])
def read_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)

@router.get("/{role_id}", response_model=schema.RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    # role_id is automatically extracted from the URL and passed here
    role = crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/search", response_model=list[schema.RoleResponse])
def search_role(name: str, db: Session = Depends(get_db)):
    return crud.search_role(db, name)

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = crud.delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}
