from pydantic import BaseModel, Field

class USERS(BaseModel):
    name: str
    email: str
    password: str

class CERTIFICATION_MODEL():
    certificationId: str
    description: str

class MODULE_CLASSESS_TIMING(BaseModel):
    time: str
    day: str

class MODULE_INFO(BaseModel):
    moduleId: str
    moduleName: str
    moduleClassesTiming: list[MODULE_CLASSESS_TIMING]
    moduleLeaderName: str
    moduleLeaderId: str
    moduleDescription: str
    moduleDuration: str

class STUDENT_PROFILE(BaseModel):
    fullName: str
    image: str
    studentId: str
    gender: str
    degree: str
    programId: str
    programName: str
    certificates: list[dict]
    enrolledModules: list[MODULE_INFO]
    optionalModules: list[MODULE_INFO]



class OPTIONAL_MODULE_IN_PROGRAM(BaseModel):
    programId: str
    programName: str
    optionModules: list[MODULE_INFO]


class TEACHING_MATERIAL(BaseModel):   
    class_id: str
    topic: str
    file_id: str


class EXCERCISE_AND_ASSIGNMENT(BaseModel):
    excercises_id: str
    student_Id: str
    student_email: str
    excercises_name: str
    class_id: str



class CREATE_USER_REQUEST(BaseModel):
    studentId: str
    password: str
