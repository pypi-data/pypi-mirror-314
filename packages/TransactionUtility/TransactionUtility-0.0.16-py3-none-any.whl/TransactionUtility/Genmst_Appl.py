import cx_Oracle
import loggerutility as logger

class Genmst_Appl:

    data_to_insert = [
        {'TRAN_ID':'T1','LINE_NO':9,'SCOPE':'z','SCOPE_DATA':'z'},
        {'TRAN_ID':'T2','LINE_NO':99,'SCOPE':'Z','SCOPE_DATA':'Z'}
    ]

    def check_and_update_tran_id(self, tran_data, connection):
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM genmst_appl 
            WHERE TRAN_ID = :tran_id
        """, tran_id=tran_data['TRAN_ID'])
        count = cursor.fetchone()[0]

        if count > 0:
            update_query = """
            UPDATE genmst_appl SET
            LINE_NO = :line_no,
            SCOPE = :scope,
            SCOPE_DATA = :scope_data
            WHERE TRAN_ID = :tran_id
            """
            cursor.execute(update_query, tran_data)
            logger.log(f"Updated: TRAN_ID {tran_data['TRAN_ID']}")
        else:
            insert_query = """
            INSERT INTO genmst_appl (
            TRAN_ID, LINE_NO, SCOPE, SCOPE_DATA
            ) VALUES (
            :tran_id, :line_no, :scope, :scope_data
            )
            """
            cursor.execute(insert_query, tran_data)
            logger.log(f"Inserted: TRAN_ID {tran_data['TRAN_ID']}")
        cursor.close()

    def process_data(self, conn):
        for data in self.data_to_insert:
            self.check_and_update_tran_id(data, conn)
