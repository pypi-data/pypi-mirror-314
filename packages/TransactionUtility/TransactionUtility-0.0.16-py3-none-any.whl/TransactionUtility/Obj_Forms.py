import cx_Oracle
import loggerutility as logger

class Obj_Forms:

    sql_models = []

    def insert_or_update_form(self, sql_model, connection, object_name):
        cursor = connection.cursor()

        required_keys = ['form_no']

        missing_keys = [key for key in required_keys if key not in sql_model]
        logger.log(f"Missing required keys for obj_forms table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for obj_forms table: {', '.join(missing_keys)}")
        else:
            win_name = f"w_{object_name}"
            title = sql_model.get('form_title', '')
            obj_brow_name = sql_model.get('obj_brow_name', '')
            obj_edit_name = sql_model.get('obj_edit_name', '')
            cross_update_expr = sql_model.get('cross_update_expr', '')
            expr_fld_info = sql_model.get('expr_fld_info', '')
            target_fld_info = sql_model.get('target_fld_info', '')
            expr_comment = sql_model.get('expr_comment', '')
            form_no = sql_model.get('form_no', '')
            scr_flag = 'F' if (form_no == '1' or form_no == 1) else 'T'
            auto_accept_scan = sql_model.get('auto_accept_scan', '')
            scan_flag = sql_model.get('scan_flag', '')
            scan_metadata = sql_model.get('scan_metadata', '')
            property_info = sql_model.get('property_info', '')
            scan_delimiter = sql_model.get('scan_delimiter', '')
            column_on_save = sql_model.get('column_on_save', '')
            after_save = sql_model.get('after_save', '')
            ext_setup = sql_model.get('ext_setup', '')
            ext_metadata = sql_model.get('ext_metadata', '')
            ext_com = sql_model.get('ext_com', '')
            auto_accept_weighdata = sql_model.get('auto_accept_weighdata', '')
            form_type = sql_model.get('form_type', '')
            disp_metadata = sql_model.get('disp_meta_data', '')
            parent_key_col = sql_model.get('parent_key_col', '')
            qty_col = sql_model.get('qty_col', '')
            rate_col = sql_model.get('rate_col', '')
            assisted_mode = sql_model.get('assisted_mode', '')
            storage_key_metadata = sql_model.get('storage_key_metadata', '')
            selection_mode = sql_model.get('selection_mode', '')
            default_view = sql_model.get('default_view', '')
            auto_addon_entry = sql_model.get('auto_addon_entry', '')
            duplicate_add = sql_model.get('duplicate_add', '')
            default_row_cnt = sql_model.get('default_row_cnt', '')
            freeze_col_pos = sql_model.get('freeze_col_pos', '')
            is_mandatory = sql_model.get('is_mandatory', '')
            tran_id_col = sql_model.get('tran_id_col', '')
            selection_opt = sql_model.get('selection_opt', '')
            key_info = sql_model.get('key_info', '')
            thumb_obj = sql_model.get('thumb_obj', '')
            thumb_image_col = sql_model.get('thumb_image_col', '')
            thumb_alt_col = sql_model.get('thumb_alt_col', '')
            # form_name = sql_model.get('form_title', '')
            form_name = ''
            form_icon = sql_model.get('form_icon', '')
            form_view_opts = sql_model.get('form_view_opts', '')
            x_column = sql_model.get('x_column', '')
            y_column = sql_model.get('y_column', '')
            action_arg = sql_model.get('action_arg', '')

            cursor.execute("""
                    SELECT COUNT(*) FROM obj_forms 
                    WHERE WIN_NAME = :win_name 
                    AND FORM_NO = :form_no
                """, win_name=win_name, form_no=form_no)
            count = cursor.fetchone()[0]
            logger.log(f"Obj_forms count ::: {count}")
            if count > 0:
                update_query = """
                    UPDATE obj_forms SET
                    TITLE = :title, OBJ_BROW_NAME = :obj_brow_name, OBJ_EDIT_NAME = :obj_edit_name, CROSS_UPDATE_EXPR = :cross_update_expr, EXPR_FLD_INFO = :expr_fld_info,
                    TARGET_FLD_INFO = :target_fld_info, EXPR_COMMENT = :expr_comment, SCR_FLAG = :scr_flag, AUTO_ACCEPT_SCAN = :auto_accept_scan, SCAN_FLAG = :scan_flag,
                    SCAN_METADATA = :scan_metadata, PROPERTY_INFO = :property_info, SCAN_DELIMITER = :scan_delimiter, COLUMN_ON_SAVE = :column_on_save, AFTER_SAVE = :after_save,
                    EXT_SETUP = :ext_setup, EXT_METADATA = :ext_metadata, EXT_COM = :ext_com, AUTO_ACCEPT_WEIGHDATA = :auto_accept_weighdata, FORM_TYPE = :form_type,
                    DISP_METADATA = :disp_metadata, PARENT_KEY_COL = :parent_key_col, QTY_COL = :qty_col, RATE_COL = :rate_col, ASSISTED_MODE = :assisted_mode,
                    STORAGE_KEY_METADATA = :storage_key_metadata, SELECTION_MODE = :selection_mode, DEFAULT_VIEW = :default_view, AUTO_ADDON_ENTRY = :auto_addon_entry, DUPLICATE_ADD = :duplicate_add,
                    DEFAULT_ROW_CNT = :default_row_cnt, FREEZE_COL_POS = :freeze_col_pos, IS_MANDATORY = :is_mandatory, TRAN_ID_COL = :tran_id_col, SELECTION_OPT = :selection_opt,
                    KEY_INFO = :key_info, THUMB_OBJ = :thumb_obj, THUMB_IMAGE_COL = :thumb_image_col, THUMB_ALT_COL = :thumb_alt_col, FORM_NAME = :form_name, FORM_ICON = :form_icon,
                    FORM_VIEW_OPTS = :form_view_opts, X_COLUMN = :x_column, Y_COLUMN = :y_column, ACTION_ARG = :action_arg
                    WHERE WIN_NAME = :win_name AND FORM_NO = :form_no
                """
                
                cursor.execute(update_query, {
                    'win_name': win_name, 'title': title, 'obj_brow_name': obj_brow_name, 'obj_edit_name': obj_edit_name, 'cross_update_expr': cross_update_expr, 'expr_fld_info': expr_fld_info,
                    'target_fld_info': target_fld_info, 'expr_comment': expr_comment, 'form_no': form_no, 'scr_flag': scr_flag, 'auto_accept_scan': auto_accept_scan, 'scan_flag': scan_flag, 'scan_metadata': scan_metadata,
                    'property_info': property_info, 'scan_delimiter': scan_delimiter, 'column_on_save': column_on_save, 'after_save': after_save, 'ext_setup': ext_setup, 'ext_metadata': ext_metadata, 'ext_com': ext_com,
                    'auto_accept_weighdata': auto_accept_weighdata, 'form_type': form_type, 'disp_metadata': disp_metadata, 'parent_key_col': parent_key_col, 'qty_col': qty_col, 'rate_col': rate_col, 'assisted_mode': assisted_mode,
                    'storage_key_metadata': storage_key_metadata, 'selection_mode': selection_mode, 'default_view': default_view, 'auto_addon_entry': auto_addon_entry, 'duplicate_add': duplicate_add, 'default_row_cnt': default_row_cnt,
                    'freeze_col_pos': freeze_col_pos, 'is_mandatory': is_mandatory, 'tran_id_col': tran_id_col, 'selection_opt': selection_opt, 'key_info': key_info, 'thumb_obj': thumb_obj, 'thumb_image_col': thumb_image_col,
                    'thumb_alt_col': thumb_alt_col, 'form_name': form_name, 'form_icon': form_icon, 'form_view_opts': form_view_opts, 'x_column': x_column, 'y_column': y_column, 'action_arg': action_arg
                })
                
                logger.log(f"Obj_forms update_query ::: {update_query}")
                logger.log(f"Updated: {win_name} - {form_no}")

            else:
                insert_query = """
                    INSERT INTO obj_forms (
                        WIN_NAME, TITLE, OBJ_BROW_NAME, OBJ_EDIT_NAME, CROSS_UPDATE_EXPR, EXPR_FLD_INFO, 
                        TARGET_FLD_INFO, EXPR_COMMENT, FORM_NO, SCR_FLAG, AUTO_ACCEPT_SCAN, SCAN_FLAG, SCAN_METADATA,
                        PROPERTY_INFO, SCAN_DELIMITER, COLUMN_ON_SAVE, AFTER_SAVE, EXT_SETUP, EXT_METADATA, EXT_COM, 
                        AUTO_ACCEPT_WEIGHDATA, FORM_TYPE, DISP_METADATA, PARENT_KEY_COL, QTY_COL, RATE_COL, ASSISTED_MODE, 
                        STORAGE_KEY_METADATA, SELECTION_MODE, DEFAULT_VIEW, AUTO_ADDON_ENTRY, DUPLICATE_ADD, DEFAULT_ROW_CNT, 
                        FREEZE_COL_POS, IS_MANDATORY, TRAN_ID_COL, SELECTION_OPT, KEY_INFO, THUMB_OBJ, THUMB_IMAGE_COL, 
                        THUMB_ALT_COL, FORM_NAME, FORM_ICON, FORM_VIEW_OPTS, X_COLUMN, Y_COLUMN, ACTION_ARG
                    ) VALUES (
                        :win_name, :title, :obj_brow_name, :obj_edit_name, :cross_update_expr, :expr_fld_info, 
                        :target_fld_info, :expr_comment, :form_no, :scr_flag, :auto_accept_scan, :scan_flag, :scan_metadata, 
                        :property_info, :scan_delimiter, :column_on_save, :after_save, :ext_setup, :ext_metadata, :ext_com, 
                        :auto_accept_weighdata, :form_type, :disp_metadata, :parent_key_col, :qty_col, :rate_col, :assisted_mode, 
                        :storage_key_metadata, :selection_mode, :default_view, :auto_addon_entry, :duplicate_add, :default_row_cnt, 
                        :freeze_col_pos, :is_mandatory, :tran_id_col, :selection_opt, :key_info, :thumb_obj, :thumb_image_col, 
                        :thumb_alt_col, :form_name, :form_icon, :form_view_opts, :x_column, :y_column, :action_arg
                    )
                """
                
                cursor.execute(insert_query, {
                    'win_name': win_name, 'title': title, 'obj_brow_name': obj_brow_name, 'obj_edit_name': obj_edit_name, 'cross_update_expr': cross_update_expr, 'expr_fld_info': expr_fld_info,
                    'target_fld_info': target_fld_info, 'expr_comment': expr_comment, 'form_no': form_no, 'scr_flag': scr_flag, 'auto_accept_scan': auto_accept_scan, 'scan_flag': scan_flag, 'scan_metadata': scan_metadata,
                    'property_info': property_info, 'scan_delimiter': scan_delimiter, 'column_on_save': column_on_save, 'after_save': after_save, 'ext_setup': ext_setup, 'ext_metadata': ext_metadata, 'ext_com': ext_com,
                    'auto_accept_weighdata': auto_accept_weighdata, 'form_type': form_type, 'disp_metadata': disp_metadata, 'parent_key_col': parent_key_col, 'qty_col': qty_col, 'rate_col': rate_col, 'assisted_mode': assisted_mode,
                    'storage_key_metadata': storage_key_metadata, 'selection_mode': selection_mode, 'default_view': default_view, 'auto_addon_entry': auto_addon_entry, 'duplicate_add': duplicate_add, 'default_row_cnt': default_row_cnt,
                    'freeze_col_pos': freeze_col_pos, 'is_mandatory': is_mandatory, 'tran_id_col': tran_id_col, 'selection_opt': selection_opt, 'key_info': key_info, 'thumb_obj': thumb_obj, 'thumb_image_col': thumb_image_col,
                    'thumb_alt_col': thumb_alt_col, 'form_name': form_name, 'form_icon': form_icon, 'form_view_opts': form_view_opts, 'x_column': x_column, 'y_column': y_column, 'action_arg': action_arg
                })
                
                logger.log(f"Obj_forms insert_query ::: {insert_query}")
                logger.log(f"Inserted: {win_name} - {form_no}")
        cursor.close()

    def process_data(self, conn, sql_models_data, object_name):
        logger.log(f"Start of Obj_Forms Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            self.insert_or_update_form(sql_model['sql_model'], conn, object_name)
        logger.log(f"End of Obj_Forms Class")

