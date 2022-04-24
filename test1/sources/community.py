from argon2 import PasswordHasher
import uuid
import secrets
import json
from sources.utils.storage import Storage
from sources.user import User
from sources.utils.randomFunctions import randomFunctions

class Community:
	@staticmethod
	def get( id = None ):
		if id == None:
			return Storage.get_value(
				file = 'communities'
			)
		else:
			return Storage.get_value(
				file = 'communities',
				key = id
			)

	@staticmethod
	def get_members( id = None ):
		return Storage.get_value(
			file = 'community_members_by_community_id',
			key = id
		)

	@staticmethod
	def create( owner_id, name, description ):
		id = str( uuid.uuid4() )

		new_community = {
			'id': id,
			'owner_id': owner_id,
			'name': name,
			'description': description
		}

		Storage.add_value(
			file = 'communities',
			key = id,
			value = new_community
		)

		likes = {
			'likes' : 1,
			'ids' : [owner_id]
		}

		Storage.add_value(
			file = "communityLikes",
			key = id,
			value = likes
		)

		posts = [User.is_logged_in()['username']] + ["Creation of Community"] + [randomFunctions.getDate()]
			
		Storage._create_file("communities\\communityPost" + id)
		Storage.add_value(
			file = "communities\\communityPost" + id,
			value = posts
		)
		owned_communities = Storage.get_value(
			file = 'communities_by_owner_id',
			key = owner_id
		)

		if owned_communities == None:
			owned_communities = [ id ]
		else:
			owned_communities.append( id )

		Storage.add_value(
			file = 'communities_by_owner_id',
			key = owner_id,
			value = owned_communities
		)

		Community.add_member_to_community(
			community_id = id,
			user_id = owner_id
		)

		return {
			'community': new_community
		}

	@staticmethod
	def add_member_to_community( community_id, user_id ):
		community = Community.get(
			id = community_id
		)

		if community != None:
			# { "user_id": [ community1, c2, c3, ... ] }
			members_by_user_id = Storage.get_value(
				file = 'community_members_by_user_id',
				key = user_id
			)

			# { "communuty_id": [ user1, u2, u3, ... ] }
			members_by_community_id = Storage.get_value(
				file = 'community_members_by_community_id',
				key = community_id
			)

			if members_by_user_id == None:
				members_by_user_id = [ community_id ]
			elif community_id not in members_by_user_id:
				members_by_user_id.append( community_id )

			if members_by_community_id == None:
				members_by_community_id = [ user_id ]
			elif user_id not in members_by_community_id:
				members_by_community_id.append( user_id )

			Storage.add_value(
				file = 'community_members_by_user_id',
				key = user_id,
				value = members_by_user_id
			)

			Storage.add_value(
				file = 'community_members_by_community_id',
				key = community_id,
				value = members_by_community_id
			)

			return True

		return False

	@staticmethod
	def remove_member_from_community( community_id, user_id ):
		community = Community.get(
			id = community_id
		)

		if community != None and community['owner_id'] != user_id:
			# { "user_id": [ community1, c2, c3, ... ] }
			members_by_user_id = Storage.get_value(
				file = 'community_members_by_user_id',
				key = user_id
			)

			# { "communuty_id": [ user1, u2, u3, ... ] }
			members_by_community_id = Storage.get_value(
				file = 'community_members_by_community_id',
				key = community_id
			)

			members_by_user_id.remove( community_id )
			members_by_community_id.remove( user_id )

			Storage.add_value(
				file = 'community_members_by_user_id',
				key = user_id,
				value = members_by_user_id
			)

			Storage.add_value(
				file = 'community_members_by_community_id',
				key = community_id,
				value = members_by_community_id
			)

	@staticmethod
	def delete_community( community_id, user_id ):
		community = Community.get(
			id = community_id
		)

		if community != None and community['owner_id'] == user_id:
			# Remove community from communities
			Storage.remove_value(
				file = 'communities',
				key = community_id
			)

			# @TODO	Loop members and remove values accordingly

			# Remove community from members by community ID { "community_id": [ id1, id2, ... ] }
			Storage.remove_value(
				file = 'community_members_by_community_id',
				key = community_id
			)

			Storage.remove_value(
				file = "communityLikes",
				key = community_id
			)
			Storage.remove_value(
				file = "communityPost",
				key = community_id
			)

			# Remove community from owner owned communities
			owned_communities = Storage.get_value(
				file = 'communities_by_owner_id',
				key = user_id
			)

			owned_communities.remove( community_id )

			Storage.add_value(
				file = 'communities_by_owner_id',
				key = user_id,
				value = owned_communities
			)

	@staticmethod
	def get_by_id( token ):
		pass