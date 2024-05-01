from fastapi import APIRouter
from models.model import USERS
from config.database import users
from schema.schemas import list_Serial_user


router = APIRouter()

@router.get("/authentication", tags=["users"])
async def get_students():
    students = list_Serial_user(users.find())
    return students


@router.post("/authentication", tags=["users"])
async def insert_student(student: USERS):
    users.insert_one(dict(student))
    return 'true'

