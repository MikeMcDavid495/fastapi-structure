from schemas import schema_estamp_type_master as setm
from models import model
from sqlalchemy.orm import Session


def create_estamp_type_master_repo(es_t_master: setm.EstampTypeMasterCreate, db: Session):
    create_es_t_master = model.EstampTypeMaster(**es_t_master.model_dump())
    db.add(create_es_t_master)
    db.commit()
    db.refresh(create_es_t_master)
    return create_es_t_master

