from fastapi import APIRouter, HTTPException, Request, status

from services.student import (
    create_student_service, delete_student_service_async, get_student_service, update_student_service,delete_student_service,
    create_student_service_async, 
    update_student_service_async,
    delete_student_service)
from data.students import students
from kafka_client.producer import SyncKafkaProducer,AsyncKafkaProducer


from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)


router = APIRouter(
    prefix="/students_fetch",
    tags=["Students"]
)


# =========================
# GET ALL STUDENTS
# =========================

@router.get(
    "",
    response_model=list[StudentResponse]

)
async def get_students():

    return list(students.values())


# =========================
# GET STUDENT BY ID
# =========================

@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID"
)
async def get_student(student_id: int):
    return get_student_service(student_id)


# =========================
# CREATE STUDENT without async service function 
# =========================

@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student"
)
async def create_student(student: StudentCreate, request: Request,):
    new_student = create_student_service(student)

    request.app.state.sync_kafka_producer.publish_student_event(
        new_student
    )

    return create_student_service(student)




# =========================
# UPDATE STUDENT without async
# =========================

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
async def update_student(
    student_id: int,
    student: StudentUpdate
):
    return update_student_service(student_id, student)


# =========================
# DELETE STUDENT without async 
# =========================

@router.delete("/{student_id}")
async def delete_student(student_id: int):
    return delete_student_service(student_id)


###################################################################################
#### Async service function for creating a student
###################################################################################

@router.post(
    "/async",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student asynchronously"
)
async def create_student_async(student: StudentCreate, request: Request,):
    new_student = await create_student_service_async(student)

    await request.app.state.async_kafka_producer.publish_student_event(
        new_student
    )


    return new_student



##################################################################################
############## Async Update student service function
##################################################################################
@router.put(
    "/async/{student_id}",
    response_model=StudentResponse,
    summary="Update a student asynchronously"
)
async def update_student_async(
    student_id: int,
    student: StudentUpdate
):

    return await update_student_service_async(
        student_id,
        student
    )

#########################################################################
#### Async Delete student service function
#########################################################################
@router.delete(
    "/async/{student_id}",
    summary="Delete a student asynchronously"
)
async def delete_student_async(student_id: int):
    
    return await delete_student_service_async(student_id)