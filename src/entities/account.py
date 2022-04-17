from utils.db import execute_query

class Account:
    def __init__(self):
        super(Account, self).__init__()
        self._fields = [
            "account_id", "password", "fname", "lname", "hospital_name"
        ]

    def list(self):
        '''
            | @Route None
            | @Access Private
            | @Desc List all rows in the ACCOUNT table.
            
            .. code-block:: python

                from src.entities.account import Account

                ac_entity = Account()
                ac_entity.list()

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT * FROM ACCOUNT;

            |
        '''
        query = "SELECT * FROM ACCOUNT;"
        results = execute_query(query)

        return results

    def list_by_key(self, account_id):
        '''
            | @Route None
            | @Access Private
            | @Desc List account information given an account id.
            
            .. code-block:: python

                from src.entities.account import Account

                ac_entity = Account()
                ac_entity.list_by_key('nong003')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT * FROM ACCOUNT WHERE account_id='nong003';

            |
        '''
        query = f"SELECT * FROM ACCOUNT WHERE account_id='{account_id}'"
        results = execute_query(query)

        return results