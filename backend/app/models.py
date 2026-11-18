from datetime import datetime, date
from sqlalchemy import String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    led_projects: Mapped[list["Project"]] = relationship("Project", back_populates="leader")
    collaboration_requests: Mapped[list["CollaborationRequest"]] = relationship("CollaborationRequest", back_populates="user")
    deadline_extensions: Mapped[list["DeadlineExtension"]] = relationship("DeadlineExtension", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    leader_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Relationships
    leader: Mapped["User"] = relationship("User", back_populates="led_projects")
    collaboration_requests: Mapped[list["CollaborationRequest"]] = relationship("CollaborationRequest", back_populates="project", cascade="all, delete-orphan")
    deadline_extensions: Mapped[list["DeadlineExtension"]] = relationship("DeadlineExtension", back_populates="project", cascade="all, delete-orphan")


class CollaborationRequest(Base):
    __tablename__ = "collaboration_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    invited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, accepted, rejected
    role: Mapped[str] = mapped_column(String(20), default="editor", nullable=False)     # viewer, editor

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="collaboration_requests")
    user: Mapped["User"] = relationship("User", back_populates="collaboration_requests")


class DeadlineExtension(Base):
    __tablename__ = "deadline_extensions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, approved, rejected
    requested_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="deadline_extensions")
    user: Mapped["User"] = relationship("User", back_populates="deadline_extensions")