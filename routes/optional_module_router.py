from fastapi import APIRouter
from config.database import optional_course, student_profile
from models.student_model import OPTIONAL_MODULE_IN_PROGRAM, MODULE_INFO
from schema.schemas import list_Serial_optional_course

optional_router = APIRouter()

@optional_router.post('/optionalCourses', tags=["APIs to show Optional courses, and enrollement and quit from courses"])
async def update_profile(profile: OPTIONAL_MODULE_IN_PROGRAM):
    optional_course.insert_one(dict(profile))

@optional_router.get("/getOptionalCourses", tags=["APIs to show Optional courses, and enrollement and quit from courses"])
async def get_student_profile(program_Id: str):
    ops_course = list_Serial_optional_course(optional_course.find({"programId": program_Id}))
    return ops_course

@optional_router.post("/enrollment", tags=["APIs to show Optional courses, and enrollement and quit from courses"])
async def enroll_student(module_Id: str, student_Id: str, class_time: str):
    studentProfile = student_profile.find_one({"studentId": student_Id })
    if studentProfile :
        optionalCourse = optional_course.find_one({"programId": studentProfile.programId})
    return optionalCourse