def covert(students) -> dict:
    return {
        "id": str(students["_id"]), 
        "name": students["name"],
        "email": students["email"],
        "password": students["password"],
    }

def list_Serial_user(students) -> list:
    return [covert(student) for student in students]


def profile_conversion(profile) -> dict:
    return {
        "id": str(profile["_id"]), 
        "fullName": profile["fullName"],
        "image": profile["image"],
        "studentId": profile["studentId"],
        "gender": profile['gender'],
        'degree': profile['degree'],
        'certificate': profile['certificate']
    }

def list_Serial_profile(profiles) -> list:
    return [profile_conversion(profile) for profile in profiles]


def optional_course_conversion(optionalCourse) -> dict:
    return {
        "id": str(optionalCourse["_id"]),
        "programId": optionalCourse["programId"],
        "courseId": optionalCourse["courseId"],
        "courseName": optionalCourse["courseName"],
        "courseDiscription": optionalCourse["courseDiscription"],
        "courseInstructor": optionalCourse["courseInstructor"] 
    }

def list_Serial_optional_course(optionalCourses) -> list:
    return [optional_course_conversion(optionalCourse) for optionalCourse in optionalCourses]


def teaching_material_conversion(teachingMaterial) -> dict:
    return {
        "id": str(teachingMaterial["_id"]),
        "class_id": teachingMaterial["class_id"],
        "topic": teachingMaterial["topic"],
        "file_id": teachingMaterial["file_id"]
    }

def list_Serial_teaching_material(optionalCourses) -> list:
    return [teaching_material_conversion(optionalCourse) for optionalCourse in optionalCourses]