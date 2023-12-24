from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_estamps as se
from repositories import repo_estamps as re


router = APIRouter(
    prefix="/estamps",
    tags=["E-Stamps"],
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


@router.post("/estamp", response_model=se.ResultData, status_code=status.HTTP_201_CREATED)
def e_stamp(e_register: se.EstampRegister, db: Session = Depends(get_db)):
    try:
        data = re.e_stamp_repo(e_register=e_register, db=db)
        return {"status": True, "message": "success", "data": data}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

