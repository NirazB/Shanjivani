# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = "Hello"

# Configure SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25),unique=True, nullable=False)
    # email = db.Column(db.String(100), unique=True , nullable=False)
    password_hash = db.Column(db.String(200))  # Rename column to password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@app.route('/')
def home():
    if "username" in session:
        return render_template('index.html',username=session['username'])
    return render_template('index.html', username='guest')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/sos', methods=['GET', 'POST'])
def sos():
    if request.method == 'POST':
        # Handle SOS action here (e.g., send alert or log data)
        emergency_details = request.form['details']
        return render_template('sos.html', message="SOS Triggered Successfully!")
    return render_template('sos.html')

@app.route('/dashboard')
def dashboard():
    # Simulated hospital data with dynamic percentage calculation
    available_beds_current = 150
    available_beds_total = 200
    available_beds_percentage = (available_beds_current / available_beds_total) * 100
    
    resource_data = {
        'available_beds': {
            'current': available_beds_current,
            'total': available_beds_total,
            'percentage': available_beds_percentage
        },
        'staff_on_duty': {
            'doctors': 45,
            'nurses': 120,
            'total': 165
        },
        'medical_equipment': {
            'ventilators': {
                'available': 30,
                'total': 40,
                'percentage': 75
            },
            'mri_machines': {
                'available': 5,
                'total': 8,
                'percentage': 62.5
            }
        },
        'emergency_room': {
            'current_patients': 25,
            'wait_time': 45,
            'critical_cases': 3
        },
        'patient_statistics': {
            'admissions': 120,
            'discharges': 95,
            'in_patient': 250
        }
    }
    return render_template('dashboard.html', data=resource_data)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')
    
# signup
@app.route('/signup', methods=['POST', 'GET'])  # Changed 'method' to 'methods'
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('signup'))
                
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User created successfully. Please login.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))
    return render_template('login.html')
   
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


