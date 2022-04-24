import json
import os
import pathlib
import json

class Storage:	
	@staticmethod
	def adjustValue(file, key = None, value = None, newChange = 0):
		if value != None:
			filePath = "data/" + file + ".json"
			with open(filePath, "r") as f:
				readDocument = json.loads(f.read())

			readDocument[key][value] = newChange

			with open(filePath, "w") as f:
				jsonFormat = json.dumps(readDocument)
				f.write(jsonFormat)
		elif value == None and key == None:
			filePath = "data/" + file + ".json"
			with open(filePath, "r") as f:
				readDocument = json.loads(f.read())

			readDocument = readDocument + newChange

			with open(filePath, "w") as f:
				jsonFormat = json.dumps(readDocument)
				f.write(jsonFormat)

		elif value == None:
			filePath = "data/" + file + ".json"
			with open(filePath, "r") as f:
				readDocument = json.loads(f.read())

			readDocument[key] = newChange

			with open(filePath, "w") as f:
				jsonFormat = json.dumps(readDocument)
				f.write(jsonFormat)

		

	@staticmethod
	def add_value( file, key = None, value = None ):
		if not os.path.isfile( Storage._get_full_path( file ) ):
			Storage._create_file( file )

		_file = open( Storage._get_full_path( file ), 'r' )
		_data = json.load( _file )

		if key != None:
			_data[ key ] = value
		else:
			_data = value

		with open( Storage._get_full_path( file ), 'w' ) as f:
			json.dump( _data, f )

	@staticmethod
	def get_value( file, key = None ):
		if not os.path.isfile( Storage._get_full_path( file ) ):
			Storage._create_file( file )

		_file = open( Storage._get_full_path( file ), 'r' )
		_data = json.load( _file )

		if key != None and key in _data:
			return _data[ key ]
		elif key == None:
			return _data

		return None

	@staticmethod
	def remove_value( file, key ):
		if not os.path.isfile( Storage._get_full_path( file ) ):
			Storage._create_file( file )
		
		_file = open( Storage._get_full_path( file ), 'r' )
		_data = json.load( _file )

		_data.pop( key, None )

		with open( Storage._get_full_path( file ), 'w' ) as f:
			json.dump( _data, f )

	@staticmethod
	def _create_file( file ):
		new_file = open( Storage._get_full_path( file ), 'w' )
		new_file.write( '{}' )
		new_file.close()

	@staticmethod
	def _get_full_path( file ):
		file = file + '.json'
		storage_util_fp = os.path.dirname( os.path.abspath( __file__ ) )
		return os.path.join(
			pathlib.Path( storage_util_fp ).parents[1],
			'data',
			file
		)
	@staticmethod
	def deleteFile(filePath):
		os.remove(filePath + ".json")