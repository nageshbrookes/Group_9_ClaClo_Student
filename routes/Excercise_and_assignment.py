from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import Field
from config.database import teacher_db
from gridfs import GridFS
from bson import ObjectId
from config.database import ExcerciseAndAssignment, class_collection
from typing import Annotated
from routes.authentication import get_current_user
from datetime import datetime

fs = GridFS(teacher_db)

assignmentRouter = APIRouter()
userdependancy = Annotated[dict, Depends(get_current_user)]


@assignmentRouter.get("/fetch-module-info/{student_email}", tags=["Excercise and Assignement"])
async def get_module_info(user: userdependancy, student_email: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')
    classes = class_collection.find({"student.email": student_email})

    enrolledCourses = []
    for file_info in classes:
            enrolledCourses.append(file_info["module_name"])
    if len(enrolledCourses) == 0:
        raise HTTPException(status_code=404, detail='You are not enrolled to any course,Please contact your Module Leader')
    
    return enrolledCourses


@assignmentRouter.post("module/upload-excercise/",  tags=["Excercise and Assignement"])
async def upload_excercise_and_assignment(user: userdependancy, student_Id:str, class_id:str, excercise_Id:str, topic_name: str,
     assignmentFile: UploadFile = File(...)):
    
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')

    # Check if class exists
    print('asdf', class_id)
    try:    
        class_doc = class_collection.find_one({"_id": ObjectId(class_id)})
    except:
         raise HTTPException(status_code=400, detail='Not a Valid ID')
    if not class_doc:
        raise HTTPException(status_code=400, detail="Class not found")
    
    # Save file to GridFS
    file_id = fs.put(assignmentFile.file, filename=assignmentFile.filename)
    
    # Save metadata to MongoDB
    dataToSave = {
    'student_Id': student_Id,
    'topic_name': topic_name,
    'excercise_Id': excercise_Id,
    "class_id": class_id,
    "file_id": str(file_id),
    'upload_date': datetime.utcnow()
    }
    
    # Insert metadata into study_materials collection
    ExcerciseAndAssignment.insert_one(dataToSave)
    
    return {"message": "Study material uploaded successfully"}



    