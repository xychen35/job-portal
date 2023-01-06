from fastapi import APIRouter

from webapps.jobs import route_jobs
from webapps.users import route_users
from webapps.auth import route_login

webapp_router = APIRouter()

webapp_router.include_router(route_jobs.router, prefix = "", tags = ['home-page'])
webapp_router.include_router(route_users.router, prefix = "", tags = ['users'])
webapp_router.include_router(route_login.router, prefix = "", tags = ['auth'])