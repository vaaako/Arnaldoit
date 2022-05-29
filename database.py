import sqlite3
from flask import g

DATABASE = 'arnaldata.db'
# 
def query_db(query, args=(), one=False):
	cursor = get_db().execute(query, args) # Query
	rv = cursor.fetchall() # Fetch all results from query
	cursor.close() # Close
	return (rv[0] if rv else None) if one else rv # Return all posts from db

def get_db():
	db = getattr(g, '_database', None) # Check if exists

	if db is None: 
		db = g._database = sqlite3.connect(DATABASE) # Create connection
	return db # Return db


def create_post(request, reply=False):
	if reply:
		query = ''' INSERT INTO replies(user, date, board, post_text, image_file, replying_to, id) values (?,?,?,?,?,?,?) '''
	else:
		query = ''' INSERT INTO posts(id, date, content, filename) VALUES (?, ?, ?, ?) '''

	cursor = get_db().cursor() # Cursor to query db
	cursor.execute(query, request) # Assemble query
	get_db().commit() # Commit changes to db 
	cursor.close() # Close cursor
	return cursor.lastrowid # Return last row id

