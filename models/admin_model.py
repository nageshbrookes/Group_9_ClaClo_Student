from pydantic import BaseModel


# Module info represent Modules of the perticular courses(Acs)
class MODULE_INFO_MODEL(BaseModel):
    moduleId: str
    moduleName: str
    moduleClassesTiming: list
    moduleLeader: str
    moduleLeaderId: str
    moduleDescription: str
    moduleDuration: str
    moduleDepartment: str
    IscourseOptional: bool