from cmath import log
from random import random
from typing import Text
from webbrowser import get
from flask import request, Blueprint, render_template, redirect, abort, jsonify
from sources.user import User
from sources.community import Community
from sources.utils.storage import Storage
from sources.utils.randomFunctions import randomFunctions
import json

account_settings = Blueprint( 'account_settings', __name__ )

@account_settings.route( '/settings', methods = [ 'GET' ] )
def settings_page():
	logged_in_user = User.is_logged_in()

	if logged_in_user != None:
		return render_template(
			'account/settings.html',
			logged_in_user = logged_in_user
		)

	return redirect( '/login' )

@account_settings.route( '/_/settings', methods = [ 'POST' ] )
def update_settings_page():
	logged_in_user = User.is_logged_in()

	if logged_in_user != None:
		data = json.loads( request.data, strict = False )
		if data['setting'] == 'setlocation':
			logged_in_user['location'] = {
				'coords': {
					'latitude': data['data']['lat'],
					'longitude': data['data']['long']
				}
			}
			Storage.add_value(
				file = 'users',
				key = logged_in_user['id'],
				value = logged_in_user
			)
	return redirect("/settings")

@account_settings.route( '/removeLocation' )
def removeLocation():
	logged_in_user = User.is_logged_in()

	if logged_in_user != None:
			logged_in_user.pop( 'location', None )
			Storage.add_value(
				file = 'users',
				key = logged_in_user['id'],
				value = logged_in_user
			)

	return redirect( '/settings' )
