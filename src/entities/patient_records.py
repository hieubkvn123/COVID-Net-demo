from utils.db import execute_query

class PatientRecordsEntity:
    def __init__(self):
        super(PatientRecordsEntity, self).__init__()

    def list(self):
        '''
            |@Route None
            |@Access Private
            |@Desc List all of the records with all fields from the PATIENT_RECORD table. The following code 
             sample
            
            .. code-block:: python
                from modules.entities.patient_records import PatientRecords

                pr_entity = PatientRecords()
                pr_entity.list()

            |is equivalent to the following SQLite3 command:

            .. highlight:: sql

                ::
                SELECT * FROM PATIENT_RECORDS;
            |
        '''