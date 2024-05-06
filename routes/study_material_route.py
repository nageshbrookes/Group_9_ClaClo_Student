from fastapi import APIRouter, HTTPException,  Response,Depends
from config.database import teacher_db
from bson import ObjectId
from datetime import datetime
from gridfs import GridFS
import mimetypes
from typing import Annotated
from routes.authentication import get_current_user
from config.database import class_collection

studyMaterialRouter = APIRouter()
fs = GridFS(teacher_db)

userdependancy = Annotated[dict, Depends(get_current_user)]

@studyMaterialRouter.get("/get-teaching-modules/{student_email}", tags=["Teaching Material"])
async def get_module_info(user: userdependancy, student_email: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')
    classes = class_collection.find({"student.email": student_email})

    enrolledCourses = []
    for file_info in classes:
            enrolledCourses.append({ 'module_name': file_info["module_name"], 'id': str(file_info["_id"])})
    if len(enrolledCourses) == 0:
        raise HTTPException(status_code=404, detail='You are not enrolled to any course,Please contact your Module Leader')
    
    return enrolledCourses



@studyMaterialRouter.get("/get-teaching-material/{class_id}",  tags=["Teaching Material"])
async def get_teaching_material(user: userdependancy, class_id: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')
    
    try:
        teaching_material = teacher_db.studymaterial_collection.find({'class_id': class_id})
    except:
        raise HTTPException(status_code=200, details='Data not found')

    study_materials = []
    for study_material in teaching_material:
        class_id = str(study_material["class_id"])
        topic = study_material["topic"]
        file_id = study_material["file_id"]
        upload_date = study_material["upload_date"]
        
        study_materials.append({
            "Study Matrial Id": str(study_material["_id"]),
            "Document Name": topic,
            "Uploading Time": upload_date
        })
    
    return study_materials


@studyMaterialRouter.get("/download-teaching-material/{class_id}/{study_material_id}",  tags=["Teaching Material"])
async def download_study_material(user: userdependancy, class_id: str , study_material_id: str):
    if user is None:
        raise HTTPException(status_code=401, details='Authentication failed')

    try:
        # Verify if class exists
        class_doc = teacher_db.class_collection.find_one({"_id": ObjectId(class_id)})
        if class_doc is None:
            raise HTTPException(status_code=404, detail="Class not found")

        # Verify if study material exists and belongs to the specified class
        study_material = teacher_db.studymaterial_collection.find_one({"_id": ObjectId(study_material_id), "class_id": class_id})
        if study_material is None:
            raise HTTPException(status_code=404, detail="Study material not found for this class")

        # Retrieve file from GridFS using the file ID stored in the study material
        file_info = fs.get(ObjectId(study_material["file_id"]))
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
        raise HTTPException(status_code=500, detail="Failed to download study material")


