from utils.db import execute_query

class PatientRecords:
    def __init__(self):
        super(PatientRecords, self).__init__()

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

                SELECT * FROM PATIENT_RECORDS;

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

                SELECT * FROM PATIENT_RECORDS WHERE nric_fin='G12345678N';

            |
        '''

        query = f"SELECT * FROM PATIENT_RECORD WHERE nric_fin='{nric}';"
        results = execute_query(query)

        return results

    def update_by_key(self, nric, attributes):
        pass

