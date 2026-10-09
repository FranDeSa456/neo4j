from fastapi import APIRouter, HTTPException

import db
from models import CourseIn

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("")
def list_courses():
    return db.list_courses()

@router.post("", status_code=201)
def create_course(payload: CourseIn):
    if db.get_course(payload.name) is not None:
        raise HTTPException(status_code=409, detail="Course already exists")
    db.create_course(payload.name, payload.hours)
    return {"name": payload.name, "hours": payload.hours}

@router.delete("/{name}", status_code=204)
def delete_course(name: str):
    if db.delete_course(name) == 0:
        raise HTTPException(status_code=404, detail="Course not found")

@router.get("/{course}/students")
def students_of_course(course: str):
    return db.students_of_course(course)

@router.post("/{course}/students/{name}", status_code=201)
def enroll_student(course: str, name: str):
    status = db.enroll_student(name, course)
    if status == "not_found":
        raise HTTPException(status_code=404, detail="Student or course not found")
    if status == "exists":
        raise HTTPException(status_code=409, detail="Student already enrolled in course")
    return {"student": name, "course": course}

@router.delete("/{course}/students/{name}", status_code=204)
def unenroll_student(course: str, name: str):
    if db.unenroll_student(name, course) == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
