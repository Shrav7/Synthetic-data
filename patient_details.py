import psycopg2
from flask import Flask,render_template, url_for
from flask import request, redirect, jsonify


app = Flask(__name__)
def get_connection():
	db = 'postgresql://postgres:12345@localhost/postgres'
	conn = psycopg2.connect(db)
	return conn

@app.route('/patient',methods=['post', 'get'])
def index():
	global patient_id, department
	conn = get_connection()
	cur = conn.cursor()
	cur.execute('SELECT patient_id,dept FROM Patient_info;')
	data = cur.fetchall()
	return render_template("display.html",value = data)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'user' or request.form['password'] != '12345':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/submit',methods = ['POST','GET'])
def submit():
	error = None
	if request.method == 'POST':
		p_id = int(request.form['patient_id'])
	return redirect(url_for('patient',p_id=p_id))

@app.route('/details',methods = ['POST','GET'])
def details():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute('SELECT * FROM Patient_info;')
	data = cur.fetchall()
	return render_template("all_details.html",data = data)

@app.route('/display/<int:p_id>/',methods=['post', 'get'])
def patient(p_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute('SELECT dept FROM Patient_info;')
	departments = cur.fetchall()
	department = list(departments[p_id])
	cur.execute('SELECT gender FROM Patient_info;')
	gender = cur.fetchall()
	cur.execute('SELECT disease FROM Patient_info;')
	disease = cur.fetchall()
	cur.execute('SELECT body_structure FROM Patient_info;')
	body = cur.fetchall()
	cur.execute('SELECT expired FROM Patient_info;')
	exp = cur.fetchall()
	return render_template("patients.html",p_id = p_id, dept = department,gender = list(gender[p_id]),Disease = list(disease[p_id]),body = list(body[p_id]),exp = list(exp[p_id]))


@app.route('/end',methods = ['POST','GET'])
def final_page():
	return render_template("final_page.html")


if __name__ == '__main__':
	app.run(debug = True)
