from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Itinerary(Base):
    __tablename__ = 'itineraries'
    id = Column(Integer, primary_key=True)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    activities = Column(ARRAY(String))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="itineraries")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    itineraries = relationship("Itinerary", back_populates="user")