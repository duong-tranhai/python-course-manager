from sqlalchemy.orm import Session

from ..models.role import Role
from ..schemas import role as schema


def create_role(db: Session, role: schema.RoleCreate):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
    return role

def search_role(db: Session, name: str):
    return db.query(Role).filter(Role.name.ilike(f"%{name}%")).all()
