from fastapi import APIRouter

from webapps.jobs import route_jobs
from webapps.users import route_users

webapp_router = APIRouter()

webapp_router.include_router(route_jobs.router, prefix = "", tags = ['home-page'])
webapp_router.include_router(route_users.router, prefix = "", tags = ['home-page'])