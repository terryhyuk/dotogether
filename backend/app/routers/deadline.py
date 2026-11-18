from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/deadline-extensions", tags=["Deadline Extensions"])

# [CREATE] Request a deadline extension
@router.post("/", response_model=schemas.DeadlineExtensionOut, status_code=status.HTTP_201_CREATED)
def create_deadline_extension(req: schemas.DeadlineExtensionCreate, user_id: int, db: Session = Depends(get_db)):
    # Verify if the project exists
    project = db.query(models.Project).filter(models.Project.id == req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    extension = models.DeadlineExtension(
        project_id=req.project_id,
        user_id=user_id,  # Will be replaced with the authenticated user ID from token later
        requested_due_date=req.requested_due_date,
        reason=req.reason,
        status="pending"
    )
    db.add(extension)
    db.commit()
    db.refresh(extension)
    return extension

# [READ] Get all deadline extension requests for a specific project
@router.get("/project/{project_id}", response_model=list[schemas.DeadlineExtensionOut])
def get_project_deadline_extensions(project_id: int, db: Session = Depends(get_db)):
    extensions = db.query(models.DeadlineExtension).filter(models.DeadlineExtension.project_id == project_id).all()
    return extensions

# [UPDATE] Approve or reject a deadline extension request (Leader permission)
@router.patch("/{extension_id}", response_model=schemas.DeadlineExtensionOut)
def update_deadline_extension_status(extension_id: int, req: schemas.DeadlineExtensionStatusUpdate, db: Session = Depends(get_db)):
    extension = db.query(models.DeadlineExtension).filter(models.DeadlineExtension.id == extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Deadline extension request not found")
    
    extension.status = req.status
    db.commit()
    db.refresh(extension)
    return extension