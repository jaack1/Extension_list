from flask import render_template
from flask import Flask, flash, redirect, session, abort, request
from app import app
from openpyxl import load_workbook
from app.models import User
import os


app.secret_key = os.urandom(24)

# Главная страница
@app.route('/')
@app.route('/index')
def index():
	def get_user_ip(): # Определяем ip пользователя
		ip = request.headers.get('X-Real-IP')
		return ip
	ip = get_user_ip()
	return render_template("index.html", # ip и титул передается в шаблон
		title = 'Портал ФГБУ "ЦГКиИПД"',
		ip = ip)

# Страничка "о портале", содержит техническую и контактную информацию о портале
@app.route('/about')
def about():
	return render_template("about.html",
		title = 'О Портале')

# Страница с таблицей внутренних номеров компании
@app.route('/numbers')
def numbers():
	sotr1 = []
	sotr2 = []
	workbook = load_workbook('/home/jack/flasksite/app/static/docs/en.xlsx')
	worksheet = workbook.get_active_sheet()
# При расскоменте строчек внизу, можно включить доступ к списку по ip
#	def get_user_ip():
#		ip = request.headers.get('X-Real-IP')
#		return ip
#	ip = get_user_ip()
	for row in worksheet: # парсим .xlsx в массивы, сначала в строчки, потом по столбцам
		for cell in row:
			if cell.value is None:
				sotr2.append(' ')
			else:
				sotr2.append(str(cell.value))
		sotr1.append(sotr2)
		sotr2 = []
# При расскоменте if ниже - включится доступ по логину на сайт
#	if not session.get('logged_in'):
#		return render_template('accessdenied.html')
#	else:
	return render_template("enums.html",
	title = 'Список внутренних номеров',
	sotr1 = sotr1)

# Админка, пока, небыло нужды доделывать ее
@app.route('/admin')
def home():
	if not session.get('logged_in'):
		return render_template("accessdenied.html")
	else:
		return 'Добро пожаловать в панель администрирования!'

# Страничка входа на сайт, отрендерит шаблон входа если юзер не залогинен
@app.route('/signin')
def signin():
	if not session.get('logged_in'):
		return render_template("login.html")
	else:
		return redirect('index')

# Обработка введенных учётных данных,
@app.route('/login', methods=['POST'])
def do_admin_login():
		username = request.form['username']
		password = request.form['password']
		# Вызовем из класса User метод для проверки логина и пароля по протоколу LDAP
		ldapaccess = User.try_login(username, password)
		# В случае совпадения, LDAP пустит пользователя, затем
		# найдет его ФИО и вернет True в ldapaccess
		# в случае несовпадения - ldapaccess будет False
		if ldapaccess:
			session['logged_in'] = True
			session['username'] = User.name
			return redirect('index')
		else:
			flash('wrong password')
			return signin()

# Следующий кусок использовася для тестов шаблона и пока не нужен
#	if request.form['password'] == 'iddqdids123' and request.form['username'] == 'admin':
# 		session['logged_in'] = True
# 		session['username'] = 'Admin'
#	else:
#		flash('wrong password!')
#	return signin()

# Страничка выхода из учетной записи
@app.route("/logout")
def logout():
	session['logged_in'] = False
	session['username'] = None
	return redirect('index')
