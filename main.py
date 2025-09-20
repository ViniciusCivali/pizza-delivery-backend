from fastapi import FastAPI
from routes import auth_router, order_router

app = FastAPI()
app.include_router(order_router)
app.include_router(auth_router)
