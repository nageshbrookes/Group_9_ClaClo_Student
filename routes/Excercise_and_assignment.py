from fastapi import APIRouter, UploadFile, File, HTTPException
from config.database import teacher_db
from gridfs import GridFS
from bson import ObjectId
from models.model import EXCERCISE_AND_ASSIGNMENT
from config.database import ExcerciseAndAssignment, class_collection


fs = GridFS(teacher_db)

assignmentRouter = APIRouter()

@assignmentRouter.post("/uploadExcerciseAndAssignment/upload/",  tags=["Excercise and Assignement"])
async def uploadExcerciseAndAssignment(studentId: str,
    classId: str,
    assignmentName: str, assignmentFile: UploadFile = File(...)):
    # Check if class exists
    class_doc = class_collection.find_one({"_id": ObjectId(classId)})
    if not class_doc:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Save file to GridFS
    file_id = fs.put(assignmentFile.file, filename=assignmentFile.filename)
    
    # Save metadata to MongoDB
    dataToSave = {
        "class_id": classId,
        "assignmentName": assignmentName,
        "file_id": str(file_id),
        "studentId": studentId
    }
    
    # Insert metadata into study_materials collection
    ExcerciseAndAssignment.insert_one(dataToSave)
    
    return {"message": "Study material uploaded successfully"}



    