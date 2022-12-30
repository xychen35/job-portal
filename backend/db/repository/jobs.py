from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from schemas.jobs import JobCreate
from db.models.jobs import Job
from core.hashing import Hasher

def create_new_job(job: JobCreate, db: Session, owner_id: int):
    job = Job(**job.dict(), owner_id = owner_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def retreive_job(id: int, db: Session):
    job = db.query(Job).filter(Job.id==id).first()
    if not job:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id:{id} does not exist")
    return job