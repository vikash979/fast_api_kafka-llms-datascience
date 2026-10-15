from data.students import students

from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

#####################################################
# Without async  service 
#######################################################################
def create_student_service(student: StudentCreate):

    new_id = max(students.keys(), default=0) + 1

    new_student = {
        "student_id": new_id,
        "name": student.name,
        "age": student.age,
        "email": student.email,
        "course": student.course,
        "address": student.address.model_dump()
    }

    students[new_id] = new_student

    return new_student


def get_student_service(student_id: int):

    student = students.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


#########################################################
##Update student service function
#########################################################
def update_student_service(
    student_id: int,
    student: StudentUpdate
):

    existing_student = students.get(student_id)

    if existing_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student.name is not None:
        existing_student["name"] = student.name

    if student.age is not None:
        existing_student["age"] = student.age

    if student.email is not None:
        existing_student["email"] = student.email

    if student.course is not None:
        existing_student["course"] = student.course

    if student.address is not None:
        existing_student["address"] = student.address.model_dump()

    return existing_student

#############################################################################
# Delete student service function
#############################################################################
def delete_student_service(student_id: int):

    student = students.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully"
    }


#############################################################################
##############Async  Service 
#############################################################################

async def create_student_service_async(student: StudentCreate):

    new_id = max(students.keys(), default=0) + 1

    new_student = {
        "student_id": new_id,
        "name": student.name,
        "age": student.age,
        "email": student.email,
        "course": student.course,
        "address": student.address.model_dump()
    }

    students[new_id] = new_student

    return new_student


#####################################################################
# async update service function
###############################################################
async def update_student_service_async(
    student_id: int,
    student: StudentUpdate
):

    existing_student = students.get(student_id)

    if existing_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student.name is not None:
        existing_student["name"] = student.name

    if student.age is not None:
        existing_student["age"] = student.age

    if student.email is not None:
        existing_student["email"] = student.email

    if student.course is not None:
        existing_student["course"] = student.course

    if student.address is not None:
        existing_student["address"] = student.address.model_dump()

    return existing_student


######################################################################################
###async delete service function
######################################################################################
async def delete_student_service_async(student_id: int):

    student = students.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully"
    }