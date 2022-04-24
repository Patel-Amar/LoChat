from flask import redirect, request, Blueprint, render_template
from sources.user import User

register = Blueprint( 'register', __name__ )

@register.route( '/register', methods = [ 'GET', 'POST' ] )
def register_page():
	logged_in_user = User.is_logged_in()
	if request.method == 'POST':
		success = False
		form = {
			'first_name': {
				'success': False
			},
			'last_name': {
				'success': False
			},
			'username': {
				'success': False
			},
			'email': {
				'success': False
			},
			'city': {
				'success': False
			},
			'password': {
				'success': False
			},
		}
		first_name = request.form.get( 'first_name' )
		last_name = request.form.get( 'last_name' )
		username = request.form.get( 'username' )
		email = request.form.get( 'email' )
		#city = request.form.get( 'city' )
		password = request.form.get( 'password' )

		#if first_name and len( first_name ) < 1:
			
		try:
			User.register(
				email = email,
				username = username,
				first_name = first_name,
				last_name = last_name,
				password = password
			)

			return redirect("/login")
		except Exception as ex:
			print(ex)


	return render_template(
		'register.html',
		logged_in_user = logged_in_user
	)