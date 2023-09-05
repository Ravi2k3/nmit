from flask import Flask, request, jsonify, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(50), nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/qrCode', methods=['GET', 'POST'])
def qr_code_page():
    if request.method == 'POST':
        name = request.form.get('name')
        branch = request.form.get('branch')
        semester = request.form.get('semester')

        if not name or not branch:
            return "Invalid data", 400
        existing_student = Student.query.filter_by(name=name).first()
        if existing_student:
            flash("Name already exists!")
            return render_template('qrCode.html')
        
        new_student = Student(name=name, branch=branch, semester=semester)
        db.session.add(new_student)
        db.session.commit()

        flash("Data entered successfully!")
        return render_template('qrCode.html')
    
    return render_template('qrCode.html')

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