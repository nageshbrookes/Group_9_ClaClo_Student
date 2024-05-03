from fastapi import APIRouter
from models.admin_model import MODULE_INFO_MODEL
from config.database import adminModuleInfo
from schema.schemas import list_Serial_user

adminRouter = APIRouter()

@adminRouter.post("/insert-module", tags=["module"])
async def insert_student(module: MODULE_INFO_MODEL):
    adminModuleInfo.insert_one(dict(module))
    return 'true'

