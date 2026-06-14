from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "mysql-service")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root123")
DB_NAME = os.getenv("DB_NAME", "studentdb")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/init", methods=["GET"])
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            year_of_join INT NOT NULL,
            department VARCHAR(100) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "students table created"})


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():
    data = request.json

    name = data.get("name")
    year_of_join = data.get("year_of_join")
    department = data.get("department")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, year_of_join, department) VALUES (%s, %s, %s)",
        (name, year_of_join, department)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "student added successfully"}), 201


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "student deleted successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
