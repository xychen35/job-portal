from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schemas.jobs import JobCreate, ShowJob
from db.models.users import User
from db.session import get_db
from db.repository.jobs import create_new_job, retreive_job, retreive_all_jobs, update_job_by_id, delete_job_by_id

from apis.version1.route_login import get_current_user_from_token

from typing import List


router = APIRouter()

@router.post("/create-job", response_model=ShowJob, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    job = create_new_job(job=job, db=db, owner_id=owner_id)
    return job

@router.get("/get/{id}", response_model=ShowJob, status_code=status.HTTP_200_OK)
async def read_job(id: int, db: Session=Depends(get_db)):
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id:{id} does not exist")
    return job

@router.get("/all-jobs", response_model=List[ShowJob], status_code=status.HTTP_200_OK)
async def list_jobs(db: Session=Depends(get_db)):
    jobs = retreive_all_jobs(db=db)
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is not avaiable job in the Jobs database")
    return jobs

@router.put("/update-job/{id}", status_code=status.HTTP_200_OK)
async def update_job(id: int, job: JobCreate, db: Session=Depends(get_db)):
    owner_id = 1
    message = update_job_by_id(id=id, job=job, db=db, owner_id=owner_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id:{id} does not exist")
    return {"detail": "Successfully updated"}

@router.delete("/delete-job/{id}", status_code=status.HTTP_200_OK)
async def delete_job(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id:{id} does not exist")
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted")