from fastapi import FastAPI

from app.database import engine, Base
from app.models.user import User
from app.routes.auth import router as auth_router
from app.models.url import URL
from app.routes.url import router as url_router 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(
    url_router,
    prefix="/url",
    tags=["URL"]
)


@app.get("/")
def home():
    return {"message": "URL Shortener API"}