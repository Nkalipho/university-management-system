from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, University, Faculty, StaffMember, Department, Course, Student, Degree
from flask_migrate import Migrate
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

def create_sample_data():
    db.drop_all()
    db.create_all()

    uni = University(name="Cambridge Metropolitan University")
    db.session.add(uni)

    # ======================
    #  Engineering Faculty
    # ======================
    eng_faculty = Faculty(name="Faculty of Engineering", dean="Prof. Alice Johnson")
    uni.faculties.append(eng_faculty)
    db.session.add(eng_faculty)
    
    eng_departments = [
        Department(name="Computer Science"),
        Department(name="Electrical Engineering"),
        Department(name="Mechanical Engineering")
    ] 
    db.session.add_all(eng_departments)
    
    for dept in eng_departments:
        dept.faculty = eng_faculty
        
    eng_staff = [
        StaffMember(name="Dr. John Smith", role="Professor"),
        StaffMember(name="Dr. Emily Brown", role="Senior Lecturer")
    ]
    db.session.add_all(eng_staff)
    
    # Set departments and faculty for engineering staff
    eng_staff[0].department = eng_departments[0]
    eng_staff[0].faculty = eng_faculty
    eng_staff[1].department = eng_departments[1]
    eng_staff[1].faculty = eng_faculty

    cs_degree = Degree(
        name="BSc Computer Science",
        rank="Undergraduate",
        requirements="A-levels: Mathematics + two science subjects",
        faculty=eng_faculty
    )
    db.session.add(cs_degree)

    ee_degree = Degree(
        name="MEng Electrical Engineering",
        rank="Postgraduate",
        requirements="BEng in Electrical Engineering or related field",
        faculty=eng_faculty
    )
    db.session.add(ee_degree)

    mech_degree = Degree(
        name="BEng Mechanical Engineering",
        rank="Undergraduate",
        requirements="A-levels: Mathematics, Physics + one technical subject",
        faculty=eng_faculty
    )
    db.session.add(mech_degree)

    eng_courses = [
        Course(course_name="Introduction to Programming", course_code="CS101", max_capacity=100),
        Course(course_name="Circuit Analysis", course_code="EE201", max_capacity=80),
        Course(course_name="Thermodynamics", course_code="ME301", max_capacity=60),
        Course(course_name="Data Structures", course_code="CS202", max_capacity=75)
    ]
    db.session.add_all(eng_courses)
    
    # Disable autoflush temporarily
    original_autoflush = db.session.autoflush
    db.session.autoflush = False
    
    for course in eng_courses:
        course.faculty = eng_faculty
        course.set_department()
        course.degrees.extend([cs_degree, ee_degree, mech_degree])
    
    # Restore original autoflush setting
    db.session.autoflush = original_autoflush

    # ======================
    #  Natural Sciences Faculty
    # ======================
    sci_faculty = Faculty(name="Faculty of Natural Sciences", dean="Dr. Brian Miller")
    uni.faculties.append(sci_faculty)
    db.session.add(sci_faculty)
    
    sci_departments = [
        Department(name="Physics"),
        Department(name="Chemistry")
    ]
    db.session.add_all(sci_departments)
    for dept in sci_departments:
        dept.faculty = sci_faculty

    sci_staff = [
        StaffMember(name="Dr. Rachel Green", role="Professor"),
        StaffMember(name="Dr. David Black", role="Researcher")
    ]
    db.session.add_all(sci_staff)
    
    # Set departments and faculty for science staff
    sci_staff[0].department = sci_departments[0]
    sci_staff[0].faculty = sci_faculty
    sci_staff[1].department = sci_departments[1]
    sci_staff[1].faculty = sci_faculty

    physics_degree = Degree(
        name="MSc Theoretical Physics",
        rank="Postgraduate",
        requirements="BSc in Physics or related field",
        faculty=sci_faculty
    )
    db.session.add(physics_degree)

    chemistry_degree = Degree(
        name="BSc Chemistry",
        rank="Undergraduate",
        requirements="A-levels: Chemistry + two science subjects",
        faculty=sci_faculty
    )
    db.session.add(chemistry_degree)

    sci_courses = [
        Course(course_name="Quantum Mechanics", course_code="PHY401", max_capacity=40),
        Course(course_name="Organic Chemistry", course_code="CHEM201", max_capacity=55),
        Course(course_name="Astrophysics", course_code="PHY305", max_capacity=35)
    ]
    db.session.add_all(sci_courses)
    
    # Disable autoflush temporarily
    original_autoflush = db.session.autoflush
    db.session.autoflush = False
    
    for course in sci_courses:
        course.faculty = sci_faculty
        course.set_department()
        course.degrees.extend([physics_degree, chemistry_degree])
    
    # Restore original autoflush setting
    db.session.autoflush = original_autoflush

    # ======================
    #  Humanities Faculty
    # ======================
    hum_faculty = Faculty(name="Faculty of Humanities", dean="Prof. Sarah Williamson")
    uni.faculties.append(hum_faculty)
    db.session.add(hum_faculty)

    history_degree = Degree(
        name="BA History",
        rank="Undergraduate",
        requirements="A-levels: History + two humanities subjects",
        faculty=hum_faculty
    )
    db.session.add(history_degree)

    literature_degree = Degree(
        name="MA English Literature",
        rank="Postgraduate",
        requirements="BA in English or related field",
        faculty=hum_faculty
    )
    db.session.add(literature_degree)

    hum_courses = [
        Course(course_name="Medieval European History", course_code="HIS101", max_capacity=120),
        Course(course_name="Shakespeare Studies", course_code="LIT301", max_capacity=45),
        Course(course_name="Modern Political Philosophy", course_code="PHIL201", max_capacity=60)
    ]
    db.session.add_all(hum_courses)
    
    # Disable autoflush temporarily
    original_autoflush = db.session.autoflush
    db.session.autoflush = False
    
    for course in hum_courses:
        course.faculty = hum_faculty
        course.set_department()
        course.degrees.extend([history_degree, literature_degree])
    
    # Restore original autoflush setting
    db.session.autoflush = original_autoflush

    # ======================
    #  Business Faculty
    # ======================
    bus_faculty = Faculty(name="Business School", dean="Dr. Michael Chen")
    uni.faculties.append(bus_faculty)
    db.session.add(bus_faculty)

    mba_degree = Degree(
        name="Master of Business Administration",
        rank="Postgraduate",
        requirements="3+ years work experience + undergraduate degree",
        faculty=bus_faculty
    )
    db.session.add(mba_degree)

    bba_degree = Degree(
        name="BSc Business Administration",
        rank="Undergraduate",
        requirements="A-levels: Mathematics + two other subjects",
        faculty=bus_faculty
    )
    db.session.add(bba_degree)

    bus_courses = [
        Course(course_name="Financial Accounting", course_code="BUS101", max_capacity=150),
        Course(course_name="Strategic Management", course_code="MBA501", max_capacity=30),
        Course(course_name="Marketing Principles", course_code="BUS202", max_capacity=90)
    ]
    db.session.add_all(bus_courses)
    
    # Disable autoflush temporarily
    original_autoflush = db.session.autoflush
    db.session.autoflush = False
    
    for course in bus_courses:
        course.faculty = bus_faculty
        course.set_department()
        course.degrees.extend([mba_degree, bba_degree])
    
    # Restore original autoflush setting
    db.session.autoflush = original_autoflush

    db.session.commit()

@app.route('/')
def index():
    student_count = Student.query.count()
    staff_count = StaffMember.query.count()
    faculty_count = Faculty.query.count()
    course_count = Course.query.count()
    recent_students = Student.query.order_by(Student.id.desc()).limit(5).all()
    uni = University.query.first()
    
    return render_template('index.html', 
                        university=uni,
                        student_count=student_count,
                        staff_count=staff_count,
                        faculty_count=faculty_count,
                        course_count=course_count,
                        recent_students=recent_students)
# Route to add a student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        aps_points = request.form.get('aps_points')
        faculty_id = request.form.get('faculty_id')
        degree_id = request.form.get('degree_id')
        
        try:
            aps_points = int(aps_points)
            faculty_id = int(faculty_id)
        except (ValueError, TypeError):
            flash("Invalid input values", "danger")
            return redirect(url_for('add_student'))

        uni = University.query.first()
        student = Student(name=name, aps_points=aps_points)
        
        # Set required relationships
        student.faculty_id = faculty_id
        if degree_id:
            student.degree_id = degree_id

        admitted = uni.add_student(student)
        db.session.add(student)
        db.session.commit()
        
        if admitted:
            flash(f"Student added successfully with ID: {student.student_id}", "success")
        else:
            flash("Student admission rejected based on APS points.", "warning")
        return redirect(url_for('students'))
    
    # GET request handling
    faculties = Faculty.query.all()
    degrees = Degree.query.all()
    return render_template('add_student.html', faculties=faculties, degrees=degrees)

# Route to list students
@app.route('/students')
def students():
    all_students = Student.query.all()
    return render_template('list_students.html', students=all_students)

# Route to add a staff member
@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        uni = University.query.first()
        staff = StaffMember(name, role)
        uni.add_staffmember(staff)
        db.session.add(staff)
        db.session.commit()
        flash(f"Staff added successfully with ID: {staff.staff_id}", "success")
        return redirect(url_for('list_staff'))
    return render_template('add_staff.html')

# Route to add a course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_code = request.form.get('course_code')
        max_capacity = request.form.get('max_capacity')
        faculty_id = request.form.get('faculty_id')

        try:
            max_capacity = int(max_capacity)
            faculty_id = int(faculty_id)
        except (ValueError, TypeError):
            flash("Invalid input values", "danger")
            return redirect(url_for('add_course'))

        # Create course with required fields
        course = Course(
            course_name=course_name,
            course_code=course_code,
            max_capacity=max_capacity
        )
        
        # Assign relationships
        course.faculty_id = faculty_id
        
        # Assign to default department if none exists
        dept = Department.query.first()
        if not dept:
            dept = Department(name="Default Department")
            db.session.add(dept)
            db.session.commit()
        course.department = dept

        db.session.add(course)
        db.session.commit()
        flash("Course added successfully", "success")
        return redirect(url_for('courses'))
    
    faculties = Faculty.query.all()
    return render_template('add_course.html', faculties=faculties)

# Route to list courses
@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('list_courses.html', courses=all_courses)

# API endpoint for courses (for DataTables)
@app.route('/api/courses')
def api_courses():
    courses = Course.query.all()
    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'course_name': course.course_name,
            'course_code': course.course_code,
            'max_capacity': course.max_capacity,
            'enrolled': course.students_enrolled.count(),
            'department': course.department.name if course.department else 'N/A',
            'faculty': course.faculty.name if course.faculty else 'N/A',
            'dean': course.faculty.dean if course.faculty else 'N/A',
            'degrees': [degree.name for degree in course.degrees]
        })
    return jsonify(courses_data)

# Route to add a faculty (and assign staff and courses)
@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        name = request.form.get('faculty_name')
        dean = request.form.get('dean_name')
        
        # Create new faculty
        new_faculty = Faculty(name, dean)
        
        # Get university and add faculty to it
        uni = University.query.first()
        uni.add_faculty(new_faculty)
        
        # Handle staff assignments
        staff_ids = request.form.getlist('staff_ids')
        for staff_id in staff_ids:
            staff = StaffMember.query.get(staff_id)
            if staff:
                staff.faculty = new_faculty
        
        # Handle course assignments
        course_ids = request.form.getlist('course_ids')
        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                course.faculty = new_faculty

        for staff_id in staff_ids:
            staff = StaffMember.query.get(staff_id)
            if staff:
                staff.faculty = new_faculty
            else:
                flash(f"Staff member with ID {staff_id} not found", "warning")

        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                course.faculty = new_faculty
            else:
                flash(f"Course with ID {course_id} not found", "warning")
        
        db.session.commit()
        flash('Faculty added successfully!', 'success')
        return redirect(url_for('list_faculties'))
    
    # For GET request: list available staff and courses not yet assigned to a faculty
    staff = StaffMember.query.filter_by(faculty_id=None).all()
    courses = Course.query.filter_by(faculty_id=None).all()
    return render_template('add_faculty.html', staff=staff, courses=courses)

# Route to list staff members
@app.route('/list_staff')
def list_staff():
    staff = StaffMember.query.all()
    return render_template('list_staff.html', staff=staff)

# Route to list faculties
@app.route('/list_faculties')
def list_faculties():
    faculties = Faculty.query.all()
    return render_template('list_faculties.html', faculties=faculties)

# Add degree program
@app.route('/add_degree', methods=['GET', 'POST'])
def add_degree():
    if request.method == 'POST':
        name = request.form.get('name')
        rank = request.form.get('rank')
        faculty_id = request.form.get('faculty_id')
        requirements = request.form.get('requirements')
        
        new_degree = Degree(name, rank)
        new_degree.faculty_id = faculty_id
        new_degree.requirements = requirements
        
        db.session.add(new_degree)
        db.session.commit()
        flash('Degree program added successfully!', 'success')
        return redirect(url_for('list_degrees'))
    
    faculties = Faculty.query.all()
    return render_template('add_degree.html', faculties=faculties)

# List degrees
@app.route('/degrees')
def list_degrees():
    degrees = Degree.query.all()
    return render_template('list_degrees.html', degrees=degrees)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True)