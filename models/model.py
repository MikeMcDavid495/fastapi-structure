from sqlalchemy import Boolean, String, Integer, DateTime, Date, Column, NVARCHAR
from databases.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    color = Column(String)
    license_plate = Column(NVARCHAR(length=10))
    province = Column(NVARCHAR(length=100))

