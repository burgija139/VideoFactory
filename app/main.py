from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="VideoFactory API",
    description="API za pokretanje generisanja video sadržaja",
    version="1.0.0",
)

app.include_router(router)