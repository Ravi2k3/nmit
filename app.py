from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    branch = db.Column(db.String(50), nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/qrCode', methods=['GET', 'POST'])
def qr_code_page():
    if request.method == 'POST':
        name = request.form.get('name')
        branch = request.form.get('branch')

        if not name or not branch:
            return "Invalid data", 400
        existing_student = Student.query.filter_by(name=name).first()
        if existing_student:
            return render_template('qrCode.html', message = "Name already exists")
        
        new_student = Student(name=name, branch=branch)
        db.session.add(new_student)
        db.session.commit()
        
        return render_template('qrCode.html', "Data submitted successfully")
    
    return render_template('qrCode.html', message="")

@app.route('/counter/<branch>', methods=['GET'])
def get_branch_data(branch):
    students = Student.query.filter_by(branch=branch).all()
    if students:
        return render_template('counter.html', branch=branch, students=students)
    else:
        return "Invalid branch or no data", 400

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=8000)