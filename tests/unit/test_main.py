import pytest
from fastapi.testclient import TestClient

from app.main_practise import app, students_db


@pytest.fixture()
def client():
    students_db.clear()
    with TestClient(app) as test_client:
        yield test_client
    students_db.clear()


def student_payload():
    return {
        "name": "Anita Sharma",
        "age": 28,
        "email": "anita@example.com",
        "course": "Python",
        "address": {
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001",
        },
    }


def test_create_student_returns_created_student(client):
    response = client.post("/students_fetch/1", json=student_payload())

    assert response.status_code == 201
    assert response.json() == {
        "student_id": 1,
        **student_payload(),
    }


def test_create_student_rejects_duplicate_id(client):
    payload = student_payload()
    client.post("/students_fetch/1", json=payload)

    response = client.post("/students_fetch/1", json=payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Student already exists"}


def test_get_student_returns_not_found_for_unknown_id(client):
    response = client.get("/students_fetch/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_list_students_filters_by_course_case_insensitively(client):
    python_student = student_payload()
    java_student = {
        **student_payload(),
        "name": "Rahul Verma",
        "email": "rahul@example.com",
        "course": "Java",
    }
    client.post("/students_fetch/1", json=python_student)
    client.post("/students_fetch/2", json=java_student)

    response = client.get("/students_fetch", params={"course": "python"})

    assert response.status_code == 200
    assert response.json() == [{"student_id": 1, **python_student}]


def test_create_student_rejects_invalid_email(client):
    payload = {**student_payload(), "email": "not-an-email"}

    response = client.post("/students_fetch/1", json=payload)

    assert response.status_code == 422