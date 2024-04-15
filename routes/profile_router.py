from fastapi import APIRouter
from config.database import student_profile
from models.model import Student_Profile
from schema.schemas import list_Serial_profile

profile_router = APIRouter()

@profile_router.post('/studentProfile', tags=["Student Profile"])
async def update_profile(profile: Student_Profile):
    student_profile.insert_one(dict(profile))

@profile_router.get("/studentProfile/{student_Id}", tags=["Student Profile"])
async def get_student_profile(student_Id: str):
    profile = list_Serial_profile(student_profile.find({ "studentId": student_Id}))
    return profile


    