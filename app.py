# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize mail
mail = Mail(app)

# Database model for user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        password = request.form['password']

        # Create a new user
        new_user = User(email=email, birthdate=birthdate, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        verification_url = url_for('verify_email', token=token, _external=True)
        msg = Message('Verify Your Email', sender='your_email@example.com', recipients=[email])
        msg.body = f'Click the link to verify your email: {verification_url}'
        mail.send(msg)

        flash('Verification email has been sent!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

# Verification route
@app.route('/verify_email/<token>')
def verify_email(token):
    # Verify email logic here
    flash('Email verified successfully!', 'success')
    return redirect(url_for('home'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,host=0.0.0.0,port=8080)
