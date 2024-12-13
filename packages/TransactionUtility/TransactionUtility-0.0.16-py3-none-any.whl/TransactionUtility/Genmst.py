import cx_Oracle
from datetime import datetime
import loggerutility as logger
import json
import re

class Genmst:

    sql_models = []

    def insert_or_update_genmst(self, column, connection):
        
        required_keys = [
            'fld_name','mod_name','error_cd','blank_opt','fld_type'
        ]
        missing_keys = [key for key in required_keys if key not in column]
        logger.log(f"Missing required keys for genmst table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for genmst table: {', '.join(missing_keys)}")
        else:
            fld_name = column.get('fld_name', '')
            mod_name = column.get('mod_name', '').upper()
            descr = column.get('descr', '').strip() or ''
            error_cd = column.get('error_cd', '').strip() or ''
            blank_opt = column.get('blank_opt', '').strip() or ''
            fld_type = column.get('fld_type','').strip() or ''
            fld_min = column.get('fld_min', '')
            fld_max = column.get('fld_max', '')
            val_type = column.get('val_type', '')
            chg_date = datetime.now().strftime('%d-%m-%y')
            chg_user = column.get('chg_user', '').strip() or 'System'
            chg_term = column.get('chg_term', '').strip() or 'System'
            val_table = column.get('val_table', '')
            sql_input = column.get('sql_input', '')
            fld_width = column.get('fld_width', '')
            udf_usage_1 = column.get('udf_usage_1', '')
            udf_usage_2 = column.get('udf_usage_2', '')
            udf_usage_3 = column.get('udf_usage_3', '')
            val_stage = column.get('val_stage', '')
            obj_name = column.get('obj_name', '')[2:]
            form_no = column.get('form_no', '')
            action = column.get('action', '')
            user_id = column.get('user_id', '')
            tran_id = column.get('tran_id', '').strip() or ''
            udf_str1_descr = column.get('udf_str1_descr', '')
            udf_str2_descr = column.get('udf_str2_descr', '')
            udf_str3_descr = column.get('udf_str3_descr', '')
            exec_seq = column.get('exec_seq', '')

            # cursor = connection.cursor()
            # queryy = "SELECT COUNT(*) FROM genmst WHERE FLD_NAME = :fld_name and MOD_NAME = :mod_name"
            # cursor.execute(queryy,{'fld_name': fld_name,'mod_name': mod_name})
            # count = cursor.fetchone()[0]
            # logger.log(f"Inside count {count}")
            # cursor.close()
            # if count > 0:
            #     logger.log(f"Inside update :: {fld_name}")
            #     logger.log(f"Inside update :: {action}")
            #     cursor = connection.cursor()
            #     update_query = """
            #         UPDATE genmst SET
            #         FLD_NAME = :FLD_NAME, MOD_NAME = :MOD_NAME, DESCR = :DESCR, ERROR_CD = :ERROR_CD,
            #         BLANK_OPT = :BLANK_OPT, FLD_TYPE = :FLD_TYPE, FLD_MIN = :FLD_MIN, FLD_MAX = :FLD_MAX,
            #         VAL_TYPE = :VAL_TYPE, CHG_DATE = TO_DATE(:CHG_DATE, 'DD-MM-YYYY'), CHG_USER = :CHG_USER,
            #         CHG_TERM = :CHG_TERM, VAL_TABLE = :VAL_TABLE, SQL_INPUT = :SQL_INPUT, FLD_WIDTH = :FLD_WIDTH,
            #         UDF_USAGE_1 = :UDF_USAGE_1, UDF_USAGE_2 = :UDF_USAGE_2, UDF_USAGE_3 = :UDF_USAGE_3,
            #         VAL_STAGE = :VAL_STAGE, OBJ_NAME = :OBJ_NAME, FORM_NO = :FORM_NO, ACTION = :ACTION,
            #         USER_ID = :USER_ID, UDF_STR1_DESCR = :UDF_STR1_DESCR, UDF_STR2_DESCR = :UDF_STR2_DESCR,
            #         UDF_STR3_DESCR = :UDF_STR3_DESCR, EXEC_SEQ = :EXEC_SEQ
            #         WHERE FLD_NAME = :fld_name and MOD_NAME = :mod_name
            #     """
            #     cursor.execute(update_query, {
            #         'fld_name': fld_name,
            #         'mod_name': mod_name,
            #         'descr': descr[:40],
            #         'error_cd': error_cd,
            #         'blank_opt': blank_opt,
            #         'fld_type': fld_type,
            #         'fld_min': fld_min,
            #         'fld_max': fld_max,
            #         'val_type': val_type,
            #         'chg_date': chg_date,
            #         'chg_user': chg_user,
            #         'chg_term': chg_term,
            #         'val_table': val_table,
            #         'sql_input': sql_input,
            #         'fld_width': fld_width,
            #         'udf_usage_1': udf_usage_1,
            #         'udf_usage_2': udf_usage_2,
            #         'udf_usage_3': udf_usage_3,
            #         'val_stage': val_stage,
            #         'obj_name': obj_name,
            #         'form_no': form_no,
            #         'action': action ,
            #         'user_id': user_id ,
            #         'udf_str1_descr': udf_str1_descr,
            #         'udf_str2_descr': udf_str2_descr,
            #         'udf_str3_descr': udf_str3_descr,
            #         'exec_seq': exec_seq
            #     })
            #     cursor.close()
            #     logger.log(f"Updated: MOD_NAME = {mod_name}")
            # else:

            logger.log(f"Inside insert")
            cursor = connection.cursor()
            max_queryy = "SELECT MAX(tran_id) FROM genmst"
            cursor.execute(max_queryy)
            max_val = cursor.fetchone()[0]
            tran_id = self.add_one_to_numeric_part(max_val)
            cursor.close()

            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM messages 
                WHERE MSG_NO = :msg_no
            """, msg_no=error_cd)
            
            logger.log(f"msg_no Of messages ::: {error_cd}")
            count = cursor.fetchone()[0]
            logger.log(f"Count Of messages ::: {count}")
            cursor.close()
            if count == 0:
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO messages (
                        MSG_NO, MSG_STR, MSG_DESCR, MSG_TYPE, MSG_OPT, MSG_TIME, ALARM,
                        ERR_SOURCE, CHG_DATE, CHG_USER, CHG_TERM, OVERRIDE_INPUT, MAIL_OPTION
                    ) VALUES (
                        :msg_no, :msg_str, :msg_descr, :msg_type, :msg_opt, :msg_time, :alarm,
                        :err_source, TO_DATE(:chg_date, 'DD-MM-YYYY'), :chg_user, :chg_term,
                        :override_input, :mail_option
                    )
                """
                values = {
                    'msg_no': error_cd,
                    'msg_str': descr,
                    'msg_descr': descr,
                    'msg_type': 'E', 
                    'msg_opt': 'Y', 
                    'msg_time': '', 
                    'alarm': '',
                    'err_source': '',
                    "chg_date": datetime.now().strftime('%d-%m-%y'),
                    "chg_user": "System", 
                    "chg_term": "System",
                    'override_input': '', 
                    'mail_option': ''
                }

                cursor.execute(insert_query, values)
                cursor.close()

            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM SYSTEM_EVENTS 
                WHERE OBJ_NAME = :obj_name and EVENT_CODE = :event_code
            """, {'obj_name': obj_name,'event_code': 'post_validate'})
            
            count1 = cursor.fetchone()[0]
            logger.log(f"Inside SYSTEM_EVENTS {count1}")
            cursor.close()
            if count1 == 0:
                logger.log(f"Inside SYSTEM_EVENTS")
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO SYSTEM_EVENTS (
                        OBJ_NAME, EVENT_CODE, EVENT_CONTEXT, SERVICE_CODE, METHOD_RULE, OVERWRITE_CORE, 
                        CHG_DATE, CHG_USER, CHG_TERM, RESULT_HANDLE, COMP_TYPE, COMP_NAME, COMM_FORMAT
                    ) VALUES (
                        :obj_name, :event_code, :event_context, :service_code, :method_rule, :overwrite_core, 
                        TO_DATE(:chg_date, 'DD-MM-YYYY'), :chg_user, :chg_term, :result_handle, :comp_type, 
                        :comp_name, :comm_format
                    )
                """
                values = {
                    'obj_name': obj_name,
                    'event_code': 'post_validate',
                    'event_context': '1',
                    'service_code': 'post_gen_val',
                    'method_rule': None,
                    'overwrite_core': '0',
                    'chg_date': datetime.now().strftime('%d-%m-%y'),  
                    'chg_user': 'System',
                    'chg_term': 'System',
                    'result_handle': '2',
                    'comp_type': 'JB',
                    'comp_name': 'ibase.webitm.ejb.sys.GenValidate',
                    'comm_format': None
                }

                cursor.execute(insert_query, values)
                cursor.close()
                logger.log(f"Inserted :: {obj_name}")

            cursor = connection.cursor()
            insert_query = """
                INSERT INTO genmst (
                FLD_NAME, MOD_NAME, DESCR, ERROR_CD, BLANK_OPT, FLD_TYPE, FLD_MIN, FLD_MAX, VAL_TYPE,
                CHG_DATE, CHG_USER, CHG_TERM, VAL_TABLE, SQL_INPUT, FLD_WIDTH, UDF_USAGE_1, UDF_USAGE_2,
                UDF_USAGE_3, VAL_STAGE, OBJ_NAME, FORM_NO, ACTION, USER_ID, TRAN_ID, UDF_STR1_DESCR,
                UDF_STR2_DESCR, UDF_STR3_DESCR, EXEC_SEQ
                ) VALUES (
                :fld_name, :mod_name, :descr, :error_cd, :blank_opt, :fld_type, :fld_min, :fld_max, :val_type,
                TO_DATE(:chg_date, 'DD-MM-YYYY'), :chg_user, :chg_term, :val_table, :sql_input, :fld_width,
                :udf_usage_1, :udf_usage_2, :udf_usage_3, :val_stage, :obj_name, :form_no, :action, :user_id,
                :tran_id, :udf_str1_descr, :udf_str2_descr, :udf_str3_descr, :exec_seq
                )
            """

            logger.log(f"msg_no Of genmst ::: {error_cd}")
            logger.log(f"Insert genmst query = {insert_query}")
            values = {
                'fld_name': fld_name,
                'mod_name': mod_name,
                'descr': descr[:40],
                'error_cd': error_cd,
                'blank_opt': blank_opt,
                'fld_type': fld_type,
                'fld_min': fld_min,
                'fld_max': fld_max,
                'val_type': val_type,
                'chg_date': chg_date,
                'chg_user': chg_user,
                'chg_term': chg_term,
                'val_table': val_table,
                'sql_input': sql_input,
                'fld_width': fld_width,
                'udf_usage_1': udf_usage_1,
                'udf_usage_2': udf_usage_2,
                'udf_usage_3': udf_usage_3,
                'val_stage': val_stage,
                'obj_name': obj_name,
                'form_no': form_no,
                'action': action ,
                'user_id': user_id ,
                'tran_id': tran_id ,
                'udf_str1_descr': udf_str1_descr,
                'udf_str2_descr': udf_str2_descr,
                'udf_str3_descr': udf_str3_descr,
                'exec_seq': exec_seq
            }
            logger.log(f"values ::: {values}")
            cursor.execute(insert_query, {
                'fld_name': fld_name,
                'mod_name': mod_name,
                'descr': descr[:40],
                'error_cd': error_cd,
                'blank_opt': blank_opt,
                'fld_type': fld_type,
                'fld_min': fld_min,
                'fld_max': fld_max,
                'val_type': val_type,
                'chg_date': chg_date,
                'chg_user': chg_user,
                'chg_term': chg_term,
                'val_table': val_table,
                'sql_input': sql_input,
                'fld_width': fld_width,
                'udf_usage_1': udf_usage_1,
                'udf_usage_2': udf_usage_2,
                'udf_usage_3': udf_usage_3,
                'val_stage': val_stage,
                'obj_name': obj_name,
                'form_no': form_no,
                'action': action ,
                'user_id': user_id ,
                'tran_id': tran_id ,
                'udf_str1_descr': udf_str1_descr,
                'udf_str2_descr': udf_str2_descr,
                'udf_str3_descr': udf_str3_descr,
                'exec_seq': exec_seq
            })
            cursor.close()
            logger.log(f"Inserted: MOD_NAME = {mod_name}")

    def is_valid_json(self, data):
        if isinstance(data, dict):
            return True
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
        
    def add_one_to_numeric_part(self, value):
        numeric_part = re.findall(r'\d+', value)
        if numeric_part:
            num = int(numeric_part[0]) + 1
            num_str = str(num).zfill(len(numeric_part[0]))
            return re.sub(r'\d+', num_str, value, 1)
        else:
            return value
        
    def process_data(self, conn, sql_models_data):
        logger.log(f"Start of Genmst Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            if "sql_model" in sql_model and "columns" in sql_model['sql_model']:
                for columns in sql_model['sql_model']['columns']:
                    if "column" in columns and "validations" in columns['column']:
                        validations = columns['column']['validations']
                        for column in validations:
                            if self.is_valid_json(column):
                                self.insert_or_update_genmst(column, conn)
        logger.log(f"End of Genmst Class")

