from argon2 import PasswordHasher
import uuid
import secrets
import json
from sources.utils.storage import Storage

class Session:
	@staticmethod
	def create( user_id ):
		id = str( uuid.uuid4() )
		token = secrets.token_urlsafe( 100 )

		new_session = {
			'id': id,
			'user_id': user_id
		}

		Storage.add_value(
			file = 'sessions',
			#key = id,
			key = token,
			value = new_session
		)

		'''Storage.add_value(
			file = 'sessions_by_token',
			key = token,
			value = id
		)'''

		return {
			'id': id,
			'user_id': id,
			'token': token
		}

	@staticmethod
	def get_by_token( token ):
		session = Storage.get_value(
			file = 'sessions',
			key = token
		)
		if session:
			return session
		'''id = Storage.get_value(
			file = 'sessions_by_token',
			key = token
		)

		if id:
			session = Storage.get_value(
				file = 'sessions',
				key = id
			)
			if session:
				return session

		return None'''

	@staticmethod
	def remove_token( token ):
		Storage.remove_value(
			file = 'sessions',
			key = token
		)