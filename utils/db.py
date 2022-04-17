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
		  instance and cursor for concise syntax. The following scenarios will apply for execution of SQLite3 queries

		| 1. Query executed successfully, no payload returned (insert, update, delete)
		
		.. code-block:: python

			response = {
				'_code' : 'query_committed'
			}

		| 2. Query executed successfully, payload returned (select)

		.. code-block:: python
			
			response = {
				'_code' : 'query_committed',
				'payload' : [
					{'field_1' : 'value_1', ...}, # Row 1
					{'field_1' : 'value_1', ...}  # Row 2
				]
			}

		| 3. Query failed

		.. code-block:: python

			response = {
				'_code' : 'query_error',
				'err_type' : '<Exception Class>',
				'err_msg' : '<Exception Message>',
				'err_trace' : '<Exception Traceback'
			}
			
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

				return { "_code" : "query_committed" }
			except:
				traceback.print_exc(file=sys.stdout)
				ex_type, ex_value, ex_traceback = sys.exc_info()
				return { 
					"_code" : "query_error", 
					"err_type" : str(ex_type),
					"err_msg" : str(ex_value),
					"err_trace" : str(ex_traceback)
				}

		cursor.close()

		return { "_code" : "query_committed", "payload" : rows }
	except: 
		traceback.print_exc(file=sys.stdout)
		ex_type, ex_value, ex_traceback = sys.exc_info()
		return { 
			"_code" : "query_error", 
			"err_type" : str(ex_type),
			"err_msg" : str(ex_value),
			"err_trace" : str(ex_traceback)
		}