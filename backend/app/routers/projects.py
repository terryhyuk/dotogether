
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app import models, schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


# [CREATE] Create a new project
@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    req: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = models.Project(
        **req.model_dump(),
        leader_id=current_user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# [READ] Get my projects
@router.get("/", response_model=list[schemas.ProjectOut])
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    # Get project IDs where the user accepted collaboration invitations
    invited_project_ids = (
        db.query(models.CollaborationRequest.project_id)
        .filter(
            models.CollaborationRequest.user_id == user_id,
            models.CollaborationRequest.status == "accepted",
        )
    )

    # Get projects led by the user OR projects the user was invited to
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


# [UPDATE] Update project details
@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    req: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the current user is the project leader
    if project.leader_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to modify this project"
        )

    # Update only the fields explicitly provided in the request
    update_data = req.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


# [DELETE] Delete a project
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the current user is the project leader
    if project.leader_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this project"
        )

    db.delete(project)
    db.commit()

    return None
