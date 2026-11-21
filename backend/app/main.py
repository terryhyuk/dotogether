from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users, projects, collaborations, deadline, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DoTogether API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(collaborations.router)
app.include_router(deadline.router)
app.include_router(auth.router)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}
