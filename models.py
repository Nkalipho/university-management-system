# models.py
import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association tables
course_degrees = db.Table(
    'course_degrees',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('degree_id', db.Integer, db.ForeignKey('degree.id'))
)

student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class University(db.Model):
    __tablename__ = 'university'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    faculties = db.relationship('Faculty', backref='university', lazy=True)
    staff = db.relationship('StaffMember', backref='university', lazy=True)
    students = db.relationship('Student', backref='university', lazy=True)

    def __init__(self, name):
        self.name = name

    def add_staffmember(self, staffmember):
        if not isinstance(staffmember, StaffMember):
            raise TypeError("Must be a Staff object!")
        clean_name = staffmember.name.strip()
        if not clean_name[0].isalpha():
            raise ValueError("Staff name must start with a letter!")
        first_letter = clean_name[0].upper()
        random_digits = ''.join(str(random.randint(0,9)) for _ in range(4))
        staff_id = f"S25{first_letter}{random_digits}"
        staffmember.staff_id = staff_id 
        staffmember.university = self
        self.staff.append(staffmember)

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Must be a Student object!")
        
        if not student.faculty_id:
            raise ValueError("Student must be assigned to a faculty")
            
        if student.aps_points >= 28:
            clean_name = student.name.strip()
            if not clean_name[0].isalpha():
                raise ValueError("Student name must start with a letter!")
            first_letter = clean_name[0].upper()
            random_digits = ''.join(str(random.randint(0,9)) for _ in range(4))
            student.student_id = f"G25{first_letter}{random_digits}"
            student.admission_status = "Accepted"
            self.students.append(student)
            return True
        student.admission_status = "Rejected"
        return False

    def add_faculty(self, faculty):
        if not isinstance(faculty, Faculty):
            raise TypeError("Must be a Faculty object!")
        self.faculties.append(faculty)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dean = db.Column(db.String(255))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=True)
    
    departments = db.relationship('Department', back_populates='faculty')
    staff = db.relationship('StaffMember', backref='faculty', lazy=True)
    courses = db.relationship('Course', backref='faculty', lazy=True)
    degrees = db.relationship('Degree', back_populates='faculty', lazy=True)

    def __init__(self, name, dean):
        self.name = name
        self.dean = dean

    def add_degree(self, degree):
        if not isinstance(degree, Degree):
            raise TypeError("Must be degree object!")
        self.degrees.append(degree)

    def add_department(self, department):
        if not isinstance(department, Department):
            raise TypeError("Must be a department object!")
        self.departments.append(department)

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Correct column name
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    
    faculty = db.relationship('Faculty', back_populates='departments')
    staff = db.relationship('StaffMember', backref='department', lazy=True)
    courses = db.relationship('Course', backref='department', lazy=True)

    def __init__(self, name):
        self.name = name
        
class Degree(db.Model):
    __tablename__ = 'degree'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    requirements = db.Column(db.Text)
    
    faculty = db.relationship('Faculty', back_populates='degrees')
    courses = db.relationship(
        'Course',
        secondary=course_degrees,
        back_populates='degrees'
    )

class StaffMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    staff_id = db.Column(db.String(20), unique=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    def __init__(self, name, role):
        self.name = name
        self.role = role

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    aps_points = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.String(20), unique=True)
    admission_status = db.Column(db.String(20))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'))
    requirements = db.Column(db.Text)
    
    courses = db.relationship('Course', secondary=student_courses,
                            backref=db.backref('students_enrolled', lazy='dynamic'),
                            lazy='dynamic')
    degree = db.relationship('Degree', backref='students')
    faculty = db.relationship('Faculty', backref='students')

    def __init__(self, name, aps_points):
        self.name = name
        self.aps_points = aps_points

    def add_course(self, course):
        if not isinstance(course, Course):
            raise TypeError("Must be a course object!")
        if self.courses.filter_by(id=course.id).first() is not None:
            raise ValueError("Course already registered as one of your courses.")
        self.courses.append(course)

    def remove_course(self, course):
        if not isinstance(course, Course):
            raise TypeError("Must be a course object!")
        if self.courses.filter_by(id=course.id).first() is None:
            raise ValueError("Course is not registered as one of your courses.")
        self.courses.remove(course)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(100), nullable=False)
    max_capacity = db.Column(db.Integer, default=0)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    degrees = db.relationship('Degree', secondary='course_degrees', back_populates='courses')

    def __init__(self, course_name, course_code, max_capacity=0):
        self.course_name = course_name
        self.course_code = course_code
        self.max_capacity = max_capacity

    def set_department(self):
        """Automatically set department based on faculty"""
        if self.faculty.name == "Faculty of Engineering":
            self.department = Department.query.filter_by(
                name="Computer Science", 
                faculty_id=self.faculty.id
            ).first()
        elif self.faculty.name == "Faculty of Natural Sciences":
            self.department = Department.query.filter_by(
                name="Physics", 
                faculty_id=self.faculty.id
            ).first()
        elif self.faculty.name == "Faculty of Humanities":
            self.department = Department.query.filter_by(
                name="History", 
                faculty_id=self.faculty.id
            ).first()
        elif self.faculty.name == "Business School":
            self.department = Department.query.filter_by(
                name="Management", 
                faculty_id=self.faculty.id
            ).first()

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Must be a student object!")
        if self.students_enrolled.filter_by(id=student.id).first() is not None:
            return
        if self.students_enrolled.count() >= self.max_capacity:
            raise ValueError("Cannot add anymore students; the course is full.")
        self.students_enrolled.append(student)

    def remove_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Must be a student object!")
        if self.students_enrolled.filter_by(id=student.id).first() is None:
            raise ValueError("Student is not enrolled in Course!")
        self.students_enrolled.remove(student)