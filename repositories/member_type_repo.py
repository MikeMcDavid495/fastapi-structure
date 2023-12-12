from sqlalchemy.orm import Session
from models import model
from schemas import member_type_schema


def get_member_type(type_id: int, skip: int, take: int, db: Session):
    pass
    # member_type = db.query(model.Member).join(modelMemberType).filter(Member.member_type_id == 1 and MemberType.id == 1)
    # return member_type


def create_member_type_repo(member_type: member_type_schema.MemberTypeCreate, db: Session):
    created_type = model.MemberType(**member_type.model_dump())
    db.add(created_type)
    db.commit()
    db.refresh(created_type)
    return created_type

