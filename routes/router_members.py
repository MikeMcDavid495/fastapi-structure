from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from typing import Annotated

from schemas import schema_members
from repositories import repo_cars, repo_members

router = APIRouter(
    prefix="/members",
    tags=["Members"],
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


@router.get("/get_all_members", response_model=schema_members.ResultData, status_code=status.HTTP_200_OK)
def get_all_members(skip: int = 0, take: int = 100, db: Session = Depends(get_db)):
    try:
        member = repo_members.get_all_members_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "get member completed!", "data": member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.get("/get_members", response_model=schema_members.ResultData, status_code=status.HTTP_200_OK)
def get_member(member_id: int, db: Session = Depends(get_db)):
    try:
        member = repo_members.get_member_repo(member_id=member_id, db=db)
        return {"status": True, "message": "get member completed!", "data": member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.post("/add_member", response_model=schema_members.ResultData, status_code=status.HTTP_201_CREATED)
def add_member(member: schema_members.MemberCreate, db: Session = Depends(get_db)):
    try:
        created_member = repo_members.add_member_repo(member=member, db=db)
        return {"status": True, "message": "member added!", "data": created_member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.patch("/update_member", response_model=schema_members.ResultData, status_code=status.HTTP_200_OK)
def update_member(
        member_update: Annotated[schema_members.MemberUpdate, Body(
            openapi_examples={
                "normal": {
                    "summary": "Normal Case",
                    "description": "`id` เป็น mandatory "
                                   "`id` is the mandatory field, "
                                   "update all",
                    "value": {
                        "id": 0,
                        "first_name": "string | replace to null if nothing change",
                        "last_name": "string | replace to null if nothing change",
                        "id_card": "string | replace to null if nothing change",
                        "expiry_date": "date | replace to null if nothing change",
                        "member_id": "int | replace to null if nothing change",
                        "member_of_parking": "str | replace to null if nothing change"
                    },
                },
                "converted": {
                    "summary": "An optionals update",
                    "description": "`id` is the mandatory field, "
                                   "update just only `first_name` and `expiry_date`",
                    "value": {
                        "id": 0,
                        "first_name": "พระอนาคามี",
                        "last_name": None,
                        "id_card": None,
                        "expiry_date": "2023-12-30",
                        "member_id": None,
                        "member_of_parking": None
                    },
                }
            },
        )],
        db: Session = Depends(get_db)):
    try:
        update_firstname = repo_members.update_member_repo(member_update=member_update, db=db)
        return {"status": True, "message": "member added!", "data": update_firstname}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))

