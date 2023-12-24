from sqlalchemy import (Boolean, String, Integer, DateTime, Date, Numeric,
                        Column, NVARCHAR, VARCHAR, ForeignKey, UUID, TIMESTAMP, DECIMAL, Identity)
from sqlalchemy.orm import relationship
from databases.database import Base
from datetime import datetime
import uuid


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(length=35))
    last_name = Column(VARCHAR(length=50))
    id_card = Column(VARCHAR(length=13))
    expiry_date = Column(Date, default=datetime.now().date())

    member_type_id = Column(Integer, ForeignKey("member_type.member_type_id"))
    member_of_parking = Column(VARCHAR(length=10), ForeignKey("parking_master.parking_code"))

    r_member_type_id = relationship("MemberType", back_populates="r_member_type_id")
    cars_owned = relationship("Car", back_populates="owner")
    parking = relationship("ParkingMaster", back_populates="member")


class MemberType(Base):
    __tablename__ = "member_type"

    id = Column(Integer, Identity(start=0), primary_key=True, index=True)
    member_type_id = Column(Integer, unique=True)
    member_type_name = Column(VARCHAR(length=20))

    r_member_type_id = relationship("Member", back_populates="r_member_type_id")


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


class ParkingMaster(Base):
    __tablename__ = "parking_master"

    id = Column(Integer, primary_key=True, autoincrement=True)

    parking_code = Column(VARCHAR(length=10), unique=True)
    parking_name = Column(VARCHAR(length=60))
    location = Column(VARCHAR(length=150))
    parking_bays = Column(Integer)

    member = relationship("Member", back_populates="parking")
    parking_setting = relationship("ParkingFeeSetting", back_populates="parking_fee")


class ParkingFeeSetting(Base):
    __tablename__ = "parking_fee_setting"

    pf_id = Column(Integer, primary_key=True, autoincrement=True)
    parking_code = Column(VARCHAR(length=10), ForeignKey("parking_master.parking_code"))
    pf_hour_01 = Column(Integer)
    pf_hour_02 = Column(Integer)
    pf_hour_03 = Column(Integer)
    pf_hour_04 = Column(Integer)
    pf_hour_05 = Column(Integer)
    pf_hour_06 = Column(Integer)
    pf_hour_07 = Column(Integer)
    pf_hour_08 = Column(Integer)
    pf_hour_09 = Column(Integer)
    pf_hour_10 = Column(Integer)
    pf_hour_11 = Column(Integer)
    pf_hour_12 = Column(Integer)
    pf_hour_13 = Column(Integer)
    pf_hour_14 = Column(Integer)
    pf_hour_15 = Column(Integer)
    pf_hour_16 = Column(Integer)
    pf_hour_17 = Column(Integer)
    pf_hour_18 = Column(Integer)
    pf_hour_19 = Column(Integer)
    pf_hour_20 = Column(Integer)
    pf_hour_21 = Column(Integer)
    pf_hour_22 = Column(Integer)
    pf_hour_23 = Column(Integer)
    pf_hour_24 = Column(Integer)
    pf_day = Column(Integer)
    pf_month = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)

    parking_fee = relationship("ParkingMaster", back_populates="parking_setting")


class Parking(Base):
    __tablename__ = "parkings"

    p_id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(VARCHAR(length=36), default=str(uuid.uuid4()), unique=True)
    parking_code = Column(VARCHAR(length=10))
    p_license_plate = Column(VARCHAR(length=10))
    p_qr_code = Column(VARCHAR(length=100), nullable=True)
    p_time_in = Column(DateTime)
    p_license_plate_time_in_img_location = Column(VARCHAR(length=100))
    p_time_out = Column(DateTime, default=None)
    p_time_out_expiry_time = Column(DateTime, default=None)
    p_license_plate_time_out_img_location = Column(VARCHAR(length=100))
    p_amount_exc_vat = Column(Numeric(10, 2))
    p_vat = Column(Numeric(10, 2))
    p_amount_inc_vat = Column(Numeric(10, 2))
    p_waived_flag = Column(Boolean)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    member_type_id = Column(Integer, ForeignKey("member_type.member_type_id"))
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class Transaction(Base):
    __tablename__ = "transactions"

    t_id = Column(Integer, primary_key=True)
    uuid = Column(VARCHAR(length=36), ForeignKey("parkings.uuid"))
    paym_id = Column(Integer, ForeignKey("payment_master.paym_id"))
    t_paid_amount = Column(DECIMAL(10, 2))
    t_paid_datetime = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class PaymentMaster(Base):
    __tablename__ = "payment_master"

    paym_id = Column(Integer, primary_key=True)
    paym_code = Column(VARCHAR(length=10))
    paym_name_th = Column(VARCHAR(length=50))
    paym_name_en = Column(VARCHAR(length=50))
    active_flag = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class Estamps(Base):
    __tablename__ = "estamps"

    e_id = Column(Integer, primary_key=True)
    uuid = Column(VARCHAR(length=36), ForeignKey("parkings.uuid"))
    esta_id = Column(Integer, ForeignKey("estamp_master.esta_id"))
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class EstampMaster(Base):
    __tablename__ = "estamp_master"

    esta_id = Column(Integer, primary_key=True)
    esta_t_id = Column(Integer, ForeignKey("estamp_type_master.esta_t_id"))
    esta_code = Column(VARCHAR(length=10))
    esta_name_th = Column(VARCHAR(length=50))
    esta_name_en = Column(VARCHAR(length=50))
    active_flag = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class EstampTypeMaster(Base):
    __tablename__ = "estamp_type_master"

    esta_t_id = Column(Integer, primary_key=True)
    esta_t_name = Column(VARCHAR(length=50))
    active_flag = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class EstampFeeSetting(Base):
    __tablename__ = 'estamp_fee_setting'

    ef_id = Column(Integer, primary_key=True, autoincrement=True)
    esta_id = Column(Integer, ForeignKey("estamp_master.esta_id"))
    ef_hour_01 = Column(Integer)
    ef_hour_02 = Column(Integer)
    ef_hour_03 = Column(Integer)
    ef_hour_04 = Column(Integer)
    ef_hour_05 = Column(Integer)
    ef_hour_06 = Column(Integer)
    ef_hour_07 = Column(Integer)
    ef_hour_08 = Column(Integer)
    ef_hour_09 = Column(Integer)
    ef_hour_10 = Column(Integer)
    ef_hour_11 = Column(Integer)
    ef_hour_12 = Column(Integer)
    ef_hour_13 = Column(Integer)
    ef_hour_14 = Column(Integer)
    ef_hour_15 = Column(Integer)
    ef_hour_16 = Column(Integer)
    ef_hour_17 = Column(Integer)
    ef_hour_18 = Column(Integer)
    ef_hour_19 = Column(Integer)
    ef_hour_20 = Column(Integer)
    ef_hour_21 = Column(Integer)
    ef_hour_22 = Column(Integer)
    ef_hour_23 = Column(Integer)
    ef_hour_24 = Column(Integer)
    ef_day = Column(Integer)
    ef_month = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)


class EventLogs(Base):
    __tablename__ = "event_logs"

    e_id = Column(Integer, primary_key=True, index=True)
    e_type = Column(VARCHAR(length=15))
    e_table = Column(VARCHAR(length=40))
    e_field = Column(VARCHAR(length=30))
    e_key_id = Column(VARCHAR(length=50))
    created_at = Column(DateTime, default=datetime.now())

