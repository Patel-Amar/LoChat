from flask import redirect, request, Blueprint, render_template, make_response,Response
from sources.user import User
from blueprints.register import register_page
auth = Blueprint( 'auth', __name__ )

@auth.route( '/login', methods = [ 'GET', 'POST'] )
def login_page():

	logged_in_user = User.is_logged_in()
	if request.method == 'POST':
		if request.form.get("submit") == "Signup":
			return redirect("/register",code = 302)
		elif request.form.get("submit") == "Login":
			success = False
			form = {
				'login': {
					'success': False
				},
				'password': {
					'success': False
				},
			}
			login = request.form.get( 'login' )
			password = request.form.get( 'password' )
				
			login_result = User.login(
				login,
				password
			)

			if login_result != None:
				response = make_response(
					redirect(
						'/browse'
					)
				)

				response.set_cookie( 'S', login_result['session']['token'] )
				return response
				
			else:
				return render_template("login.html", userNotFound = True)


	return render_template(
		'login.html',
		logged_in_user = logged_in_user
	)

@auth.route( '/logout' )
def logout_page():
	logged_in_user = User.is_logged_in()

	User.logout(
		request.cookies.get( 'S' )
	)

	response = make_response(
		redirect(
			"/login"
		)
	)
	return response
