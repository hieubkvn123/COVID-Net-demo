from utils.db import execute_query

class PatientRecords:
    def __init__(self):
        super(PatientRecords, self).__init__()
        self._fields = [
            "nric_fin", "phone", "fname", "lname", "gender", "dob"
        ]

    def list(self):
        '''
            | @Route None
            | @Access Private
            | @Desc List all of the records with all fields from the PATIENT_RECORD table. The following code 
              sample
            
            .. code-block:: python

                from src.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                pr_entity.list()

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT * FROM PATIENT_RECORD;

            |
        '''
        query = f"SELECT * FROM PATIENT_RECORD;"
        results = execute_query(query)

        return results 

    def list_by_key(self, nric):
        '''
            | @Route None
            | @Access Private
            | @Desc List a specific patient record with the given NRIC.
            
            .. code-block:: python

                from src.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                pr_entity.list_by_key('G12345678N')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT * FROM PATIENT_RECORD WHERE nric_fin='G12345678N';

            |
        '''

        query = f"SELECT * FROM PATIENT_RECORD WHERE nric_fin='{nric}';"
        results = execute_query(query)

        return results

    def _construct_update_key_vals_pairs(self, attributes):
        '''
            | @Route None
            | @Access None
            | @Desc An utility function, used to construct pairs of key-value 
              for the update query in SQLite3. For example,

            .. code-block:: python
            
                from src.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                attributes = { 'fname' : 'Nong', 'lname' : 'Hieu' }
                
                # Returns 'fname="Nong", lname="Hieu"'
                pr_entity._construct_update_key_vals_pairs(attributes)
                
            |
        '''
        return ",".join(f'{key}="{value}"' for key, value in attributes.items())

    def update_by_key(self, nric, attributes):
        '''
            | @Route None
            | @Access Private
            | @Desc Update a patient record given the NRIC and the list of attributes.
            
            .. code-block:: python

                from src.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                pr_entity.update_by_key('G12345678N', {'fname' : 'Nong', 'lname' : 'Hieu'})

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                UPDATE PATIENT_RECORD SET fname="Nong", lname="Hieu" WHERE nric_fin="G12345678N";

            |
        '''

        query_format = 'UPDATE PATIENT_RECORD SET {} WHERE nric_fin="{}";'
        query = query_format.format(self._construct_update_key_vals_pairs(attributes), nric)
        results = execute_query(query, type="update")

        return results

    def insert(self, nric, fname, lname, dob, gender, phone):
        '''
            | @Route None
            | @Access Private
            | @Desc Insert into PATIENT_RECORD given a full set of attributes.
            
            .. code-block:: python

                from src.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                pr_entity.insert('G12345678N', 'Nong', 'Hieu', '2000-04-30', 'Male', '88720435')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                INSERT INTO PATIENT_RECORD VALUES('G12345678N', 'Nong', 'Hieu', '2000-04-30', 'Male', '88720435');

            |
        '''

        query = f'INSERT INTO PATIENT_RECORD VALUES("{nric}", "{phone}", "{fname}", "{lname}", "{gender}", "{dob}");'
        results = execute_query(query, type="insert")

        return results