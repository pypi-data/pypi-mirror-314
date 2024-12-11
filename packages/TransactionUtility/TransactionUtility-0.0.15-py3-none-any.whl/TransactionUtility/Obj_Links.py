import cx_Oracle
import loggerutility as logger

class Obj_Links:
    
    sql_models = []

    def check_or_update_obj_links(self, links, connection):
        
        required_keys = [
            'obj_name', 'form_no', 'field_name', 'link_form_name', 'link_arg', 'rights_char',
            'line_no'
        ]
        missing_keys = [key for key in required_keys if key not in links]
        logger.log(f"Missing required keys for obj_links table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for obj_links table: {', '.join(missing_keys)}")
        else:
            obj_name = links.get('obj_name', '')
            form_no = links.get('form_no', '')
            field_name = links.get('field_name', '')
            target_obj_name = links.get('target_object', '')
            link_form_name = links.get('link_form_name', '')
            link_title = links.get('link_title', '')
            link_uri = links.get('link_uri', '')
            link_type = links.get('link_type', '')
            link_arg = links.get('link_arg', '')
            update_flag = links.get('update_flag', '')
            link_name = links.get('link_name', '')
            rights_char = links.get('rights_char', '')
            image = links.get('image', '')
            show_in_panel = links.get('show_in_panel', '')
            shortcut_char = links.get('shortcut_char', '')
            auto_invoke = links.get('auto_invoke', '')
            swipe_position = links.get('swipe_position', '')
            title = links.get('title', '')
            descr = links.get('descr', '')
            show_confirm = links.get('show_confirm', '')
            display_mode = links.get('display_mode', '')
            line_no = links.get('line_no', '')
            link_id = links.get('link_id', '')
            rec_specific = links.get('record_specific', '')

            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM obj_links 
                WHERE OBJ_NAME = :obj_name 
                AND FORM_NO = :form_no 
                AND FIELD_NAME = :field_name 
                AND LINE_NO = :line_no
            """, obj_name=obj_name, form_no=form_no, 
                field_name=field_name, line_no=line_no)
            count = cursor.fetchone()[0]
            if count > 0:
                
                update_query = """
                    UPDATE obj_links SET
                    TARGET_OBJ_NAME = :target_obj_name, LINK_FORM_NAME = :link_form_name,
                    LINK_TITLE = :link_title, LINK_URI = :link_uri, LINK_TYPE = :link_type,
                    LINK_ARG = :link_arg, UPDATE_FLAG = :update_flag, LINK_NAME = :link_name,
                    RIGHTS_CHAR = :rights_char, IMAGE = :image, SHOW_IN_PANEL = :show_in_panel,
                    SHORTCUT_CHAR = :shortcut_char, AUTO_INVOKE = :auto_invoke,
                    SWIPE_POSITION = :swipe_position, TITLE = :title, DESCR = :descr,
                    SHOW_CONFIRM = :show_confirm, DISPLAY_MODE = :display_mode,
                    LINK_ID = :link_id, REC_SPECIFIC = :rec_specific
                    WHERE OBJ_NAME = :obj_name 
                    AND FORM_NO = :form_no 
                    AND FIELD_NAME = :field_name 
                    AND LINE_NO = :line_no
                """

                cursor.execute(update_query, {
                    'obj_name': obj_name,
                    'form_no': form_no,
                    'field_name': field_name,
                    'target_obj_name': target_obj_name,
                    'link_form_name': link_form_name,
                    'link_title': link_title,
                    'link_uri': link_uri,
                    'link_type': link_type,
                    'link_arg': link_arg,
                    'update_flag': update_flag,
                    'link_name': link_name,
                    'rights_char': rights_char,
                    'image': image,
                    'show_in_panel': show_in_panel,
                    'shortcut_char': shortcut_char,
                    'auto_invoke': auto_invoke,
                    'swipe_position': swipe_position,
                    'title': title,
                    'descr': descr,
                    'show_confirm': show_confirm,
                    'display_mode': display_mode,
                    'line_no': line_no,
                    'link_id': link_id,
                    'rec_specific': rec_specific
                })


            else:

                insert_query = """
                    INSERT INTO obj_links (
                    OBJ_NAME, FORM_NO, FIELD_NAME, TARGET_OBJ_NAME, LINK_FORM_NAME,
                    LINK_TITLE, LINK_URI, LINK_TYPE, LINK_ARG, UPDATE_FLAG, LINK_NAME,
                    RIGHTS_CHAR, IMAGE, SHOW_IN_PANEL, SHORTCUT_CHAR, AUTO_INVOKE,
                    SWIPE_POSITION, TITLE, DESCR, SHOW_CONFIRM, DISPLAY_MODE, LINE_NO,
                    LINK_ID, REC_SPECIFIC
                    ) VALUES (
                    :obj_name, :form_no, :field_name, :target_obj_name, :link_form_name,
                    :link_title, :link_uri, :link_type, :link_arg, :update_flag, :link_name,
                    :rights_char, :image, :show_in_panel, :shortcut_char, :auto_invoke,
                    :swipe_position, :title, :descr, :show_confirm, :display_mode, :line_no,
                    :link_id, :rec_specific
                )
                """

                cursor.execute(insert_query, {
                    'obj_name': obj_name,
                    'form_no': form_no,
                    'field_name': field_name,
                    'target_obj_name': target_obj_name,
                    'link_form_name': link_form_name,
                    'link_title': link_title,
                    'link_uri': link_uri,
                    'link_type': link_type,
                    'link_arg': link_arg,
                    'update_flag': update_flag,
                    'link_name': link_name,
                    'rights_char': rights_char,
                    'image': image,
                    'show_in_panel': show_in_panel,
                    'shortcut_char': shortcut_char,
                    'auto_invoke': auto_invoke,
                    'swipe_position': swipe_position,
                    'title': title,
                    'descr': descr,
                    'show_confirm': show_confirm,
                    'display_mode': display_mode,
                    'line_no': line_no,
                    'link_id': link_id,
                    'rec_specific': rec_specific
                })
            cursor.close()


    def process_data(self, conn, sql_models_data):
        logger.log(f"Start of Obj_Links Class")
        self.sql_models = sql_models_data
        for sql_model in self.sql_models:
            if "sql_model" in sql_model and "links" in sql_model['sql_model']:
                for links in sql_model['sql_model']['links']:
                    self.check_or_update_obj_links(links, conn)
        logger.log(f"End of Obj_Links Class")

