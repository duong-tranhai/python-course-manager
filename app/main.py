import subprocess

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth import get_current_user
from app.routers import user as user_router, role as role_router, course as course_router, auth as auth_router, \
    lesson as lesson_router, quiz as quiz_router, admin as admin_router,  attendance as attendance_router
from app.scheduler import start_scheduler

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Unauthorized",
                "message": "You must include a valid Authorization token to access this resource."
            }
        )
    return await request.app.default_exception_handler(request, exc)


# You can add additional URLs to this list, for example, the frontend's production domain, or other frontends.
allowed_origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS
    allow_headers=["*"],  # includes Authorization
)

@app.on_event("startup")
def on_startup():
    subprocess.run(["alembic", "upgrade", "head"])
    start_scheduler()

app.include_router(user_router.router,dependencies=[Depends(get_current_user)])
app.include_router(role_router.router, dependencies=[Depends(get_current_user)])
app.include_router(course_router.router, dependencies=[Depends(get_current_user)])
app.include_router(lesson_router.router, dependencies=[Depends(get_current_user)])
app.include_router(quiz_router.router, dependencies=[Depends(get_current_user)])
app.include_router(admin_router.router, dependencies=[Depends(get_current_user)])
app.include_router(attendance_router.router, dependencies=[Depends(get_current_user)])
app.include_router(auth_router.router)
