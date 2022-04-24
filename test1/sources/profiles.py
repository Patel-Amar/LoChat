import json
from argon2 import PasswordHasher
import uuid
from sources.session import Session
from sources.utils.storage import Storage
from sources.user import User
from flask import request

class Profile:
    @staticmethod
    def createProfile():
        logged_in_user = User.is_logged_in()

        id = logged_in_user['id']
        fName = logged_in_user['first_name']
        lName = logged_in_user['last_name']
        username = logged_in_user['username']
        pNouns = ""
        bio = ""



        new_profile = {
            'id': id,
            'first_name': fName,
            'last_name': lName,
            'username': username,
            'pNouns': pNouns,
            'bio': bio
        }

        Storage.add_value(
            file='profiles.json',
            key=id,
            value=new_profile
        )

        return new_profile
    @staticmethod
    def get(id = None):
        if(id != None):
            return Storage.get_value(
                file='profiles.json',
                key='id'
            )
        else:
            return Storage.get_value(
                file='profiles.json'
            )
    
    @staticmethod
    def changeFirstName(newName):
        logged_in_user = User.is_logged_in()
        new_prof = Profile.get(logged_in_user['id'])
        new_prof['first_name'] = newName
        Storage.adjustValue(
            file='profiles.json',
            key=logged_in_user['id'],
            newChange=new_prof
        )
    @staticmethod
    def changeLastName(newName):
        logged_in_user = User.is_logged_in()
        new_prof = Profile.get(logged_in_user['id'])
        new_prof['last_name'] = newName
        Storage.adjustValue(
            file='profiles.json',
            key=logged_in_user['id'],
            newChange=new_prof
        )
    @staticmethod
    def changeUsername(newName):
        #Gets the log in information for the user
        logged_in_user = User.is_logged_in()
        #sets the variable to the profile of the logged in user
        new_prof = Profile.get(logged_in_user['id'])
        #Changes the usernname to the newer name the user wants
        new_prof['username'] = newName
        #Changes the values to the new value inside of the .json file
        Storage.adjustValue(
            file='profiles.json',
            key=logged_in_user['id'],
            newChange=new_prof
        )
    @staticmethod
    def changePronouns(newPns):
        logged_in_user = User.is_logged_in()
        new_prof = Profile.get(logged_in_user['id'])
        new_prof['pNouns'] = newPns
        Storage.adjustValue(
            file='profiles.json',
            key=logged_in_user['id'],
            newChange=new_prof
        )
    @staticmethod
    def changeBio(newBio):
        logged_in_user = User.is_logged_in()
        new_prof = Profile.get(logged_in_user['id'])
        new_prof['bio'] = newBio
        Storage.adjustValue(
            file='profiles.json',
            key=logged_in_user['id'],
            newChange=new_prof
        )