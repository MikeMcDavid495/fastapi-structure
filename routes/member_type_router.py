from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import member_type_schema
from repositories import member_type_repo

router = APIRouter(
    prefix="/member_type",
    tags=["Member Type"],
    # dependencies=[Depends(JWTBearer())],
    responses={404: {"data": "not found!"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def content_return_error(e: HTTPException):
    return {"status": False, "message": str(e.detail), "data": None}


@router.get("/get_member_type")
def get_member_type(type_id: int, skip: int, take: int, db: Session = Depends(get_db)):
    try:
        list_of_member = member_type_repo.get_member_type(type_id=type_id, skip=skip, take=take, db=db)
        return {"status": True, "message": "get data completed!", "data": list_of_member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.post("/create_member_type", response_model=member_type_schema.ResultData, status_code=status.HTTP_201_CREATED)
def create_member_type(member_type: member_type_schema.MemberTypeCreate, db: Session = Depends(get_db)):
    try:
        member_type = member_type_repo.create_member_type_repo(member_type=member_type, db=db)
        return {"status": True, "message": "get data completed!", "data": member_type}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))