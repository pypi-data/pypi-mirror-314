import cx_Oracle
from datetime import datetime
import loggerutility as logger

class Obj_Actions:

    sql_models = []
    
    def insert_or_update_actions(self, actions, connection):

        required_keys = [
            'obj_name', 'line_no', 'title'
        ]

        missing_keys = [key for key in required_keys if key not in actions]
        logger.log(f"Missing required keys for obj_actions table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for obj_actions table: {', '.join(missing_keys)}")
        else:
            obj_name = actions.get('obj_name', '')
            line_no = actions.get('line_no', '')
            image = actions.get('image', '')
            description = actions.get('description', '')
            service_code = actions.get('service_code', '')
            interactive = actions.get('interactive', '')
            rights_char = actions.get('rights_char', '')
            title = actions.get('title', '')
            form_no = actions.get('form_no', '')
            service_handler = actions.get('service_handler', '')
            placement = actions.get('placement', '')
            action_type = actions.get('action_type', '')
            tran_type = actions.get('tran_type', '')
            chg_date = datetime.now().strftime('%d-%m-%y')
            chg_term = actions.get('chg_term', '').strip() or 'System'
            chg_user = actions.get('chg_user', '').strip() or 'System'
            is_confirmation_req = actions.get('confirmation_req', '')
            sep_duty_opt = actions.get('sep_duty_opt', '')
            re_auth_opt = actions.get('re_auth_opt', '')
            show_in_panel = actions.get('show_in_panel', '')
            page_context = actions.get('page_context', '')
            type_ = actions.get('type', '')  
            action_arg = actions.get('action_arg', '')
            swipe_position = actions.get('swipe_position', '')
            multi_row_opt = actions.get('multi_row_opt', '')
            action_id = actions.get('id', '')
            def_nodata = actions.get('def_no_data', '')
            in_proc_intrupt = actions.get('in_proc_intrupt', '')
            estimated_time = actions.get('estimated_time', '')
            action_group = actions.get('action_group', '')
            display_opt = actions.get('display_opt', '')
            display_mode = actions.get('display_mode', '')
            show_confirm = actions.get('show_confirm', '')
            rec_specific = actions.get('rec_specific', '')

            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM obj_actions WHERE OBJ_NAME = :obj_name AND LINE_NO = :line_no", obj_name=obj_name, line_no=line_no)
            count = cursor.fetchone()[0]
            if count > 0:

                values = {
                    "obj_name": obj_name, "line_no": line_no, "image": image, "description": description, "service_code": str(service_code),
                    "interactive": interactive, "rights_char": rights_char, "title": title, "form_no": form_no, "service_handler": service_handler,
                    "placement": placement, "action_type": action_type, "tran_type": tran_type, "chg_date": chg_date, "chg_term": chg_term,
                    "chg_user": chg_user, "is_confirmation_req": is_confirmation_req, "sep_duty_opt": sep_duty_opt, "re_auth_opt": re_auth_opt,
                    "show_in_panel": show_in_panel, "page_context": page_context, "type": type_, "action_arg": action_arg, "swipe_position": swipe_position,
                    "multi_row_opt": multi_row_opt, "action_id": action_id, "def_nodata": def_nodata, "in_proc_intrupt": in_proc_intrupt, 
                    "estimated_time": estimated_time, "action_group": action_group, "display_opt": display_opt, "display_mode": display_mode,
                    "show_confirm": show_confirm, "rec_specific": rec_specific
                }

                update_query = """
                    UPDATE obj_actions SET
                    IMAGE = :image, DESCRIPTION = :description, SERVICE_CODE = :service_code,
                    INTERACTIVE = :interactive, RIGHTS_CHAR = :rights_char, TITLE = :title,
                    FORM_NO = :form_no, SERVICE_HANDLER = :service_handler, PLACEMENT = :placement,
                    ACTION_TYPE = :action_type, TRAN_TYPE = :tran_type, 
                    CHG_DATE = TO_DATE(:chg_date, 'DD-MM-YYYY'), CHG_TERM = :chg_term, CHG_USER = :chg_user,
                    IS_CONFIRMATION_REQ = :is_confirmation_req, SEP_DUTY_OPT = :sep_duty_opt,
                    RE_AUTH_OPT = :re_auth_opt, SHOW_IN_PANEL = :show_in_panel,
                    PAGE_CONTEXT = :page_context, TYPE = :type, ACTION_ARG = :action_arg,
                    SWIPE_POSITION = :swipe_position, MULTI_ROW_OPT = :multi_row_opt,
                    ACTION_ID = :action_id, DEF_NODATA = :def_nodata, 
                    IN_PROC_INTRUPT = :in_proc_intrupt, ESTIMATED_TIME = :estimated_time,
                    ACTION_GROUP = :action_group, DISPLAY_OPT = :display_opt,
                    DISPLAY_MODE = :display_mode, SHOW_CONFIRM = :show_confirm,
                    REC_SPECIFIC = :rec_specific
                    WHERE OBJ_NAME = :obj_name AND LINE_NO = :line_no
                """
                cursor.execute(update_query, values)
                logger.log(f"Updated: {obj_name} - {line_no}")
            else:
                values = {
                    "obj_name": obj_name, "line_no": line_no, "image": image, "description": description, "service_code": str(service_code),
                    "interactive": interactive, "rights_char": rights_char, "title": title, "form_no": form_no, "service_handler": service_handler,
                    "placement": placement, "action_type": action_type, "tran_type": tran_type, "chg_date": chg_date, "chg_term": chg_term,
                    "chg_user": chg_user, "is_confirmation_req": is_confirmation_req, "sep_duty_opt": sep_duty_opt, "re_auth_opt": re_auth_opt,
                    "show_in_panel": show_in_panel, "page_context": page_context, "type": type_, "action_arg": action_arg, "swipe_position": swipe_position,
                    "multi_row_opt": multi_row_opt, "action_id": action_id, "def_nodata": def_nodata, "in_proc_intrupt": in_proc_intrupt, 
                    "estimated_time": estimated_time, "action_group": action_group, "display_opt": display_opt, "display_mode": display_mode,
                    "show_confirm": show_confirm, "rec_specific": rec_specific
                }

                insert_query = """
                    INSERT INTO obj_actions (
                    OBJ_NAME, LINE_NO, IMAGE, DESCRIPTION, SERVICE_CODE, INTERACTIVE,
                    RIGHTS_CHAR, TITLE, FORM_NO, SERVICE_HANDLER, PLACEMENT, ACTION_TYPE,
                    TRAN_TYPE, CHG_DATE, CHG_TERM, CHG_USER, IS_CONFIRMATION_REQ,
                    SEP_DUTY_OPT, RE_AUTH_OPT, SHOW_IN_PANEL, PAGE_CONTEXT, TYPE,
                    ACTION_ARG, SWIPE_POSITION, MULTI_ROW_OPT, ACTION_ID, DEF_NODATA,
                    IN_PROC_INTRUPT, ESTIMATED_TIME, ACTION_GROUP, DISPLAY_OPT,
                    DISPLAY_MODE, SHOW_CONFIRM, REC_SPECIFIC
                    ) VALUES (
                    :obj_name, :line_no, :image, :description, :service_code, :interactive,
                    :rights_char, :title, :form_no, :service_handler, :placement, :action_type,
                    :tran_type, TO_DATE(:chg_date, 'DD-MM-YYYY'), :chg_term, :chg_user, :is_confirmation_req,
                    :sep_duty_opt, :re_auth_opt, :show_in_panel, :page_context, :type,
                    :action_arg, :swipe_position, :multi_row_opt, :action_id, :def_nodata,
                    :in_proc_intrupt, :estimated_time, :action_group, :display_opt,
                    :display_mode, :show_confirm, :rec_specific)
                """
                cursor.execute(insert_query, values)
                logger.log(f"Inserted: {obj_name} - {line_no}")
            cursor.close()


    def process_data(self, conn, sql_models_data):
        logger.log(f"Start of Obj_Actions Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            if "sql_model" in sql_model and "action" in sql_model['sql_model']:
                for actions in sql_model['sql_model']['action']:
                    if actions:
                        self.insert_or_update_actions(actions, conn)
        logger.log(f"End of Obj_Actions Class")
