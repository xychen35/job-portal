from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import retreive_all_jobs, retreive_job
from sqlalchemy.orm import Session
from db.session import get_db

from webapps.jobs.forms import JobCreateForm
from db.models.users import User
from schemas.jobs import JobCreate
from db.repository.jobs import create_new_job 
from apis.version1.route_login import get_current_user_from_token
from fastapi.security.utils import get_authorization_scheme_param

from apis.version1.route_jobs import list_jobs

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/")
async def home(request: Request, db: Session=Depends(get_db), msg: str = None):
    jobs = retreive_all_jobs(db=db)
    return templates.TemplateResponse("jobs/homepage.html", {"request": request, "jobs": jobs, "msg": msg})

@router.get("/detail/{id}")
async def job_detail(id: int, request: Request, db: Session=Depends(get_db)):
    job = retreive_job(id=id, db=db)
    return templates.TemplateResponse("jobs/detail.html", {"request": request, "job": job})

@router.get("/post-a-job/")
async def create_job(request: Request, db: Session=Depends(get_db)):
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})

@router.post("/post-a-job/")
async def create_job(request: Request, db: Session=Depends(get_db)):
    form = JobCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(token)
            current_user: User = get_current_user_from_token(token=param, db=db)
            job = JobCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/detail/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)

@router.get("/delete-job/")
async def show_jobs_to_delete(request: Request, db: Session=Depends(get_db)):
    jobs = await list_jobs(db=db)
    return templates.TemplateResponse("jobs/show_jobs_to_delete.html", {"request": request, "jobs": jobs})