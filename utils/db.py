import sys
import sqlite3
import traceback
from flask import g, jsonify
from config import DATABASE

# For getting sqlite database cursor
def make_dicts(cursor, row):
	'''
		| @Route None
		| @Access None
		| @Desc : An utility function. Convert the SQLite3 query results to a list of dictionaries where
		  each column name is a key in the dictionary.
	'''
	return dict((cursor.description[idx][0], value)
				for idx, value in enumerate(row))

def get_db():
	'''
		| @Route None
		| @Access None
		| @Desc : Get the SQLite3 connection instance.
	'''
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)

	db.row_factory = make_dicts
	return db

def execute_query(query, type=None):
	'''
		| @Route None
		| @Access None
		| @Desc : A shortcut function to execute an SQLite3 query without explicitly creating a connection
		  instance and cursor for concise syntax.
	'''

	try:
		conn = get_db()
		cursor = conn.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()

		if(type in ['delete', 'update', 'insert']):
			try:
				conn.commit()
				cursor.close()

				return "query_committed"
			except:
				traceback.print_exc(file=sys.stdout)
				return "query_error"

		cursor.close()

		return rows
	except: 
		traceback.print_exc(file=sys.stdout)
		return "query_error"