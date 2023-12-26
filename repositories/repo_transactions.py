from fastapi import HTTPException, status
from models import model
from sqlalchemy.orm import Session
from schemas import schema_transactions as st
from datetime import datetime, timedelta

from repositories import repo_parkings


def get_all_transactions_repo(skip: int, take: int, db: Session):
    transactions = db.query(model.Transaction).order_by(model.Transaction.t_id.desc()).offset(skip).limit(take).all()
    return transactions


def create_transaction_repo(tr: st.TransactionCreate, db: Session):
    try:
        create_tr = model.Transaction(**tr.model_dump())
        create_tr.t_paid_datetime = datetime.now()
        db.add(create_tr)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        if "a foreign key constraint fails" in str(e) and "FOREIGN KEY (`uuid`)" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        elif "a foreign key constraint fails" in str(e) and "FOREIGN KEY (`paym_id`)" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        db.refresh(create_tr)
        repo_parkings.normal_cal(tr.uuid, db)
        return create_tr

