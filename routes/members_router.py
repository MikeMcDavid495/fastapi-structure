from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import members_schema
from repositories import cars_repo, members_repo

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


@router.post("/create_car_for_member", response_model=members_schema.ResultData, status_code=status.HTTP_201_CREATED)
def create_car_for_member(owner_id: int, car: members_schema.CarBase, db: Session = Depends(get_db)):
    try:
        car = members_repo.create_car_for_member_repo(owner_id=owner_id, car=car, db=db)
        return {"status": True, "message": "created!", "data": car}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.get("/get_members", response_model=members_schema.ResultData, status_code=status.HTTP_200_OK)
def get_member(member_id: int, db: Session = Depends(get_db)):
    try:
        member = members_repo.get_member_repo(member_id=member_id, db=db)
        return {"status": True, "message": "get member completed!", "data": member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.post("/add_member", response_model=members_schema.ResultData, status_code=status.HTTP_201_CREATED)
def add_member(member: members_schema.MemberCreate, db: Session = Depends(get_db)):
    try:
        created_member = members_repo.add_member_repo(member=member, db=db)
        return {"status": True, "message": "member added!", "data": created_member}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))


@router.patch("/update_member", response_model=members_schema.ResultData, status_code=status.HTTP_200_OK)
def update_member(member_update: members_schema.MemberUpdate, db: Session = Depends(get_db)):
    try:
        update_firstname = members_repo.update_member_repo(member_update=member_update, db=db)
        return {"status": True, "message": "member added!", "data": update_firstname}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))