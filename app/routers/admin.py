from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import admin as admin_crud
from app.database import SessionLocal
from app.helpers.audit import log_action
from app.models.user import User
from app.schemas.course import CourseAdminResponse, CourseDetailResponse, CourseUpdate
from app.schemas.role import RoleResponse, RoleBase, AssignRoleRequest
from app.schemas.system_log import SystemLogResponse
from app.schemas.user import UserWithRoleResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_admin(user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user

@router.get("/overview")
def get_admin_overview(
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_admin_dashboard_data(db)

@router.get("/users", response_model=list[UserWithRoleResponse])
def list_users(
    search: Optional[str] = Query(None),
    role_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_all_users(db, search=search, role_id=role_id)

@router.get("/courses", response_model=List[CourseAdminResponse])
def get_all_courses(
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_all_courses_with_stats(db)

@router.get("/courses/{course_id}/details", response_model=CourseDetailResponse)
def view_course_details(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_course_details(course_id, db)

@router.put("/courses/{course_id}", response_model=CourseAdminResponse)
def update_course(
    course_id: int,
    update_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.update_course(course_id, update_data, db)

@router.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(verify_admin)
):
    return admin_crud.delete_course(course_id, db)

@router.get("/roles", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db), current_admin: User = Depends(verify_admin)):
    return admin_crud.get_all_roles(db)

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleBase, db: Session = Depends(get_db), current_admin: User = Depends(verify_admin)):
    return admin_crud.create_role(role, db)

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleBase, db: Session = Depends(get_db), current_admin: User = Depends(verify_admin)):
    return admin_crud.update_role(role_id, role, db)

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_admin: User = Depends(verify_admin)):
    admin_crud.delete_role(role_id, db)
    return {"message": "Role deleted"}

@router.patch("/users/assign_role")
def assign_role(request: AssignRoleRequest, db: Session = Depends(get_db), current_admin: User = Depends(verify_admin)):
    admin_crud.assign_role_to_user(request.user_id, request.role_id, db)
    log_action(db, user_id=current_admin.id, action="role_assigned",
               detail=f"Assigned role ID {request.role_id} to user ID {request.user_id}")

    return {"message": "Role assigned"}

@router.get("/logs", response_model=list[SystemLogResponse])
def fetch_system_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin=Depends(verify_admin)):
    return admin_crud.get_system_logs(db, skip=skip, limit=limit)