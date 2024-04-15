from fastapi import FastAPI

from routes.route import router
from routes.profile_router import profile_router
from routes.optional_router import optional_router

app = FastAPI()

app.include_router(router)
app.include_router(profile_router)
app.include_router(optional_router)
