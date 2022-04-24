from flask import request, Blueprint, render_template,redirect
from sources.user import User
from blueprints.auth import login_page

about = Blueprint( 'about', __name__ )

@about.route( '/about', methods = [ 'GET', 'POST' ] )
def about_page():
	logged_in_user = User.is_logged_in()
	return render_template(
		'about.html',
		logged_in_user = logged_in_user,
	)