from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_payment_master as scm
from repositories import repo_payment_master as rpm

router = APIRouter(
    prefix="/payment_master",
    tags=["Payment Master"],
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


@router.post("/create_payment_master", response_model=scm.ResultData, status_code=status.HTTP_201_CREATED)
def create_payment_master(pm: scm.PaymentMasterCreate, db: Session = Depends(get_db)):
    try:
        created_pm = rpm.create_payment_master_repo(pm=pm, db=db)
        return {"status": True, "message": "created", "data": created_pm}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

