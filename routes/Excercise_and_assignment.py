import mimetypes
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Depends
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
    # authentication check
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')
    
    try: 
        classes = class_collection.find({"student.email": student_email})
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail="Failed to download answer")

    enrolledCourses = []
    for file_info in classes:
            enrolledCourses.append(file_info["module_name"])
    if len(enrolledCourses) == 0:
        raise HTTPException(status_code=404, detail='You are not enrolled to any course,Please contact your Module Leader')
    
    return enrolledCourses


@assignmentRouter.post("/upload-excercise/",  tags=["Excercise and Assignement"])
async def upload_excercise_and_assignment(user: userdependancy, student_Id:str, class_id:str, excercise_Id:str, topic_name: str,  
                                          assignmentFile: UploadFile = File(...) ):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')

    # Check if class exists
    try:    
        class_doc = class_collection.find_one({"_id": ObjectId(class_id)})
    except:
         raise HTTPException(status_code=400, detail='Not a Valid ID')
    if not class_doc:     
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Save file to GridFS
    print(assignmentFile.content_type)
    if assignmentFile.content_type in ('application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg'):
        print('insdf')
        file_id = fs.put(assignmentFile.file, filename=assignmentFile.filename)
    else:
        # sent unsupported media type error
        raise HTTPException(status_code=415, detail='File formate is not supported. Please use PDF,DOC and png formate only') 
    
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


@assignmentRouter.get("/get-assignments/", tags=["Excercise and Assignement"])
async def get_assignment(user: userdependancy):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')

    assignments = []
    for answer in ExcerciseAndAssignment.find():
        student_id = answer["student_Id"]
        topic_name = answer["topic_name"]
        excercise_id = answer["excercise_Id"]
        class_id = answer["class_id"]
        file_id = answer["file_id"]
        upload_date = answer["upload_date"]

        
        assignments.append({
            "answer_id": str(answer[ "_id" ]),  
            "student_id": student_id,
            "topic_name": topic_name, 
            "excercise_id": excercise_id,
            "class_id": class_id,
            "file_id": file_id,
            "upload_date": upload_date

        })
        
    return assignments
    

@assignmentRouter.get("/download-assignment/{student_id}/{exercise_id}", tags=["Excercise and Assignement"])
async def download_assignment(user: userdependancy, student_id: str,
                                    exercise_id: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')
    
    try:
        # Check if the exercise exists
        exercise = teacher_db.exercise_collection.find_one({"_id": ObjectId(exercise_id)})
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        # Check if the student exists
        student = teacher_db.student_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Retrieve the answer for the given exercise and student
        answer = ExcerciseAndAssignment.find_one({"excercise_Id": exercise_id, "student_Id": student_id})
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found for this student and exercise")

        # Retrieve file from GridFS using the file ID stored in the study material
        file_info = fs.get(ObjectId(answer["file_id"]))
        if file_info is None:
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media type based on file extension
        filename = file_info.filename
        media_type, _ = mimetypes.guess_type(filename)
        if media_type is None:
                media_type = "application/octet-stream"

        # Read file content into memory
        file_content = file_info.read()

        # Return file content as response
        return Response(content=file_content, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException:

        # Re-raise HTTPException to return specific error responses
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail="Failed to download answer")