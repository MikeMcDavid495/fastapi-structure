from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from schemas import orders_schema
from repositories import orders_repo


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
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


@router.post("/create_order", response_model=orders_schema.ResultData, status_code=status.HTTP_201_CREATED)
def create_order(order: orders_schema.OrderCreate, db: Session = Depends(get_db)):
    try:
        created_order = orders_repo.create_order_repo(order=order, db=db)
        return {"status": True, "message": "created", "data": created_order}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=content_return_error(e))

