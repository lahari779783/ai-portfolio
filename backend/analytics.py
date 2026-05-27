from fastapi import APIRouter

from pydantic import BaseModel

from database import SessionLocal
from models import Visit

router = APIRouter()

class VisitData(BaseModel):

    session_id:str

    page:str

    duration:str

    device:str

    country:str

@router.post("/track")

async def track(data: VisitData):

    db = SessionLocal()

    visit = Visit(

        session_id=data.session_id,

        page=data.page,

        duration=data.duration,

        device=data.device,

        country=data.country
    )

    db.add(visit)

    db.commit()

    db.close()

    return {
        "message":"tracked"
    }