from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies.authen_bearer import JWTBearer
from databases.database import SessionLocal

from schemas import schema_transactions as st
from repositories import repo_transactions as rt

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
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


@router.get("/get_all_transactions", response_model=st.ResultData, status_code=status.HTTP_200_OK)
def get_all_transactions(skip: int = 0, take: int = 50, db: Session = Depends(get_db)):
    try:
        transactions = rt.get_all_transactions_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "success", "data": transactions}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.post("/create_transaction", response_model=st.ResultData, status_code=status.HTTP_201_CREATED)
def create_transaction(tr: st.TransactionCreate, db: Session = Depends(get_db)):
    try:
        created_tr = rt.create_transaction_repo(tr=tr, db=db)
        return {"status": True, "message": "created", "data": created_tr}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))

