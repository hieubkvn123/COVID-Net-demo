from utils.db import execute_query

class Diagnosis:
    def __init__(self):
        super(Diagnosis, self).__init__()
        self._fields = [
            "patient_nric_fin", "bystaff_account_id", "date_time",
            "result", "confidence", "xray_img_url"
        ]

    def get_by_id_and_datetime(self, nric, datetime):
        '''
            | @Route None
            | @Access Private
            | @Desc List a particular diagnosis result given the patient's NRIC and date when the
              diagnosis is created
        '''

        query = f'SELECT * FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin  WHERE pr.nric_fin="{nric}" and d.date_time="{datetime}"'
        results = execute_query(query)

        return results


    def list_by_id(self, nric):
        '''
            | @Route None
            | @Access Private
            | @Desc List all diagnosis history of a patient given the patient's NRIC.

            .. code-block:: python 
            
                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.list_by_id('G1778418N')
            
            | is equivalent to the following SQLite3 command 

            .. code-block:: sql

                SELECT * FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin  WHERE pr.nric_fin='G1778418N' ORDER BY d.date_time;
        '''
        query = f'SELECT * FROM DIAGNOSIS d JOIN PATIENT_RECORD pr ON d.patient_nric_fin=pr.nric_fin  WHERE pr.nric_fin="{nric}" ORDER BY d.date_time;'
        results = execute_query(query)

        return results

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

    def modify_diagnosis_nric(self, old_nric, new_nric, date_time):
        '''
            | @Route None
            | @Access Private 
            | @Desc This function is dedicated to the case when the nurse created a diagnosis with a wrong NRIC
              and wish to modify the NRIC of the corresponding diagnosis.

            .. code-block:: python
                
                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.modify_diagnosis_nric('G12345678N', 'G87654321N', '2022-04-15 00:00:00')

            | is equivalent to the following SQLite3 command:
            
            .. code-block:: sql
                
                UPDATE DIAGNOSIS SET patient_nric_fin='G87654321N' WHERE patient_nric_fin='G12345678N' AND date_time='2022-04-15 00:00:00';
            
            |

        '''
        query = f'UPDATE DIAGNOSIS SET patient_nric_fin="{new_nric}" WHERE patient_nric_fin="{old_nric}" AND date_time="{date_time}"'
        results = execute_query(query, type="update")

        return results

    def delete_by_key_and_datetime(self, nric, date_time):
        '''
            | @Route None
            | @Access Private
            | @Desc Delete a particular patient's diagnosis result in case the result is faulty or the x-ray is mistaken.

            .. code-block:: python
                
                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.modify_diagnosis_nric('G12345678N', 'G87654321N', '2022-04-15 00:00:00')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                DELETE FROM DIAGNOSIS WHERE patient_nric_fin='G12345678N' AND date_time='2022-04-15 00:00:00';

            |

        '''

        query = f'DELETE FROM DIAGNOSIS WHERE patient_nric_fin="{nric}" AND date_time="{date_time}"'
        results = execute_query(query, type="delete")

        return results