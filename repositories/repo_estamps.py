from datetime import datetime

from schemas import schema_estamps as se
from models import model
from sqlalchemy.orm import Session


def e_stamp_repo(e_register: se.EstampRegister, db: Session):
    parking = (db.query(model.Parking)
               .filter_by(p_qr_code=e_register.qrcode, parking_code=e_register.parking_code)
               .first())

    add_e_stamp = model.Estamps(
        uuid=parking.uuid,
        esta_id=3,
        created_at=datetime.now()
    )

    db.add(add_e_stamp)
    db.commit()
    db.refresh(add_e_stamp)
    return add_e_stamp

