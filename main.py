from fastapi import FastAPI
from routes.route import router
from routes.profile_router import profile_router
from routes.optional_module_router import optional_router
from routes.route_studymaterial import studymaterial
from routes.Excercise_and_assignment  import assignmentRouter

app = FastAPI()

app.include_router(router)
# app.include_router(profile_router)
# app.include_router(optional_router)
app.include_router(studymaterial)
app.include_router(assignmentRouter)