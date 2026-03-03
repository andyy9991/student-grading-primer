from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this
def _error(message:str , code: int = 404):
    return jsonify({"error": message}), code

def _parse_int(value, field_name: str):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an integer")    

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _error("Invalid JSON body")

    name = data.get("name")
    course = data.get("course")
    mark_raw = data.get("mark", 0) #edge case

    if not isinstance(name, str) or not name.strip():
        return _error("Missing or invalid 'name'")
    if not isinstance(course, str) or not course.strip():
        return _error("Missing or invalid 'course'")

    try:
        mark = _parse_int(mark_raw, "mark")
    except ValueError as e:
        return _error(str(e))

    if mark is None:
        return _error("Missing or invalid 'mark'")
    if mark < 0 or mark > 100:
        return _error("'mark' must be between 0 and 100")

    created = db.insert_student(name.strip(), course.strip(), mark)
    return jsonify(created), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _error("Invalid JSON body")

    name = data.get("name", None)
    course = data.get("course", None)
    mark_raw = data.get("mark", None)

    if name is not None and (not isinstance(name, str) or not name.strip()):
        return _error("Invalid 'name'")
    if course is not None and (not isinstance(course, str) or not course.strip()):
        return _error("Invalid 'course'")

    mark = None
    if mark_raw is not None:
        try:
            mark = _parse_int(mark_raw, "mark")
        except ValueError as e:
            return _error(str(e))
        if mark < 0 or mark > 100:
            return _error("'mark' must be between 0 and 100")

    updated = db.update_student(
        student_id,
        name=name.strip() if isinstance(name, str) else None,
        course=course.strip() if isinstance(course, str) else None,
        mark=mark,
    )
    if updated is None:
        return _error("Student not found")

    return jsonify(updated), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)
    if deleted is None:
        return _error("Student not found")
    return jsonify(deleted), 200


@app.route("/stats")
def get_stats():
    students = db.get_all_students()
    marks = [s["mark"] for s in students]

    if len(marks) == 0:
        return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
