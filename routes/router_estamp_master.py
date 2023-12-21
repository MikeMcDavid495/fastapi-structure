from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from databases.database import SessionLocal
from sqlalchemy.orm import Session

from schemas import schema_estamp_master
from repositories import repo_estamp_master

router = APIRouter(
    prefix="/estamp_master",
    tags=["E-Stamp Master"],
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


@router.post("/add_estamp_master", response_model=schema_estamp_master.ResultData, status_code=status.HTTP_201_CREATED)
def add_estamp_master(es_master: schema_estamp_master.EstampMasterCreate, db: Session = Depends(get_db)):
    try:
        created_stamp_master = repo_estamp_master.add_estamp_master_repo(es_master=es_master, db=db)
        return {"status": True, "message": "created", "data": created_stamp_master}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

