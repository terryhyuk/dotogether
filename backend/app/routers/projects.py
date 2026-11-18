from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/projects", tags=["Projects"])

# [CREATE] Create a new project (task)
@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(req: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Verify if the leader user actually exists in the DB
    leader = db.query(models.User).filter(models.User.id == req.leader_id).first()
    if not leader:
        raise HTTPException(status_code=404, detail="Leader user not found")
    
    project = models.Project(**req.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

# [READ] Get my projects (Projects I lead + Projects I accepted collaboration invites for)
@router.get("/", response_model=list[schemas.ProjectOut])
def get_my_projects(user_id: int, db: Session = Depends(get_db)):
    # Extract project IDs where the user has an 'accepted' collaboration request
    invited_project_ids = (
        db.query(models.CollaborationRequest.project_id)
        .filter(
            models.CollaborationRequest.user_id == user_id,
            models.CollaborationRequest.status == "accepted",
        )
    )
    
    # Query projects led by the user OR projects the user is invited to
    projects = (
        db.query(models.Project)
        .filter(
            or_(
                models.Project.leader_id == user_id,
                models.Project.id.in_(invited_project_ids),
            )
        )
        .all()
    )
    return projects

# [UPDATE] Update project details (title, description, dates, etc.)
@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, req: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update only the fields that were explicitly provided in the req
    update_data = req.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        
    db.commit()
    db.refresh(project)
    return project

# [DELETE] Delete a project
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None