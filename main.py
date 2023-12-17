from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dependencies.authen_jwt import sign_jwt
from databases.database import engine
from models import model

from routes.cars_router import router as cars_router
from routes.members_router import router as members_router
from routes.member_type_router import router as member_type_router
from routes.orders_router import router as orders_router
from routes.parking_master_router import router as parking_master_order

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
app.include_router(orders_router)
app.include_router(parking_master_order)


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

