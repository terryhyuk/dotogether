from datetime import datetime, date
from pydantic import BaseModel, EmailStr

# --- User ---
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    department: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    department: str | None

    model_config = {"from_attributes": True}


# --- Project ---
class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    start_date: date | None = None
    due_date: date | None = None

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: date | None = None
    due_date: date | None = None
    
class ProjectOut(BaseModel):
    id: int
    leader_id: int
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None

    model_config = {"from_attributes": True}


# --- Collaboration Request ---
class CollaborationInvite(BaseModel):
    project_id: int
    user_id: int
    role: str = "editor"

class CollaborationStatusUpdate(BaseModel):
    status: str  # accepted | rejected

class CollaborationOut(BaseModel):
    id: int
    project_id: int
    user_id: int
    invited_at: datetime
    status: str
    role: str

    model_config = {"from_attributes": True}

# --- Deadline Extension ---
class DeadlineExtensionCreate(BaseModel):
    project_id: int
    requested_due_date: date | None = None
    reason: str | None = None

class DeadlineExtensionStatusUpdate(BaseModel):
    status: str  # approved | rejected

class DeadlineExtensionOut(BaseModel):
    id: int
    project_id: int
    user_id: int
    status: str
    requested_due_date: date | None
    reason: str | None

    model_config = {"from_attributes": True}