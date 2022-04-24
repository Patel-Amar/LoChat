from flask import request, Blueprint, render_template,redirect
from sources.user import User
from blueprints.auth import login_page

home = Blueprint( 'home', __name__ )

@home.route( '/', methods = [ 'GET', 'POST' ] )
def home_page():
	return redirect("/login", code = 302)
