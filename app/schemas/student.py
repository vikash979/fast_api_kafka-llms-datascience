#################################################
#अब main.py में ये classes नहीं रहेंगी। hata unga jo main_practise.py में define kiya hai.
########################################
from pydantic import BaseModel, EmailStr


class Address_student(BaseModel):
    city: str
    state: str
    pincode: str


class StudentCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    course: str
    address: Address_student


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: EmailStr | None = None
    course: str | None = None
    address: Address_student | None = None


class StudentResponse(BaseModel):
    student_id: int
    name: str
    age: int
    email: EmailStr
    course: str
    address: Address_student