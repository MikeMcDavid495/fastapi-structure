from fastapi import HTTPException, status
from schemas import schema_parkings
from sqlalchemy.orm import Session
from models import model
from datetime import datetime
import math


def stamp_transaction_in_repo(tr_in: schema_parkings.ParkingBase, db: Session):
    json_time_in = schema_parkings.ParkingCreate(
        parking_code=tr_in.parking_code,
        p_license_plate=tr_in.p_license_plate,
        p_qr_code=tr_in.p_qr_code,
        member_id=tr_in.member_id,
        p_time_in=datetime.now(),
        p_license_plate_time_in_img_location="c:/",
        p_time_out=None,
        p_time_out_expiry_time=None,
        p_license_plate_time_out_img_location="c:/",
        p_amount_exc_vat=0.7,
        p_vat=0.7,
        p_amount_inc_vat=1.4,
        p_waived_flag=True
    )

    transaction_in = model.Parking(**json_time_in.model_dump())
    db.add(transaction_in)
    db.commit()
    db.refresh(transaction_in)
    return transaction_in


def stamp_transaction_out_repo(tr_out: schema_parkings.ParkingUpdate, db: Session):
    tr_in = db.query(model.Parking).filter_by(p_id=tr_out.p_id).first()

    if tr_in is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction in not found")

    transaction_out = tr_in
    transaction_out.p_time_out = datetime.now()
    transaction_out.p_time_out_expiry_time = datetime.now()
    transaction_out.updated_at = datetime.now()

    # update_data = tr_out.model_dump(exclude_unset=True)
    #
    # for key, value in update_data.items():
    #     setattr(tr_in, key, value)

    db.commit()
    return transaction_out


def total_expenses(p_id: int, parking_code: str, db: Session):
    tr = db.query(model.Parking).filter_by(p_id=p_id).first()
    minutes_total = (datetime.now() - tr.p_time_in).total_seconds() / 60.0

    parking_days = math.floor(minutes_total / 1440)
    parking_hours = math.ceil((minutes_total % 1440) / 60)
    parking_minutes = math.floor((minutes_total % 1440) % 60)

    sum_value = 0
    parking_fee = db.query(model.ParkingFeeSetting).filter_by(parking_code=parking_code).first()

    keys = list(parking_fee.__dict__.keys())
    keys.sort()

    if parking_fee:
        sum_value = sum_value + (parking_days * [value for key, value in parking_fee.__dict__.items() if key == "pf_day"][0])
        for key in keys:

            if str(key).startswith("pf_hour_"):

                db_hour = str(key).rsplit('_', 1)[-1]
                pa_hour = f"{parking_hours:02d}"

                value = getattr(parking_fee, key)
                sum_value = sum_value + int(value)

                if db_hour == pa_hour:
                    break

    dict_cal = {
        "parking_days": parking_days,
        "parking_hours": parking_hours,
        "parking_minutes": parking_minutes,
        "parking_total_amount": sum_value,
    }

    return dict_cal

