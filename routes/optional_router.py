from fastapi import APIRouter
from config.database import optional_course
from models.model import Optional_Courses
from schema.schemas import list_Serial_optional_course

optional_router = APIRouter()

@optional_router.post('/optionalCourses', tags=["Opotional Courses"])
async def update_profile(profile: Optional_Courses):
    optional_course.insert_one(dict(profile))

@optional_router.get("/optionalCourses/{program_Id}", tags=["Opotional Courses"])
async def get_student_profile(program_Id: str):
    ops_course = list_Serial_optional_course(optional_course.find({"programId": program_Id}))
    return ops_course