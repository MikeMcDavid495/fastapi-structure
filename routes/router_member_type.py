from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_member_type
from repositories import repo_member_type

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


@router.get("/get_member_type", response_model=schema_member_type.ResultData, status_code=status.HTTP_200_OK)
def get_member_type(type_id: int, db: Session = Depends(get_db)):
    try:
        list_of_member = repo_member_type.get_member_type(type_id=type_id, db=db)
        return {"status": True, "message": "get data completed!", "data": list_of_member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.post("/create_member_type", response_model=schema_member_type.ResultData, status_code=status.HTTP_201_CREATED)
def create_member_type(member_type: schema_member_type.MemberTypeCreate, db: Session = Depends(get_db)):
    try:
        member_type = repo_member_type.create_member_type_repo(member_type=member_type, db=db)
        return {"status": True, "message": "created", "data": member_type}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))

