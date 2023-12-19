from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from schemas import schema_parking_master
from repositories import repo_parking_master

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
             response_model=schema_parking_master.ResultData,
             status_code=status.HTTP_201_CREATED)
def create_parking_master(parking: schema_parking_master.ParkingMasterCreate, db: Session = Depends(get_db)):
    try:
        created_parking = repo_parking_master.create_parking_master_repo(parking=parking, db=db)
        return {"status": True, "message": "created", "data": created_parking}
    except HTTPException as e:
        return content_return_error(e)

