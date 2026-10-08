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


def _create_student(tx, name, age):
    tx.run(
        "CREATE (:Student {name: $name, age: $age})",
        name=name,
        age=age,
    )


def create_student(name, age):
    with get_driver().session(database=DATABASE) as session:
        session.execute_write(_create_student, name, age)


def _delete_student(tx, name):
    result = tx.run(
        """
        MATCH (s:Student {name: $name})
        DETACH DELETE s
        RETURN count(*) AS deleted
        """,
        name=name,
    )
    return result.single()["deleted"]


def delete_student(name):
    with get_driver().session(database=DATABASE) as session:
        return session.execute_write(_delete_student, name)


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
