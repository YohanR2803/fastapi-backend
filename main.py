# main.py
from fastapi import FastAPI, Depends, Request, HTTPException, Form
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

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
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

# Endpoint for Zoho Form submission
@app.post("/submissions", status_code=201)
async def create_submission(
    request: Request,
    email: str = Form(...),
    discord_id: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    mobile_no: str = Form(None),
    country: str = Form(None),
    db: Session = Depends(get_db),
    _: None = Depends(verify_auth)
):
    raw_body = await request.body()
    print("RAW REQUEST BODY:\n", raw_body.decode())

    db_obj = models.Submission(
        email=email,
        discord_id=discord_id,
        first_name=first_name,
        last_name=last_name,
        mobile_no=mobile_no,
        country=country,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Optionally call Discord bot (commented out for now)
    # await discord_bot.assign_verified_role(discord_id)

    return {"id": db_obj.id, "verified": True}
