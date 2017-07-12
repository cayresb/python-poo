import sqlite3

class BancoDeDados:
	"""Classe que representa o banco de dados (database) da aplicação"""

	def __init__(self, nome='banco.db'):
		self.nome, self.conexao = nome, None

	def conecta(self):
		"""Conecta passando o nome do arquivo"""
		self.conexao = sqlite3.connect(self.nome)

	def desconecta(self):
		"""Desconecta do banco"""
		try:
			self.conexao.close()
		except AttributeError:
			pass

	def criar_tabelas(self):
		"""Cria as tabelas do banco"""
		try:
			cursor = self.conexao.cursor()

			cursor.execute("""
			CREATE TABLE IF NOT EXISTS clientes (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					nome TEXT NOT NULL,
					cpf VARCHAR(11) UNIQUE NOT NULL,
					email TEXT NOT NULL
			);
			""")

		except AttributeError:
			print('Faça a conexão do banco antes de criar as tabelas.')

	def inserir_cliente(self, nome, cpf, email):
		"""Insere cliente no banco"""
		try:
			cursor = self.conexao.cursor()

			try:
				cursor.execute("""
					INSERT INTO clientes (nome, cpf, email) VALUES (?,?,?)
				""", (nome, cpf, email))
			except sqlite3.IntegrityError:
				print('O cpf %s já existe!' % cpf)

			self.conexao.commit()

		except AttributeError:
			print('Faça a conexão do banco antes de inserir clientes.')

	def buscar_cliente(self, cpf):
		"""Busca um cliente pelo cpf"""
		try:
			cursor = self.conexao.cursor()

			# Tentando EAFP!!
			try:
				cursor.execute("""SELECT nome FROM clientes WHERE cpf =""" + cpf)
				var_nome = cursor.fetchone()
				if var_nome is None:
					print('Cliente não encontrado. Verifique se o CPF foi inserido corretamente!')
				else:
					print('Cliente %s encontrado.' % var_nome)
			except:
				pass
		except AttributeError:
			print('Faça a conexão do banco antes de buscar clientes.')

	def remover_cliente(self, cpf):
		"""Removendo cliente a partir do CPF"""
		# EAFP
		try:
			cursor = self.conexao.cursor()
			# EAFP
			try:
				cursor.execute("""SELECT nome FROM clientes WHERE cpf =""" + cpf)
				var_nome = cursor.fetchone()
				# LBYL
				if var_nome is None:
					print('Cliente não encontrado. Verifique se o CPF foi inserido corretamente!')
					# break
				else:
					cursor.execute("""DELETE FROM clientes WHERE cpf ="%s" """ % cpf)
					print('Cliente %s foi removido com suscesso!' % var_nome)

			except:
				pass

			self.conexao.commit()
		except AttributeError:
			print('Faça a conexão do banco antes de buscar clientes.')

	def buscar_email(self, email):
		"""Buscando cliente por email e retornando verdadeiro (True) ou falso (False)"""
		# EAFP
		try:
			cursor = self.conexao.cursor()
			# EAFP
			try:
				cursor.execute("""SELECT nome FROM clientes WHERE email="%s" """ % email)
				var_nome = cursor.fetchone()
				# LBYL
				if var_nome is None:
					print('False! E-mail não encontrado!')
				else:
					print('True! E-mail referente ao cliente %s!' % var_nome)
			except:
				pass

		except AttributeError:
			print('Faça a conexão do banco antes de buscar clientes.')
