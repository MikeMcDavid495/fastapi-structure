from fastapi import HTTPException, status
from schemas import schema_estamp_master
from sqlalchemy.orm import Session
from models import model


def add_estamp_master_repo(es_master: schema_estamp_master.EstampMasterCreate, db: Session):
    e_stamp_type = db.query(model.EstampTypeMaster.esta_t_id).filter_by(esta_t_id=es_master.esta_t_id).scalar()
    if e_stamp_type is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-Stamp Type ID not available")

    e_stamp = model.EstampMaster(**es_master.model_dump())
    db.add(e_stamp)
    db.commit()
    db.refresh(e_stamp)
    return e_stamp

