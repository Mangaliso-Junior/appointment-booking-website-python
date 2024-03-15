from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '293e0ea94047c1aca2dd0a70497ef2d7971ebea8086a6f82cbb19b1e501ac7d2'

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="mangaliso",
    password="Mangi@1997",
    database="appointments"
)

cursor = db.cursor()

USERNAME = "admin"
PASSWORD = "admin123"

def check_login(): 
    if 'username' in session: 
        return True
    return False

@app.route('/')
def index():
    if not check_login(): 
        return redirect(url_for('login'))
    # Fetch all appointments from the database
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    return render_template('index.html', appointments=appointments,check_login=check_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            # Set the session variable upon successful login
            session['username'] = username
            # Redirect to the index page after successful login
            return redirect(url_for('index'))
        else:
            # Display an error message for unsuccessful login attempts
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message, check_login=check_login)

    return render_template('login.html', check_login=check_login)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if not check_login():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get data from the form
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']

        # Insert the data into the database
        cursor.execute("""
            INSERT INTO appointments (patient_name, doctor_name, appointment_date)
            VALUES (%s, %s, %s)
        """, (patient_name, doctor_name, appointment_date))

        db.commit()

        return redirect(url_for('index'))

    return render_template('book_appointment.html', check_login=check_login)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session data for 'username'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
