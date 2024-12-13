import cx_Oracle
import loggerutility as logger
import json

class Obj_Itemchange:
    
    sql_models = []
        
    def is_valid_json(self, data):
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    def check_or_update_obj_itemchange(self, item_change,connection):

        required_keys = ['obj_name', 'form_no', 'field_name']
        missing_keys = [key for key in required_keys if key not in item_change]
        logger.log(f"Missing required keys for obj_itemchange table: {missing_keys}")

        if missing_keys:
            raise KeyError(f"Missing required keys for obj_itemchange table: {', '.join(missing_keys)}")
        else:
            obj_name = item_change.get('obj_name', '')
            form_no = item_change.get('form_no', '')
            field_name = item_change.get('field_name', '')
            mandatory = item_change.get('mandatory_server', '')
            exec_at = item_change.get('exec_at', '')
            js_arg = item_change.get('js_arg', '')
        
            cursor = connection.cursor()
            queryy = f"""
                SELECT COUNT(*) FROM obj_itemchange 
                WHERE OBJ_NAME = '{obj_name}'
                AND FORM_NO =  '{form_no}'
                AND FIELD_NAME =  '{field_name}'
            """
            cursor.execute(queryy)
            count = cursor.fetchone()[0]
            if count > 0:
                update_query = """
                    UPDATE obj_itemchange SET
                    MANDATORY = :mandatory,
                    EXEC_AT = :exec_at,
                    JS_ARG = :js_arg
                    WHERE OBJ_NAME = :obj_name 
                    AND FORM_NO = :form_no
                    AND FIELD_NAME = :field_name
                """
                cursor.execute(update_query, {
                    'obj_name': obj_name,
                    'form_no': form_no,
                    'field_name': field_name,
                    'mandatory': mandatory,
                    'exec_at': exec_at,
                    'js_arg': js_arg
                })
            else:
                insert_query = """
                                INSERT INTO obj_itemchange (
                                OBJ_NAME, FORM_NO, FIELD_NAME, MANDATORY, EXEC_AT, JS_ARG
                                ) VALUES (:obj_name, :form_no, :field_name, :mandatory, :exec_at, :js_arg)
                            """
                
                cursor.execute(insert_query, {
                    'obj_name': obj_name,
                    'form_no': form_no,
                    'field_name': field_name,
                    'mandatory': mandatory,
                    'exec_at': exec_at,
                    'js_arg': js_arg
                })
            cursor.close()

    def process_data(self, conn, sql_models_data):
        logger.log(f"Start of Obj_Itemchange Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            if "sql_model" in sql_model and "columns" in sql_model['sql_model']:
                for column in sql_model['sql_model']['columns']:
                    if "column" in column and "item_change" in column['column']:
                        item_change = column['column']['item_change']
                        if self.is_valid_json(item_change):
                            self.check_or_update_obj_itemchange(item_change, conn)
        logger.log(f"End of Obj_Itemchange Class")