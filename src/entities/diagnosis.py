from utils.db import execute_query

class Diagnosis:
    def __init__(self):
        super(Diagnosis, self).__init__()
        self._fields = [
            "patient_nric_fin", "bystaff_account_id", "date_time",
            "result", "confidence", "xray_img_url"
        ]

    def list(self):
        '''
            | @Route None
            | @Access Private
            | @Desc List all of the diagnosis records from DIAGNOSIS and PATIENT_RECORD. The tables DIAGNOSIS
              and PATIENT_RECORD are linked together by a foreign key "nric_fin". When listed, both information 
              from the DIAGNOSIS and the PATIENT_RECORD tables will be displayed.
            
            .. code-block:: python

                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.list()

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT * FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin ORDER BY d.date_time;

            |
        '''
        query = "SELECT * FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin ORDER BY d.date_time;"
        results = execute_query(query)

        return results

    def insert(self, nric, by_staff_id, date_time, result, confidence, xray_img_url): 
        '''
            | @Route None
            | @Access Private
            | @Desc Insert into DIAGNOSIS given a full set of attributes.
            
            .. code-block:: python

                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.insert('G12345678N', 'nong003', '2022-04-13', 'negative', 0.83, '/static/images/G12345678N/sample.png')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                INSERT INTO DIAGNOSIS VALUES('G12345678N', 'nong003', '2022-04-13', 'negative', 0.83, '/static/images/G12345678N/sample.png');

            |
        '''

        query = f'INSERT INTO DIAGNOSIS VALUES("{nric}", "{by_staff_id}", "{date_time}", "{result}", {confidence}, "{xray_img_url}");'
        results = execute_query(query, type="insert")

        return results