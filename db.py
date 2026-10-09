import os

from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

DATABASE = "neo4j"

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(URI, auth=AUTH)
    return _driver


def list_students():
    records, _, _ = get_driver().execute_query(
        """
        MATCH (s:Student)
        RETURN s.name AS name, s.age AS age
        ORDER BY s.name
        """,
        database_=DATABASE,
    )
    return [record.data() for record in records]


def get_student(name):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (s:Student {name: $name})
        RETURN s.name AS name, s.age AS age
        """,
        name=name,
        database_=DATABASE,
    )
    return records[0].data() if records else None


def create_student(name, age):
    get_driver().execute_query(
        "CREATE (:Student {name: $name, age: $age})",
        name=name,
        age=age,
        database_=DATABASE,
    )


def delete_student(name):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (s:Student {name: $name})
        DETACH DELETE s
        RETURN count(*) AS deleted
        """,
        name=name,
        database_=DATABASE,
    )
    return records[0]["deleted"] if records else 0


def list_courses():
    records, _, _ = get_driver().execute_query(
        """
        MATCH (c:Course)
        RETURN c.name AS name, c.hours AS hours
        ORDER BY c.name
        """,
        database_=DATABASE,
    )
    return [record.data() for record in records]


def get_course(name):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (c:Course {name: $name})
        RETURN c.name AS name, c.hours AS hours
        """,
        name=name,
        database_=DATABASE,
    )
    return records[0].data() if records else None


def create_course(name, hours):
    get_driver().execute_query(
        "CREATE (:Course {name: $name, hours: $hours})",
        name=name,
        hours=hours,
        database_=DATABASE,
    )


def delete_course(name):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (c:Course {name: $name})
        DETACH DELETE c
        RETURN count(*) AS deleted
        """,
        name=name,
        database_=DATABASE,
    )
    return records[0]["deleted"] if records else 0


def students_of_course(course):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (:Course {name: $course})<-[:ENROLLED_IN]-(s:Student)
        RETURN s.name AS name, s.age AS age
        ORDER BY s.name
        """,
        course=course,
        database_=DATABASE,
    )
    return [record.data() for record in records]


def enroll_student(student, course):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (s:Student {name: $student})
        MATCH (c:Course {name: $course})
        OPTIONAL MATCH (s)-[old:ENROLLED_IN]->(c)
        MERGE (s)-[r:ENROLLED_IN]->(c)
        RETURN old IS NOT NULL AS already_enrolled
        """,
        student=student,
        course=course,
        database_=DATABASE,
    )
    if not records:
        return "not_found"
    if records[0]["already_enrolled"]:
        return "exists"
    return "created"


def unenroll_student(student, course):
    records, _, _ = get_driver().execute_query(
        """
        MATCH (:Student {name: $student})-[r:ENROLLED_IN]->(:Course {name: $course})
        DELETE r
        RETURN count(*) AS deleted
        """,
        student=student,
        course=course,
        database_=DATABASE,
    )
    return records[0]["deleted"] if records else 0
