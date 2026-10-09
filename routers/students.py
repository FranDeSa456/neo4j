from fastapi import APIRouter, HTTPException

import db
from models import StudentIn

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("")
def list_students():
    return db.list_students()

@router.get("/{name}")
def get_student(name: str):
    student = db.get_student(name)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("", status_code=201)
def create_student(payload: StudentIn):
    if db.get_student(payload.name) is not None:
        raise HTTPException(status_code=409, detail="Student already exists")
    db.create_student(payload.name, payload.age)
    return {"name": payload.name, "age": payload.age}

@router.delete("/{name}", status_code=204)
def delete_student(name: str):
    if db.delete_student(name) == 0:
        raise HTTPException(status_code=404, detail="Student not found")
