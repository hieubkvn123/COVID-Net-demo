from datetime import datetime
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
              from the DIAGNOSIS and the PATIENT_RECORD tables will be displayed even for the patient records
              without any diagnosis results.
            
            .. code-block:: python

                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.list()

            | is equivalent to the following SQLite3 command (Full outer join PATIENT_RECORD and DIAGNOSIS by NRIC/FIN):

            .. code-block:: sql

                SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, d.result 
                    FROM DIAGNOSIS d 
                    JOIN PATIENT_RECORD pr 
                    ON d.patient_nric_fin=pr.nric_fin 
                    UNION ALL 
                    SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, "None"
                    FROM PATIENT_RECORD pr 
                    LEFT JOIN DIAGNOSIS d 
                    ON d.patient_nric_fin=pr.nric_fin WHERE d.patient_nric_fin IS NULL 
                    ORDER BY d.date_time;

            |
        '''
        query = """SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, d.result 
                    FROM DIAGNOSIS d 
                    JOIN PATIENT_RECORD pr 
                    ON d.patient_nric_fin=pr.nric_fin 
                    UNION ALL 
                    SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, "None"
                    FROM PATIENT_RECORD pr 
                    LEFT JOIN DIAGNOSIS d 
                    ON d.patient_nric_fin=pr.nric_fin WHERE d.patient_nric_fin IS NULL 
                    ORDER BY d.date_time;"""

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

    def search(self, nric, fname, lname, date, result):
        '''
            | @Route None
            | @Access Private
            | @Desc Search diagnosis records based on nric, first name, last name, date when diagnosed and diagnosis result.

            .. code-block:: python
                
                from src.entities.diagnosis import Diagnosis

                dn_entity = Diagnosis()
                dn_entity.search('G12345678N', 'Nong', 'Hieu', '2022-04-15', 'positive')

            | is equivalent to the following SQLite3 command:

            .. code-block:: sql

                SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, d.result 
                    FROM DIAGNOSIS d 
                    JOIN PATIENT_RECORD pr 
                    ON d.patient_nric_fin=pr.nric_fin 
                    WHERE pr.nric_fin LIKE '%G12345678N%' 
                    AND pr.fname LIKE '%Nong%'
                    AND pr.lname LIKE '%Hieu%'
                    AND TO_DATE(d.date_time) = '2022-04-15'
                    AND d.result = 'positive';
            |

        '''
        result = "" if result.lower() != "positive" and result.lower() != "negative" else result
        if(date == "" or date is None):
            query_format = '''SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, d.result 
                        FROM DIAGNOSIS d 
                        JOIN PATIENT_RECORD pr 
                        ON d.patient_nric_fin=pr.nric_fin 
                        WHERE pr.nric_fin LIKE '%{}%' 
                        AND pr.fname LIKE '%{}%'
                        AND pr.lname LIKE '%{}%'
                        AND d.result LIKE '%{}%';
            '''
            query = query_format.format(nric, fname, lname, result)
        else:
            query_format = '''SELECT pr.nric_fin, pr.fname, pr.lname, d.date_time, d.result 
                        FROM DIAGNOSIS d 
                        JOIN PATIENT_RECORD pr 
                        ON d.patient_nric_fin=pr.nric_fin 
                        WHERE pr.nric_fin LIKE '%{}%' 
                        AND strftime('%Y-%m-%d', d.date_time) == '{}'
                        AND pr.fname LIKE '%{}%'
                        AND pr.lname LIKE '%{}%'
                        AND d.result LIKE '%{}%';
            '''
            query = query_format.format(nric, date, fname, lname, result)

        results = execute_query(query)

        return results