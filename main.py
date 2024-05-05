from fastapi import FastAPI
from routes.authentication import router
from routes.admin_routes.module_route import adminRouter
from routes.optional_module_router import optional_router
from routes.study_material_route import studyMaterialRouter
from routes.Excercise_and_assignment  import assignmentRouter

app = FastAPI()

app.include_router(router)
# app.include_router(profile_router)
# app.include_router(optional_router)
app.include_router(studyMaterialRouter)
app.include_router(assignmentRouter)
# app.include_router(adminRouter)