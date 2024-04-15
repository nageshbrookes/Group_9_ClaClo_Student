from pydantic import BaseModel

class Users(BaseModel):
    name: str
    email: str
    password: str

class certification():
    certificationID: str
    description: str

class Student_Profile(BaseModel):
    fullName: str
    image: str
    studentId: str
    gender: str
    degree: str
    certificate: list[dict]

class Optional_Courses(BaseModel):
    programId: str
    courseId: str
    courseName: str
    courseDiscription: str
    courseInstructor: str
