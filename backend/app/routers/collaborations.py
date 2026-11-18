from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/collaborations", tags=["Collaborations"])

@router.post("/invite", response_model=schemas.CollaborationOut)
def invite_collaborator(req: schemas.CollaborationInvite, db: Session = Depends(get_db)):
    collaboration = models.CollaborationRequest(**req.model_dump())
    db.add(collaboration)
    db.commit()
    db.refresh(collaboration)
    return collaboration

@router.get("/pending", response_model=list[schemas.CollaborationOut])
def get_pending_invites(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.CollaborationRequest)
        .filter(
            models.CollaborationRequest.user_id == user_id,
            models.CollaborationRequest.status == "pending",
        )
        .all()
    )

@router.patch("/{request_id}", response_model=schemas.CollaborationOut)
def respond_invite(request_id: int, req: schemas.CollaborationStatusUpdate, db: Session = Depends(get_db)):
    collaboration_req = db.query(models.CollaborationRequest).filter(models.CollaborationRequest.id == request_id).first()
    if not collaboration_req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    collaboration_req.status = req.status
    db.commit()
    db.refresh(collaboration_req)
    return collaboration_req