from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for flash messages

# -------------------------
# MySQL connection
# -------------------------
db = mysql.connector.connect(
    host="10.111.21.71",          # VM IP over VPN
    user="admin",                 # admin can connect remotely
    password="admin#ab12cd34",
    database="ccsccDB"
)

# -------------------------
# ROUTES
# -------------------------

@app.route('/')
def home():
    """Driver stats home page"""
    return render_template('driver_status_home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login form submission"""
    if request.method == 'POST':
        email = request.form['username']  # matches HTML input name
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT verify_login(%s, %s)", (email, password))
        result = cursor.fetchone()

        if result and result[0]:  # True if login successful
            flash("Login successful!", "success")
            print("account found")
            return redirect(url_for('home'))  # redirect to driver_status_home page
        else:
            flash("Invalid email or password.", "danger")
            print("account not found")
            return redirect(url_for('login'))

    # GET request → show login page
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle account creation form submission"""
    if request.method == 'POST':
        username = request.form['username']
        drivername = request.form['drivername']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.callproc('create_account', (username, drivername, email, password))
        db.commit()

        flash("Account created (if email was unique). Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# -------------------------
# RUN FLASK
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
