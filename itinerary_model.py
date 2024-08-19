from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URL)
DatabaseSession = sessionmaker(bind=engine)
BaseModel = declarative_base()

class TravelItinerary(BaseModel):
    __tablename__ = 'travel_itineraries'
    itinerary_id = Column(Integer, primary_key=True)
    target_destination = Column(String, nullable=False)
    journey_start_date = Column(Date, nullable=False)
    journey_end_date = Column(Date, nullable=False)
    planned_activities = Column(ARRAY(String))
    planner_user_id = Column(Integer, ForeignKey('users.id'))
    associated_user = relationship("User", back_populates="travel_itineraries")