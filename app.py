from flask import Flask, request, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(20), unique=True, nullable=False)  # New unique USN field
    name = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(50), nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/qrCode', methods=['GET', 'POST'])
def qr_code_page():
    session.pop('_flashes', None)
    
    if request.method == 'POST':
        usn = request.form.get('usn')
        name = request.form.get('name')
        branch = request.form.get('branch')
        semester = request.form.get('semester')

        if not usn or not name or not branch or not semester:
            return "Invalid data", 400

        # Search for existing student by USN
        existing_student = Student.query.filter_by(usn=usn).first()

        if existing_student:
            existing_student.name = name
            existing_student.branch = branch
            existing_student.semester = semester
            db.session.commit()
            flash("Data updated successfully!", category='info')
        else:
            new_student = Student(usn=usn, name=name, branch=branch, semester=semester)
            db.session.add(new_student)
            db.session.commit()
            flash("Data entered successfully!", category='info')

        return render_template('qrCode.html')

    return render_template('qrCode.html')

@app.route('/counter', methods=['GET'])
def counter_selection():
    return render_template('counter_selection.html')

@app.route('/counter/<branch>', methods=['GET'])
def get_branch_data(branch):
    students = Student.query.filter_by(branch=branch).all()
    if students:
        return render_template('counter.html', branch=branch, students=students, semester=students[0].semester)
    else:
        return "Invalid branch or no data", 400

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=8000)
