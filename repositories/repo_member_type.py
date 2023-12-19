from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import model
from schemas import schema_member_type


def get_member_type(type_id: int, db: Session):
    member_type = db.query(model.MemberType).filter_by(id=type_id).first()
    if member_type is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="member type not found!")
    return member_type


def create_member_type_repo(member_type: schema_member_type.MemberTypeCreate, db: Session):
    member_type_name = db.query(model.MemberType).filter_by(member_type_name=member_type.member_type_name).first()
    if member_type_name is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already Member Type")

    created_type = model.MemberType(**member_type.model_dump())
    db.add(created_type)
    db.commit()
    db.refresh(created_type)
    return created_type

