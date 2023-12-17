from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from schemas import parking_master_schema
from repositories import parking_master_repo

router = APIRouter(
    prefix="/parking_master",
    tags=["Parking Master"],
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


@router.post("/create_parking_master",
             response_model=parking_master_schema.ResultData,
             status_code=status.HTTP_201_CREATED)
def create_parking_master(parking: parking_master_schema.ParkingMasterCreate, db: Session = Depends(get_db)):
    try:
        created_parking = parking_master_repo.create_parking_master_repo(parking=parking, db=db)
        return {"status": True, "message": "created", "data": created_parking}
    except HTTPException as e:
        return content_return_error(e)

