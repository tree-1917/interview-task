from fastapi import FastAPI
from app.auth import authRoute


app = FastAPI()


app.include_router(authRoute)