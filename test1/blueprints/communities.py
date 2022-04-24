from cmath import log
from random import random
from typing import Text
from webbrowser import get
from flask import request, Blueprint, render_template, redirect, abort
from sources.user import User
from sources.community import Community
from sources.utils.storage import Storage
from sources.utils.randomFunctions import randomFunctions

communities = Blueprint( 'communities', __name__ )

@communities.route( '/browse', methods = [ 'GET', 'POST' ] )
def browse_page():
	logged_in_user = User.is_logged_in()

	with(open("data\\communities.json", "r") as f):
		communities = f.read()

	if logged_in_user != None:
		if request.method == 'POST':
			if request.form.get("submit") == "post":
			# @TODO	Add form validation
				create_community = Community.create(
					owner_id = logged_in_user['id'],
					name = request.form.get( 'CommunityName' ),
					description = request.form.get("CommunityDescription")
				)
				return redirect( '/community/' + create_community['community']['id'] )

		return render_template(
			'community/browse.html',
			logged_in_user = logged_in_user,
			communities = communities
		)

	return redirect("/login")

@communities.route( '/community/<id>', methods = [ 'GET', 'POST' ] )
def community_page( id ):
	logged_in_user = User.is_logged_in()
	community = Community.get( id = id )
	communityPosts = Storage.get_value(
		file = "communityPost",
		key = id
	)
	membersInCommunity = Storage.get_value(
		file = "community_members_by_community_id",
		key = id
	)
	if logged_in_user != None:
		if User.returnID() in membersInCommunity:
			if request.method == "POST":
				if request.form.get("submit") == "post":
					text = request.form.get("text")
					if text != "":
						Storage.adjustValue(
							file = "communities\\communityPost" + id,
							newChange = [User.is_logged_in()['username'],text, randomFunctions.getDate() ]
						)
						return redirect("/community/" + str(id)) 
	else:
		return redirect("/login")

	communityLikes = Storage.get_value(
		file = "communityLikes",
		key = id
	)

	with(open("data\\communities\\communityPost" + id + ".json", "r") as f):
		communityPosts = f.read()
	
	if community != None:
		members_ids = Community.get_members( id = community['id'] )
		members = {}
		all_users = User.get()
		for user_id in members_ids:
			members[ user_id ] = all_users[ user_id ]

		return render_template(
			'community/community.html',
			logged_in_user = logged_in_user,
			community = community,
			members = members,
			likes = communityLikes['likes'],
			idnum = communityPosts,
			member = User.returnID() in membersInCommunity
		)

	else:
		return abort( 404 )

#Links this function to the url of community/<id>/join
@communities.route( '/community/<id>/join' )
def join_page( id ):
	#Collects the information of the logged in user
	logged_in_user = User.is_logged_in()
	#Collects the community information of a community with the id
	community = Community.get( id = id )

	#If the community does exist and the user is logged in
	if community != None and logged_in_user != None:
		#Add the user to the community member list
		Community.add_member_to_community(
			community_id = community['id'],
			user_id = logged_in_user['id']
		)
		#Send the user back to the community page
		return redirect( '/community/' + community['id'] )

	#if the user is not logged in or the community does not exist,
	#give the error 404
	else:
		return abort( 404 )

@communities.route( '/community/<id>/leave' )
def leave_page( id ):
	logged_in_user = User.is_logged_in()
	community = Community.get( id = id )

	if community != None and logged_in_user != None:
		Community.remove_member_from_community(
			community_id = community['id'],
			user_id = logged_in_user['id']
		)
		return redirect( '/community/' + community['id'] )
	else:
		return abort( 404 )

@communities.route( '/community/<id>/delete' )
def delete_community_page( id ):
	logged_in_user = User.is_logged_in()
	community = Community.get( id = id )

	Storage.deleteFile("data\\communities\\communityPost" + str(id))

	if community != None and logged_in_user != None:
		Community.delete_community(
			community_id = community['id'],
			user_id = logged_in_user['id']
		)
		return redirect( '/browse?dc=yes' )
	else:
		return abort( 404 )

@communities.route("/community/<id>/like")
def likeCommunity(id):
	logged_in_user = User.is_logged_in()
	communityLikes = Storage.get_value(
		file = "communityLikes", 
		key = id
	)
	if logged_in_user != None:
		if (User.returnID() in communityLikes['ids']):
			return redirect("/community/" + str(id)) 
		
		else:
			Storage.adjustValue(
				file = "communityLikes",
				key = id,
				value = 'likes',
				newChange = communityLikes['likes'] + 1

			)
			Storage.adjustValue(
				file = "communityLikes",
				key = id,
				value = "ids",
				newChange = communityLikes["ids"] + [User.returnID()]

			)
	return redirect("/community/" + str(id)) 


	