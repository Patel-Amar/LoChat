from crypt import methods
from pickle import GET
from flask import Blueprint
from sources.user import User

profile = Blueprint('profile', __name__)

@profile.route('/profile/<prof_id>', methods = ['GET', 'POST'])
def userProfile(prof_id):
    userLoggedIn = User.is_logged_in()
    #user is viewing their own profile
    if(prof_id == userLoggedIn['id']):
        #give option to edit
        pass
    else:
        #no option to edit
        pass

@profile.route('/profile/<prof_id>/edit', methods = ['GET', 'POST'])
def editProfile(prof_id):
    #show hmtl script for editing profile
    pass