from fastapi import HTTPException, status
from schemas import schema_payment_master as scm
from sqlalchemy.orm import Session
from models import model


def get_all_payment_master_repo(db: Session):
    pm = db.query(model.PaymentMaster).order_by(model.PaymentMaster.paym_id).all()
    return pm


def create_payment_master_repo(pm: scm.PaymentMasterCreate, db: Session):
    payment_code = db.query(model.PaymentMaster.paym_code).filter_by(paym_code=pm.paym_code).scalar()
    if payment_code is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This payment code is already exits")

    create_pm = model.PaymentMaster(**pm.model_dump())
    db.add(create_pm)
    db.commit()
    db.refresh(create_pm)
    return create_pm

