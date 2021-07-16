from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy.orm import backref, joinedload
from sqlalchemy.orm import relationship

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:7028898230@localhost/student"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# student_class = db.Table(
#   "student_class",
# db.Column("student_id", db.Integer, db.ForeignKey("student.student_id")),
#  db.Column("class_id", db.Integer, db.ForeignKey("class.class_id")),
# )


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # mapped_Table = db.relationship(
    #    "Class",
    #    secondary="Student_class",
    #    backref=db.backref("Student", lazy="dynamic"),
    # )

    def __init__(self, name):
        self.name = name

        classes = relationship("Class", secondary="student_class")


@app.route("/student", methods=["GET"])
def get_student():
    result = db.engine.execute("select * from student")
    response = []
    for row in result:
        response.append({"student_id": row["student_id"], "name": row["name"]})
    response = {"student": response}
    return response


@app.route("/student", methods=["POST"])
def create_student():
    print(request.json)
    student_data = Student(request.json["name"])
    db.session.add(student_data)
    db.session.commit()
    return {"status": "Sucess"}


# ======================== Class class ==============================


class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)

    def _init_(self, course_name):
        self.course_name = course_name

        student = relationship("Student", secondary="student_class")


@app.route("/class", methods=["GET"])
def get_class():
    result = db.engine.execute("select * from class")
    response = []
    for row in result:
        response.append(
            {"class_id": row["class_id"], "course_name": row["course_name"]}
        )
    response = {"class": response}
    return response


@app.route("/class", methods=["POST"])
def create_class():
    print(request.json)
    class_data = Class(request.json["course_name"])
    db.session.add(class_data)
    db.session.commit()
    return {"status": "Sucess"}


# ==================== student_class Table ===========================


class Student_class(db.Model):
    _tablename_ = "student_class"
    student_class_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"))
    classes = relationship(
        "Class", backref=backref("student_class", cascade="all, delete-orphan")
    )
    student = relationship(
        "Student", backref=backref("student_class", cascade="all, delete-orphan")
    )


if __name__ == "__main__":
    app.run(host="localhost", port="8000")
