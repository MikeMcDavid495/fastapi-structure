import uuid

from fastapi import HTTPException, status
from schemas import schema_parkings
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import model
from datetime import datetime
import math


def entrance_repo(tr_in: schema_parkings.ParkingBase, db: Session):
    member = (db.query(model.Member)
              .join(model.Car)
              .filter(model.Member.member_of_parking == tr_in.parking_code, model.Car.license_plate == tr_in.p_license_plate)
              .first())

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no Member in this parking")

    # this is member
    if datetime.now().date() > member.expiry_date:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Member has been expired")

    # print(member.member_id)

    json_entrance = schema_parkings.ParkingCreate(
        parking_code=tr_in.parking_code,
        p_license_plate=tr_in.p_license_plate,
        p_qr_code=tr_in.p_qr_code,
        member_id=member.id,
        member_type_id=member.member_type_id,
        p_time_in=datetime.now(),
        uuid=str(uuid.uuid4()),
        p_license_plate_time_in_img_location="c:/",
        p_time_out=None,
        p_time_out_expiry_time=None,
        p_license_plate_time_out_img_location="c:/",
        p_amount_exc_vat=0.7,
        p_vat=0.7,
        p_amount_inc_vat=1.4,
        p_waived_flag=True
    )
    #
    transaction_in = model.Parking(**json_entrance.model_dump())
    db.add(transaction_in)
    db.commit()
    db.refresh(transaction_in)
    return transaction_in


def entrance_app_repo(tr_in: schema_parkings.ParkingBase, db: Session):
    # member = (db.query(model.Member)
    #           .join(model.Car)
    #           .filter(model.Member.member_of_parking == tr_in.parking_code, model.Car.license_plate == tr_in.p_license_plate)
    #           .first())
    #
    # if member is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no Member in this parking")
    #
    # # this is member
    # if datetime.now().date() > member.expiry_date:
    #     raise HTTPException(status_code=status.HTTP_410_GONE, detail="Member has been expired")
    pass


def entrance_kiosk_repo(tr_in: schema_parkings.ParkingBase, db: Session):
    json_entrance = schema_parkings.ParkingCreate(
        parking_code=tr_in.parking_code,
        p_license_plate=tr_in.p_license_plate,
        p_qr_code=tr_in.p_qr_code,
        member_id=None,
        member_type_id=0,
        p_time_in=datetime.now(),
        uuid=str(uuid.uuid4()),
        p_license_plate_time_in_img_location="c:/",
        p_time_out=None,
        p_time_out_expiry_time=None,
        p_license_plate_time_out_img_location="c:/",
        p_amount_exc_vat=0.7,
        p_vat=0.7,
        p_amount_inc_vat=1.4,
        p_waived_flag=False
    )

    transaction_in = model.Parking(**json_entrance.model_dump())
    db.add(transaction_in)
    db.commit()
    db.refresh(transaction_in)
    return transaction_in


def stamp_transaction_out_repo(tr_out: schema_parkings.ParkingUpdate, db: Session):
    t_out = db.query(model.Parking).filter_by(uuid=tr_out.uuid).first()

    if t_out is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction in not found")

    transaction_out = t_out
    transaction_out.p_time_out = datetime.now()
    transaction_out.p_time_out_expiry_time = datetime.now()
    transaction_out.updated_at = datetime.now()

    # update_data = t_out.model_dump(exclude_unset=True)
    #
    # for key, value in update_data.items():
    #     setattr(tr_in, key, value)

    db.commit()
    return transaction_out


def parking_calculation(qrcode: str, db: Session):
    parking = db.query(model.Parking).filter_by(p_qr_code=qrcode).first()

    if parking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบ QR code นี้ในระบบ")

    if parking.p_waived_flag:
        json_res = {
            "status": True,
            "message": "ไม่มียอดชำระ",
            "data": None
        }
        return json_res

    if parking.p_time_out is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบ QR code นี้ในระบบ")

    data_uuid = parking.uuid
    parking_code = parking.parking_code

    dict_cal = total_expenses(data_uuid, parking_code, db)
    if dict_cal:
        if all([dict_cal["parking_minutes"] < 15, dict_cal["parking_hours"] < 1, dict_cal["parking_days"] < 1]):
            return {
                "status": True,
                "message": "ไม่มียอดชำระ",
                "data": dict_cal
            }

    return {
        "status": True,
        "message": "success",
        "data": dict_cal
    }


def total_expenses(tr_uuid: str, parking_code: str, db: Session):

    # case: entrance not found
    time_in = db.query(model.Parking.p_time_in).filter_by(uuid=tr_uuid).scalar()
    if time_in is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")

    # case: not found setting fee for that parking code
    parking_fee = db.query(model.ParkingFeeSetting).filter_by(parking_code=parking_code, deleted_at=None).first()
    if parking_fee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no parking fee for this parking code")

    # case: parking less than 15 minutes
    minutes_total = math.floor((datetime.now() - time_in).total_seconds() / 60.0)
    if minutes_total < 15:
        return {
            "time_in": time_in,
            "current_time": datetime.now(),
            "parking_days": 0,
            "parking_hours": 0,
            "parking_minutes": minutes_total,
            "parking_total_amount": 0,
            "e_stamp_discount": 0,
            "total_paid": 0
        }

    # parked more than 15 minutes, calculation cost
    parking_days = math.floor(minutes_total / 1440)
    real_hour = math.floor((minutes_total % 1440) / 60)
    parking_hours = math.ceil((minutes_total % 1440) / 60)
    parking_minutes = math.floor((minutes_total % 1440) % 60)

    sum_total = 0
    sum_of_the_day = 0

    keys = list(parking_fee.__dict__.keys())
    keys.sort()

    if parking_fee:
        day_rate = [value for key, value in parking_fee.__dict__.items() if key == "pf_day"][0]
        sum_total = parking_days * day_rate

        for key in keys:

            if str(key).startswith("pf_hour_"):
                print("sum_value : ", sum_of_the_day)
                print("day_rate : ", day_rate)

                db_hour = str(key).rsplit('_', 1)[-1]
                pa_hour = f"{parking_hours:02d}"

                value = getattr(parking_fee, key)
                sum_of_the_day = sum_of_the_day + int(value)

                if db_hour == pa_hour:
                    if sum_of_the_day >= day_rate:
                        sum_total = sum_total + day_rate
                        break
                    sum_total = sum_total + sum_of_the_day
                    break

    e_sum_of_the_day = 0
    e_sum_total = 0

    # in case: got discount from e-stamp
    e_stamp = (
        db.query(model.Estamps, model.EstampFeeSetting)
        .filter(model.Estamps.uuid == tr_uuid)
        .all()
    )
    if len(e_stamp) > 0:

        e_keys = list(e_stamp[0][1].__dict__.keys())
        e_keys.sort()

        e_stamp_dict = {key: value for key, value in e_stamp[0][1].__dict__.items()}
        print(e_stamp_dict)

        e_day_rate = [value for key, value in e_stamp[0][1].__dict__.items() if key == "ef_day"][0]
        e_sum_total = parking_days * e_day_rate

        for key in e_keys:

            if str(key).startswith("ef_hour_"):
                print("ส่วนลด : ", e_sum_of_the_day)
                print("ส่วนลดแบบเหมา : ", e_day_rate)

                e_db_hour = str(key).rsplit('_', 1)[-1]
                e_pa_hour = f"{parking_hours:02d}"

                value = getattr(e_stamp[0][1], key)
                e_sum_of_the_day = e_sum_of_the_day + int(value)

                if e_db_hour == e_pa_hour:
                    if e_sum_of_the_day >= e_day_rate:
                        e_sum_total = sum_total + e_day_rate
                        break
                    e_sum_total = e_sum_total + e_sum_of_the_day
                    break
        print("e_sum_total", e_sum_total)
    parking_total_amount = sum_total - e_sum_total

    # in case: check if already paid
    trans = db.query(model.Transaction).filter_by(uuid=tr_uuid).all()
    if len(trans) >= 1:
        total_paid = 0
        for tran in trans:
            total_paid = total_paid + tran.t_paid_amount

        if total_paid >= parking_total_amount:
            return {
                "time_in": time_in,
                "current_time": datetime.now(),
                "parking_days": 0,
                "parking_hours": 0,
                "parking_minutes": 0,
                "parking_total_amount": 0,
                "e_stamp_discount": 0,
                "total_paid": 0
            }
        else:
            parking_total_amount = int(parking_total_amount - total_paid)

    # in case: not paid yet
    dict_cal = {
        "time_in": time_in,
        "current_time": datetime.now(),
        "parking_days": parking_days,
        "parking_hours": real_hour,
        "parking_minutes": parking_minutes,
        "parking_total_amount": sum_total,
        "e_stamp_discount": e_sum_total,
        "total_paid": parking_total_amount
    }

    return dict_cal

