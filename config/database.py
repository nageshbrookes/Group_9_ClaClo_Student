from pymongo import MongoClient
import certifi
ca = certifi.where()

# uri = "mongodb+srv://19261357:test1234@cluster0.4wz4fbb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
# # uri = "mongodb+srv://19274214:COMP7033@comp7033.og3ddze.mongodb.net/?retryWrites=true&w=majority&appName=COMP7033"
# client = MongoClient(uri, tlsCAFile=ca)

TeacherDatabaseURI= "mongodb+srv://19274214:COMP7033@comp7033.og3ddze.mongodb.net/?retryWrites=true&w=majority&appName=COMP7033"
teacherClient = MongoClient(TeacherDatabaseURI, tlsCAFile=ca)
teacher_db = teacherClient.teacher_db

db = teacherClient.student_db

users = db["users"]
student_profile = db["student_profile"]
optional_course = db["optional_courses"]


ExcerciseAndAssignment = teacher_db["excercise_and_assignment"]
teacher_studymaterial_collection = teacher_db["studymaterial_collection"]
class_collection = teacher_db["class_collection"]
