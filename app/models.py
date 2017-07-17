from ldap3 import Server, Connection, ALL, NTLM, AUTO_BIND_NO_TLS, SUBTREE, ALL_ATTRIBUTES
from app import app


class User():
	name = None
	def __init__(self, username, password):
		self.username = username


	@staticmethod
	def try_login(username, password):
		server = Server('192.168.1.1', get_info=ALL)
		conndata = []
		try:
			conn = Connection(server, user='DC\\'+username, password=password, authentication=NTLM, auto_bind=True)
		except:
			c = False
			conndata.append(c)
			return conndata
		else:
			conn.search(search_base='OU=FGBUUsers,DC=dc,DC=local',
				search_filter='(&(sAMAccountName='+username+'))',
				search_scope=SUBTREE,
				attributes=ALL_ATTRIBUTES,
				get_operational_attributes=True)
			conn.result
			User.name = conn.entries[0].name.value
			c = True
			conndata.append(c)
			return conndata
