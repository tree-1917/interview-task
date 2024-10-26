from fastapi import FastAPI
from app.auth import authRoute
from app.orginzation import orgRoute

app = FastAPI()


app.include_router(authRoute)
app.include_router(orgRoute)