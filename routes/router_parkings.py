from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from dependencies.authen_bearer import JWTBearer
from sqlalchemy.orm import Session
from databases.database import SessionLocal

from schemas import schema_parkings
from repositories import repo_parkings


router = APIRouter(
    prefix="/parkings",
    tags=["Parkings"],
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


@router.get("/get_all_parkings", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
def get_all_parking(skip: int = 0, take: int = 10, db: Session = Depends(get_db)):
    try:
        parkings = repo_parkings.get_all_parking_repo(skip=skip, take=take, db=db)
        return {"status": True, "message": "success", "data": parkings}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.post("/entrance", response_model=schema_parkings.ResultData, status_code=status.HTTP_201_CREATED)
def entrance(tr_in: schema_parkings.ParkingBase, db: Session = Depends(get_db)):
    try:
        transaction_in = repo_parkings.entrance_repo(tr_in=tr_in, db=db)
        return {"status": True, "message": "created", "data": transaction_in}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.post("/entrance-app", response_model=schema_parkings.ResultData, status_code=status.HTTP_201_CREATED)
def entrance_app(tr_in: schema_parkings.ParkingBase, db: Session = Depends(get_db)):
    try:
        transaction_in = repo_parkings.entrance_app_repo(tr_in=tr_in, db=db)
        return {"status": True, "message": "created", "data": transaction_in}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.post("/entrance-kiosk", response_model=schema_parkings.ResultData, status_code=status.HTTP_201_CREATED)
def entrance_kiosk(tr_in: schema_parkings.ParkingBase, db: Session = Depends(get_db)):
    try:
        transaction_in = repo_parkings.entrance_kiosk_repo(tr_in=tr_in, db=db)
        return {"status": True, "message": "created", "data": transaction_in}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))


@router.patch("/exit-qrcode", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
def exit_by_qrcode(qrcode: schema_parkings.QRCode, db: Session = Depends(get_db)):
    try:
        result = repo_parkings.exit_by_qrcode_repo(qrcode=qrcode, db=db)
        return {"status": result["status"], "message": result["message"], "data": result["data"]}
    except HTTPException as e:
        return JSONResponse(content_return_error(e))
#
#
# @router.get("/payment", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
# def payment(qrcode: str, db: Session = Depends(get_db)):
#     try:
#         result = repo_parkings.parking_calculation(qrcode=qrcode, db=db)
#         return {"status": result["status"], "message": result["message"], "data": result["data"]}
#     except HTTPException as e:
#         return content_return_error(e)


# @router.get("/calculate", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
# def total_expenses(tr_uuid: str, parking_code: str, db: Session = Depends(get_db)):
#     try:
#         total = repo_parkings.total_expenses(tr_uuid=tr_uuid, parking_code=parking_code, db=db)
#         return {"status": True, "message": "success", "data": total}
#     except HTTPException as e:
#         return JSONResponse(content_return_error(e))

@router.post("/payment-kiosk", response_model=schema_parkings.ResultData, status_code=status.HTTP_200_OK)
def payment_kiosk(pk: schema_parkings.PaymentKiosk, db: Session = Depends(get_db)):
    try:
        result = repo_parkings.payment_kiosk_repo(pk=pk, db=db)
        return {"status": result["status"], "message": result["message"], "data": result["data"]}
    except HTTPException as e:
        return content_return_error(e)

