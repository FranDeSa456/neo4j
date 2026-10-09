import os
from contextlib import asynccontextmanager

import neo4j
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import db


class StudentIn(BaseModel):
    name: str
    age: int

class CourseIn(BaseModel):
    name: str
    hours: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = db.get_driver()
    driver.verify_connectivity()
    print("Connected to Neo4j!")
    yield
    driver.close()

app = FastAPI(title="neo4j-exercise", lifespan=lifespan)

# Routes

@app.get("/students")
def list_students():
    return db.list_students()

@app.get("/students/{name}")
def get_student(name: str):
    student = db.get_student(name)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students", status_code=201)
def create_student(payload: StudentIn):
    if db.get_student(payload.name) is not None:
        raise HTTPException(status_code=409, detail="Student already exists")
    db.create_student(payload.name, payload.age)
    return {"name": payload.name, "age": payload.age}

@app.delete("/students/{name}", status_code=204)
def delete_student(name: str):
    if db.delete_student(name) == 0:
        raise HTTPException(status_code=404, detail="Student not found")

@app.get("/courses")
def list_courses():
    return db.list_courses()

@app.post("/courses", status_code=201)
def create_course(payload: CourseIn):
    if db.get_course(payload.name) is not None:
        raise HTTPException(status_code=409, detail="Course already exists")
    db.create_course(payload.name, payload.hours)
    return {"name": payload.name, "hours": payload.hours}

@app.get("/courses/{course}/students")
def students_of_course(course: str):
    return db.students_of_course(course)

@app.delete("/courses/{name}", status_code=204)
def delete_course(name: str):
    if db.delete_course(name) == 0:
        raise HTTPException(status_code=404, detail="Course not found")

@app.post("/courses/{course}/students/{name}", status_code=201)
def enroll_student(course: str, name: str):
    status = db.enroll_student(name, course)
    if status == "not_found":
        raise HTTPException(status_code=404, detail="Student or course not found")
    if status == "exists":
        raise HTTPException(status_code=409, detail="Student already enrolled in course")
    return {"student": name, "course": course}

@app.delete("/courses/{course}/students/{name}", status_code=204)
def unenroll_student(course: str, name: str):
    if db.unenroll_student(name, course) == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")