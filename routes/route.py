from fastapi import APIRouter
from models.model import Users
from config.database import users
from schema.schemas import list_Serial_user


router = APIRouter()

@router.get("/authentication", tags=["users"])
async def get_students():
    students = list_Serial_user(users.find())
    return students


@router.post("/authentication", tags=["users"])
async def insert_student(student: Users):
    users.insert_one(dict(student))
    return 'true'

# @router.post("/file")
# async def fileUpload(file: UploadFile):
#     if file.content_type != ".png" | file.content_type != ".jpeg":
#         raise HTTPException(400, detail='invalid document type')
#     else :
#         data = json.loads(file.file.read())
#     content
