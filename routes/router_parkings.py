from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_parkings
from repositories import repo_parkings


router = APIRouter(
    prefix="/parkings",
    tags=["Pakings"],
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


@router.post("/stamp_transaction_in", response_model=schema_parkings.ResultData, status_code=status.HTTP_201_CREATED)
def stamp_transaction_in(tr_in: schema_parkings.ParkingBase, db: Session = Depends(get_db)):
    try:
        transaction_in = repo_parkings.stamp_transaction_in_repo(tr_in=tr_in, db=db)
        return {"status": True, "message": "created", "data": transaction_in}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.patch("/stamp_transaction_out", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
def stamp_transaction_out(tr_out: schema_parkings.ParkingUpdate, db: Session = Depends(get_db)):
    try:
        transaction_out = repo_parkings.stamp_transaction_out_repo(tr_out=tr_out, db=db)
        return {"status": True, "message": "created", "data": transaction_out}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.get("/total_expenses", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
def total_expenses(p_id: int, parking_code: str, db: Session = Depends(get_db)):
    try:
        total = repo_parkings.total_expenses(p_id=p_id, parking_code=parking_code, db=db)
        return {"status": True, "message": "created", "data": total}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

