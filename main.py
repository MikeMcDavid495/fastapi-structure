from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies.authen_jwt import sign_jwt
from databases.database import engine
from models import model
from routes.cars_router import router as car_router
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

app.include_router(car_router)


@app.get("/")
def hello():
    token = sign_jwt("mike")
    return {"hello": "car system", "token": token}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

