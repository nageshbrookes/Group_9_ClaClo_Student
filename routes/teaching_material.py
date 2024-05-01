from fastapi import APIRouter
from config.database import teacher_studymaterial_collection
from schema.schemas import list_Serial_teaching_material

studymaterial = APIRouter()

@studymaterial.get("/teaching", tags=["Teaching Material"])
async def get_student_profile():
    profile = list_Serial_teaching_material(teacher_studymaterial_collection.find({}))
    return profile




    