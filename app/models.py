from ldap3 import Server, Connection, ALL, NTLM, AUTO_BIND_NO_TLS, SUBTREE, ALL_ATTRIBUTES
from app import app

# Класс Пользователь
class User():
	name = None
	def __init__(self, username, password):
		self.username = username

	# метод проверки логина и пароля по протоколу LDAP
	@staticmethod
	def try_login(username, password):
		# DNS сервер
		server = Server('192.168.1.1', get_info=ALL)
		# Попытка подключения к серверу по ldap
		# В случае неудачи будет вызвано исключение и функция вернет False
		try:
			conn = Connection(server, user='DC\\'+username, password=password, authentication=NTLM, auto_bind=True)
		except:
			return False
		else:
			# В случае успеха - будет произведен поиск в базе по логину
			# Функция вернет True
			# и присвоит атрибуту name ФИО пользователя
			conn.search(search_base='OU=FGBUUsers,DC=dc,DC=local',
				search_filter='(&(sAMAccountName='+username+'))',
				search_scope=SUBTREE,
				attributes=ALL_ATTRIBUTES,
				get_operational_attributes=True)
			conn.result
			User.name = conn.entries[0].name.value # Атрибуту класса будет присвоино ФИО пользователя
			return True
