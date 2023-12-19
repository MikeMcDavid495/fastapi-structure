from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dependencies.authen_jwt import sign_jwt
from databases.database import engine
from models import model

from routes.router_cars import router as cars_router
from routes.router_members import router as members_router
from routes.router_member_type import router as member_type_router
from routes.router_parking_master import router as parking_master
from routes.router_parking_fee_setting import router as parking_fee_setting_router
from routes.router_parkings import router as parkings_router

import uvicorn


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars_router)
app.include_router(members_router)
app.include_router(member_type_router)
app.include_router(parking_master)
app.include_router(parking_fee_setting_router)
app.include_router(parkings_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("REQUEST : ", request.__dict__)
    print("EXCEPTION : ", exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": False, "message": exc.args[0][0].get('msg'), "data": {
            "error_type": exc.args[0][0].get('loc')[0],
            "error_params": exc.args[0][0].get('loc')[1],
            "error_value": exc.args[0][0].get('input'),
        }})
    )


@app.get("/")
def hello():
    token = sign_jwt("mike")
    return {"hello": "car system", "token": token}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

