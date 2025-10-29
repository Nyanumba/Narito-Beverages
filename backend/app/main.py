from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.users import User
from app.api.v1 import auth 

from app.core.config import settings
print("Loaded DB:", settings.postgres_db)


app = FastAPI(title = "Narito-Bevarages")
app.include_router (auth.router, prefix = "/auth", tags =["Auth"])

Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return {"message": "The Narito-Bevarage shop API is running"}