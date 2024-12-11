import cx_Oracle
from datetime import datetime
import loggerutility as logger

class Pophelp:
    
    sql_models = []

    def check_or_update_pophelp(self, lookup, connection):

        required_keys = [
            'field_name', 'mod_name'
        ]

        missing_keys = [key for key in required_keys if key not in lookup]
        logger.log(f"Missing required keys for pophelp table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for pophelp table: {', '.join(missing_keys)}")
        else:
            field_name = lookup.get('field_name', '')
            mod_name = lookup.get('mod_name', '')
            sql_str = lookup.get('sql_str', '')
            dw_object = lookup.get('dw_object', '')
            msg_title = lookup.get('msg_title', '')
            width = lookup.get('width', '')
            height = lookup.get('height', '')
            chg_date = datetime.now().strftime('%d-%m-%y')
            chg_user = lookup.get('chg_user', '').strip() or 'System'
            chg_term = lookup.get('chg_term', '').strip() or 'System'
            dist_opt = lookup.get('dist_opt', '')
            filter_string = lookup.get('filter_string', '')
            sql_input = lookup.get('sql_input', '')
            default_col = lookup.get('default_col', '')
            pop_align = lookup.get('pop_align', '')
            query_mode = lookup.get('query_mode', '')
            page_context = lookup.get('page_context', '')
            pophelp_cols = lookup.get('pophelp_cols', '')
            pophelp_source = lookup.get('pophelp_source', '')
            multi_opt = lookup.get('multi_opt', '')
            help_option = lookup.get('help_option', '')
            popup_xsl_name = lookup.get('popup_xsl_name', '')
            auto_fill_len = lookup.get('auto_fill_len', '')
            thumb_obj = lookup.get('thumb_obj', '')
            thumb_image_col = lookup.get('thumb_image_col', '')
            thumb_alt_col = lookup.get('thumb_alt_col', '')
            auto_min_length = lookup.get('auto_min_length', '')
            obj_name__ds = lookup.get('obj_name__ds', '')
            data_model_name = lookup.get('data_model_name', '')
            validate_data = lookup.get('validate_data', '')
            item_change = lookup.get('item_change', '')
            msg_no = lookup.get('msg_no', '')
            filter_expr = lookup.get('filter_expr', '')
            layout = lookup.get('layout', '')

            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pophelp 
                WHERE FIELD_NAME = :field_name AND MOD_NAME = :mod_name
            """, field_name=field_name, mod_name=mod_name)
            count = cursor.fetchone()[0]
            if count > 0:
                update_query = """
                    UPDATE pophelp SET
                    SQL_STR = :sql_str, DW_OBJECT = :dw_object, 
                    MSG_TITLE = :msg_title, WIDTH = :width, HEIGHT = :height, 
                    CHG_DATE = TO_DATE(:chg_date, 'DD-MM-YYYY'), CHG_USER = :chg_user, 
                    CHG_TERM = :chg_term, DIST_OPT = :dist_opt, FILTER_STRING = :filter_string, 
                    SQL_INPUT = :sql_input, DEFAULT_COL = :default_col, POP_ALIGN = :pop_align, 
                    QUERY_MODE = :query_mode, PAGE_CONTEXT = :page_context, 
                    POPHELP_COLS = :pophelp_cols, POPHELP_SOURCE = :pophelp_source, 
                    MULTI_OPT = :multi_opt, HELP_OPTION = :help_option, 
                    POPUP_XSL_NAME = :popup_xsl_name, AUTO_FILL_LEN = :auto_fill_len, 
                    THUMB_OBJ = :thumb_obj, THUMB_IMAGE_COL = :thumb_image_col, 
                    THUMB_ALT_COL = :thumb_alt_col, AUTO_MIN_LENGTH = :auto_min_length, 
                    OBJ_NAME__DS = :obj_name__ds, DATA_MODEL_NAME = :data_model_name, 
                    VALIDATE_DATA = :validate_data, ITEM_CHANGE = :item_change, 
                    MSG_NO = :msg_no, FILTER_EXPR = :filter_expr, LAYOUT = :layout
                    WHERE FIELD_NAME = :field_name AND MOD_NAME = :mod_name
                """
                cursor.execute(update_query, {
                    'field_name': field_name, 'mod_name': mod_name, 'sql_str': sql_str, 'dw_object': dw_object, 'msg_title': msg_title, 'width': width, 'height': height,
                    'chg_date': chg_date, 'chg_user': chg_user, 'chg_term': chg_term, 'dist_opt': dist_opt, 'filter_string': filter_string, 'sql_input': sql_input,
                    'default_col': default_col, 'pop_align': pop_align, 'query_mode': query_mode, 'page_context': page_context, 'pophelp_cols': pophelp_cols, 
                    'pophelp_source': pophelp_source, 'multi_opt': multi_opt, 'help_option': help_option, 'popup_xsl_name': popup_xsl_name, 'auto_fill_len': auto_fill_len,
                    'thumb_obj': thumb_obj, 'thumb_image_col': thumb_image_col, 'thumb_alt_col': thumb_alt_col, 'auto_min_length': auto_min_length,
                    'obj_name__ds': obj_name__ds, 'data_model_name': data_model_name, 'validate_data': validate_data, 'item_change': item_change, 'msg_no': msg_no, 
                    'filter_expr': filter_expr, 'layout': layout
                })
                logger.log(f"Updated: FIELD_NAME={field_name} and MOD_NAME={mod_name}")
            else:
                insert_query = """
                    INSERT INTO pophelp (
                        FIELD_NAME, MOD_NAME, SQL_STR, DW_OBJECT, MSG_TITLE, WIDTH, HEIGHT, 
                        CHG_DATE, CHG_USER, CHG_TERM, DIST_OPT, FILTER_STRING, SQL_INPUT, 
                        DEFAULT_COL, POP_ALIGN, QUERY_MODE, PAGE_CONTEXT, POPHELP_COLS, 
                        POPHELP_SOURCE, MULTI_OPT, HELP_OPTION, POPUP_XSL_NAME, AUTO_FILL_LEN, 
                        THUMB_OBJ, THUMB_IMAGE_COL, THUMB_ALT_COL, AUTO_MIN_LENGTH, 
                        OBJ_NAME__DS, DATA_MODEL_NAME, VALIDATE_DATA, ITEM_CHANGE, MSG_NO, 
                        FILTER_EXPR, LAYOUT
                    ) 
                    VALUES (
                        :field_name, :mod_name, :sql_str, :dw_object, :msg_title, :width, :height, 
                        TO_DATE(:chg_date, 'DD-MM-YYYY'), :chg_user, :chg_term, :dist_opt, :filter_string, :sql_input, 
                        :default_col, :pop_align, :query_mode, :page_context, :pophelp_cols, 
                        :pophelp_source, :multi_opt, :help_option, :popup_xsl_name, :auto_fill_len, 
                        :thumb_obj, :thumb_image_col, :thumb_alt_col, :auto_min_length, 
                        :obj_name__ds, :data_model_name, :validate_data, :item_change, :msg_no, 
                        :filter_expr, :layout
                    )
                """

                cursor.execute(insert_query, {
                    'field_name': field_name, 'mod_name': mod_name, 'sql_str': sql_str, 'dw_object': dw_object, 'msg_title': msg_title, 'width': width, 'height': height,
                    'chg_date': chg_date, 'chg_user': chg_user, 'chg_term': chg_term, 'dist_opt': dist_opt, 'filter_string': filter_string, 'sql_input': sql_input,
                    'default_col': default_col, 'pop_align': pop_align, 'query_mode': query_mode, 'page_context': page_context, 'pophelp_cols': pophelp_cols, 
                    'pophelp_source': pophelp_source, 'multi_opt': multi_opt, 'help_option': help_option, 'popup_xsl_name': popup_xsl_name, 'auto_fill_len': auto_fill_len,
                    'thumb_obj': thumb_obj, 'thumb_image_col': thumb_image_col, 'thumb_alt_col': thumb_alt_col, 'auto_min_length': auto_min_length,
                    'obj_name__ds': obj_name__ds, 'data_model_name': data_model_name, 'validate_data': validate_data, 'item_change': item_change, 'msg_no': msg_no, 
                    'filter_expr': filter_expr, 'layout': layout
                })

                logger.log(f"Inserted: FIELD_NAME={field_name} and MOD_NAME={mod_name}")
            cursor.close()

    def process_data(self, conn, sql_models_data):
        logger.log(f"Start of Pophelp Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            if "sql_model" in sql_model and "columns" in sql_model['sql_model']:
                for column in sql_model['sql_model']['columns']:
                    lookup = column['column']['lookup']
                    if lookup:
                        self.check_or_update_pophelp(lookup, conn)
        logger.log(f"End of Pophelp Class")


