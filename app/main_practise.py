
from fastapi import FastAPI,  HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import Request
app  =  FastAPI()
templates  =  Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "name": "Vikash"
        }
    )


@app.get("/home")
async def list_user():
    return {"message":"welcome to home"}

@app.get("/about")
async def about():
    return {"message": "about the page"}

@app.get("/contact")
async def contact():
    return {
        "email":"vikash.kumar979@gmail.com",
        "name":"vikash"
    }

@app.get("/student/{student_id}")
async def student_detail(student_id: int):
     return {
        "student_id": student_id
    }


@app.get("/products")
async def page_count(page:int =1):
    return {"page":page}

@app.get("/products/{page}")
async def page_count(page:int =1):
    return {"page":page}

#===========================================
    #Multiple Default Values
    #http://127.0.0.1:8000/product_items
    #or hhttp://127.0.0.1:8000/product_items/?page=2&limit=20
#==========================================
@app.get("/product_items")
async def product_list(page:int =1 , limit:int = 10):
    return {
        "page": page,
        "limit": limit
    }

#================================================
    #Optional Query Parameter
    #http://127.0.0.1:8000/search?name=python
###############################################
from typing import Optional
@app.get("/search")
async def search_option(name:Optional[str]=None):
    return {"name": name}


#==============================================
    #Real Project Example (Pagination)
###########################################

@app.get("/employees")
async def employees(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "start_index": start,
        "end_index": end
    }

#===================================================
    #Path Parameter और Query Parameter एक साथ भी हो सकते हैं।
    #http://127.0.0.1:8000/students/100?course=java
#================================================
@app.get("/students/{student_id}")
async def student(student_id: int, course: str = "Python"):
    return {
        "student_id": student_id,
        "course": course
    }

##############################################
    #Professional Validation using pydantic
###############################################
from pydantic import BaseModel,Field, EmailStr

class Student(BaseModel):
    name: str
    email: str
    age: int


@app.post("/student_created")
async def create_student(student: Student):
    print(type(student))
    data = student.model_dump()

    print(type(data))

    return {
        "message": "Student created successfully",
        "student": data
    }

###################################################
#अब Validation थोड़ा Powerful बनाते हैं
####################################################

class Student_Record(BaseModel):
    name : str =  Field(min_length=9, max_length=50)
    age : int  =  Field(ge=18, le=60)
    email: str

##########################################################
#Nested Pydantic Models
###########################################################
class Address(BaseModel):
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    pincode: str = Field(
        ...,
        pattern=r"^[1-9][0-9]{5}$",
        description="6 digit Indian PIN code"
    )


# -----------------------------
# Main Model
# -----------------------------
class Student_Address(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=5, le=100)
    email: str = Field(..., min_length=5)
    course: str = Field(..., min_length=2)
    address: Address

# ==========================================
# Temporary Database
# ==========================================

students_db = {}
@app.post("/students_address/{student_id}", response_model=Student_Address)
def create_student_address(student_id: int, student: Student_Address):

    if student_id in students_db:
        raise HTTPException(
            status_code=409,
            detail="Student already exists"
        )

    students_db[student_id] = student

    return student

# ==========================================
# GET - Single Student
# ==========================================

@app.get(
    "/students_address/{student_id}",
    response_model=Student
)
def get_student(student_id: int):

    student = students_db.get(student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

# ==========================================
# GET - All Students / Filter
#/students_address?course=Python
# ==========================================

@app.get("/students_address")
def get_students(
    course: str | None = Query(
        default=None,
        min_length=2
    )
):

    if course:

        return [
            student
            for student in students_db.values()
            if student.course.lower() == course.lower()
        ]

    return list(students_db.values())

#########################################################
# Best practise Request और Response के लिए अलग-अलग models रखना अच्छा practice है।
###############################################################

class Address_student(BaseModel):
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    pincode: str = Field(..., pattern=r"^[1-9][0-9]{5}$")


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=3)
    age: int = Field(..., ge=5, le=100)
    email: EmailStr
    course: str
    address: Address_student


class StudentResponse(BaseModel):
    student_id: int
    name: str
    age: int
    email: EmailStr
    course: str
    address: Address_student

class StudentUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    age: int = Field(
        ...,
        ge=5,
        le=100
    )

    email: EmailStr

    course: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    address: Address_student


# =========================================================
# 5. POST - Create Student
# =========================================================

@app.post(
    "/students_fetch/{student_id}",
    response_model=StudentResponse,
    status_code=201,
    summary="Create a student"
)
def create_student(
    student_id: int,
    student: StudentCreate
):

    # Check duplicate student
    if student_id in students_db:

        raise HTTPException(
            status_code=409,
            detail="Student already exists"
        )

    # Create response object
    new_student = StudentResponse(
        student_id=student_id,
        name=student.name,
        age=student.age,
        email=student.email,
        course=student.course,
        address=student.address
    )

    # Save in database
    students_db[student_id] = new_student

    return new_student


# =========================================================
# 6. GET - Get Student By ID
# =========================================================

@app.get(
    "/students_fetch/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID"
)
def get_student(student_id: int):

    student = students_db.get(student_id)

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =========================================================
# 7. GET - Get All Students
# =========================================================

@app.get(
    "/students_fetch",
    response_model=list[StudentResponse],
    summary="Get all students"
)
def get_students(
    course: str | None = Query(
        default=None,
        min_length=2,
        description="Filter students by course"
    )
):

    # If course filter is provided
    if course:

        return [
            student
            for student in students_db.values()
            if student.course.lower() == course.lower()
        ]

    # Otherwise return all students
    return list(students_db.values())

# -------------------------
# Temporary Database
# -------------------------

students = {
    1: {
        "student_id": 1,
        "name": "Rahul",
        "age": 25,
        "email": "rahul@gmail.com",
        "course": "Python",
        "address": {
            "city": "Noida",
            "state": "Uttar Pradesh",
            "pincode": "201301"
        }
    },

    2: {
        "student_id": 2,
        "name": "Amit",
        "age": 28,
        "email": "amit@gmail.com",
        "course": "FastAPI",
        "address": {
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001"
        }
    }
}

##############################################################
#8 Update Student
##############################################################

@app.put(
    "/students_fetch/{student_id}",
    response_model=StudentResponse
)
async def update_student(
    student_id: int,
    student: StudentUpdate
):
    existing_student = students.get(student_id)

    # Check student exists
    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Create updated student
    updated_student = StudentResponse(
        student_id=student_id,
        name=student.name,
        age=student.age,
        email=student.email,
        course=student.course,
        address=student.address
    )

    # Update database
    students_db[student_id] = updated_student

    return updated_student

# -------------------------
# DELETE
# -------------------------

@app.delete("/students_fetch/{student_id}")
async def delete_student(student_id: int):

    student = students.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully"
    }
