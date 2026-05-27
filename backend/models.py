from sqlalchemy import Column, Integer, String

from database import Base

class Visit(Base):

    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String)

    page = Column(String)

    duration = Column(String)

    device = Column(String)

    country = Column(String)