from flask import render_template
from flask import Flask, flash, redirect, session, abort, request
from app import app
from openpyxl import load_workbook
from app.models import User
import os


app.secret_key = os.urandom(24)


@app.route('/')
@app.route('/index')
def index():
	def get_user_ip():
		ip = request.headers.get('X-Real-IP')
		return ip
	ip = get_user_ip()
	return render_template("index.html",
		title = 'Портал ФГБУ "ЦГКиИПД"',
		ip = ip)

@app.route('/about')
def about():
	return render_template("about.html",
		title = 'О Портале')


@app.route('/numbers')
def numbers():
	sotr1 = []
	sotr2 = []
	workbook = load_workbook('/home/jack/flasksite/app/static/docs/en.xlsx')
	worksheet = workbook.get_active_sheet()
	def get_user_ip():
		ip = request.headers.get('X-Real-IP')
		return ip
#	ip = get_user_ip()
	for row in worksheet:
		for cell in row:
			if cell.value is None:
				sotr2.append(' ')
			else:
				sotr2.append(str(cell.value))
		sotr1.append(sotr2)
		sotr2 = []
#	if not session.get('logged_in'):
#		return render_template('accessdenied.html')
#	else:
	return render_template("enums.html",
	title = 'Список внутренних номеров',
	sotr1 = sotr1)

@app.route('/admin')
def home():
	if not session.get('logged_in'):
		return render_template("accessdenied.html")
	else:
		return 'Добро пожаловать в панель администрирования!'

@app.route('/signin')
def signin():
	if not session.get('logged_in'):
		return render_template("login.html")
	else:
		return redirect('index')

@app.route('/login', methods=['POST'])
def do_admin_login():
#	if request.form['password'] == 'iddqdids123' and request.form['username'] == 'admin':
		username = request.form['username']
		password = request.form['password']
		ldapaccess = User.try_login(username, password)
		if ldapaccess[0]:
			session['logged_in'] = True
			session['username'] = User.name
			return redirect('index')
		else:
			flash('wrong password')
			return signin()



#	else:
#		flash('wrong password!')
#	return signin()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	session['username'] = None
	return redirect('index')
