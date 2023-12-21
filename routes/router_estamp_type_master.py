from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_estamp_type_master as setm
from repositories import repo_stamp_type_master as rstm


router = APIRouter(
    prefix="/estamp_type_master",
    tags=["E-Stamp Type Master"],
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


@router.post("/create_estamp_type_master", response_model=setm.ResultData, status_code=status.HTTP_201_CREATED)
def create_estamp_type_master(es_t_master: setm.EstampTypeMasterCreate, db: Session = Depends(get_db)):
    try:
        created_e_stamp_type = rstm.create_estamp_type_master_repo(es_t_master=es_t_master, db=db)
        return {"status": True, "message": "created", "data": created_e_stamp_type}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


