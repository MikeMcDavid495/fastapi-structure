from sqlalchemy import Boolean, String, Integer, DateTime, Date, Column, NVARCHAR, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from databases.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(length=35))
    last_name = Column(VARCHAR(length=50))
    id_card = Column(VARCHAR(length=13))
    member_id = Column(Integer, ForeignKey("member_type.id"))

    member_type_id = relationship("MemberType", back_populates="member_type_id")
    cars_owned = relationship("Car", back_populates="owner")


class MemberType(Base):
    __tablename__ = "member_type"

    id = Column(Integer, primary_key=True, index=True)
    member_type_name = Column(VARCHAR(length=20))

    member_type_id = relationship("Member", back_populates="member_type_id")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(VARCHAR(length=20))
    color = Column(VARCHAR(length=20))
    license_plate = Column(VARCHAR(length=20))
    province = Column(VARCHAR(length=20))
    owner_id = Column(Integer, ForeignKey("members.id"))

    owner = relationship("Member", back_populates="cars_owned")
    # license_plate = Column(NVARCHAR(length=10))
    # province = Column(NVARCHAR(length=100))
