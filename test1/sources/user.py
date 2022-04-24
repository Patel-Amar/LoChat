import json
from argon2 import PasswordHasher
import uuid
from sources.session import Session
from sources.utils.storage import Storage
from flask import request

class User:
	@staticmethod
	def get( id = None ):
		if id == None:
			return Storage.get_value(
				file = 'users'
			)
		else:
			return Storage.get_value(
				file = 'users',
				key = id
			)

	@staticmethod
	def get_by_id( id ):
		return Storage.get_value(
			file = 'users',
			key = id
		)

	@staticmethod
	def get_by_email( email ):
		email = email.lower()
		user_id = Storage.get_value(
			file = 'users_by_email',
			key = email
		)

		if user_id:
			return User.get_by_id( user_id )

		return None

	@staticmethod
	def get_by_username( username ):
		username = username.lower()
		user_id = Storage.get_value(
			file = 'users_by_username',
			key = username
		)

		if user_id:
			return User.get_by_id( user_id )

		return None

	@staticmethod
	def get_by_username_or_email( value ):
		username = User.get_by_username( value )
		if username:
			return username

		email = User.get_by_email( value )
		if email:
			return email

		return None

	@staticmethod
	def register( email, username, first_name, last_name, password ):
		ph = PasswordHasher()

		id = str( uuid.uuid4() )
		email = email.lower()
		hashed_password = ph.hash( password )

		email_in_use = Storage.get_value(
			file = 'users_by_email',
			key = email
		)

		username_in_use = Storage.get_value(
			file = 'users_by_username',
			key = username.lower()
		)

		if email_in_use:
			raise Exception( 'EMAIL_IN_USE' )

		if username_in_use:
			raise Exception( 'USERNAME_IN_USE' )

		new_user = {
			'id': id,
			'email': email,
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
			'hashed_password': hashed_password
		}

		Storage.add_value(
			file = 'users',
			key = id,
			value = new_user
		)

		Storage.add_value(
			file = 'users_by_email',
			key = email,
			value = id
		)

		Storage.add_value(
			file = 'users_by_username',
			key = username.lower(),
			value = id
		)

		return new_user

	@staticmethod
	def login( login, password ):
		user = User.get_by_username_or_email( login )
		ph = PasswordHasher()
		if user:
			try:
				if ph.verify( user['hashed_password'], password ):
					session = Session.create(
						user_id = user['id']
					)
					return {
						'session': session,
						'user': user
					}
			except Exception as ex:
				print( ex )

	@staticmethod
	def is_logged_in( token = None ):
		if token == None:
			token = request.cookies.get( 'S' )

		if token != None:
			session = Session.get_by_token( token )
			if session:
				user = User.get_by_id( session['user_id'] )
				if user:
					return user

		return None

	@staticmethod
	def logout( token ):
		return Session.remove_token( token )

	@staticmethod
	def returnID():
		token = request.cookies.get("S")
		session = Session.get_by_token(token)
		return session['user_id']
