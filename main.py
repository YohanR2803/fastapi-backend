# main.py
from fastapi import FastAPI, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, discord_bot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("SECRET_TOKEN from .env:", os.getenv("SECRET_TOKEN"))

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

if not SECRET_TOKEN:
    raise RuntimeError("SECRET_TOKEN not set in .env")

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Define Pydantic model for submission data
class SubmissionIn(BaseModel):
    email: str
    discord_id: str
    first_name: str
    last_name: str
    mobile_no: str
    country: str

# Dependency to get a session from the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authorization check
def verify_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

# Endpoint to create a new submission
@app.post("/submissions", status_code=201)
async def create_submission(
    request: Request,  # Move request to the beginning as it doesn't have a default
    sub: SubmissionIn,
    db: Session = Depends(get_db),
    _: None = Depends(verify_auth)
):
    # Capture raw request body and print for debugging
    raw_body = await request.body()
    print("RAW REQUEST BODY:\n", raw_body.decode())
    
    # Create a new submission object and save it to the database
    db_obj = models.Submission(**sub.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Assign verified role in Discord using the bot
    await discord_bot.assign_verified_role(sub.discord_id)
    
    # Return the created submission ID and verified status
    return {"id": db_obj.id, "verified": True}
