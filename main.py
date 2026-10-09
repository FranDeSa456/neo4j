import os
from contextlib import asynccontextmanager

import neo4j
from fastapi import FastAPI

import db
from routers import courses, students


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = db.get_driver()
    driver.verify_connectivity()
    print("Connected to Neo4j!")
    yield
    driver.close()

app = FastAPI(title="neo4j-exercise", lifespan=lifespan)

app.include_router(students.router)
app.include_router(courses.router)
