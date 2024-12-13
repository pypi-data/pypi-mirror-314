import cx_Oracle
from collections import defaultdict
import loggerutility as logger

class Dynamic_Table_Creation:
        
    def check_table_exists(self, table_name, connection):
        if not connection:
            return False
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) as CNT FROM USER_TABLES WHERE TABLE_NAME = :table_name", table_name=table_name)
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except cx_Oracle.Error as error:
            logger.log(f"Error checking APP_NAME existence: {error}")
            return False
        
    def check_column_exists(self, table_name, column_name, connection):
        if not connection:
            return False
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                    SELECT COUNT(*) as CNT FROM all_tab_columns 
                    WHERE table_name = :table_name AND column_name = :column_name
                """,
                table_name=table_name,
                column_name=column_name
            )
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except cx_Oracle.Error as error:
            logger.log(f"Error checking if column {column_name} exists in {table_name}: {error}")
            return False
        
    def drop_constraint(self, table_name, owner, connection):

        cursor = connection.cursor()
        try:
            query = """
                SELECT ac.constraint_name
                FROM all_constraints ac
                WHERE ac.table_name = :table_name
                AND ac.constraint_type = 'P'
                AND ac.owner = :owner
            """
            cursor.execute(query, table_name=table_name.upper(), owner=owner.upper())
            constraint = cursor.fetchone()

            if constraint:
                constraint_name = constraint[0]
                logger.log(f"Found constraint: {constraint_name} on table {table_name}")
 
                drop_query = f"ALTER TABLE {owner}.{table_name} DROP CONSTRAINT {constraint_name}"
                cursor.execute(drop_query)
                logger.log(f"Constraint {constraint_name} dropped successfully from table {table_name}.")
            
        except cx_Oracle.Error as error:
            logger.log(f"Error while dropping constraint from table {table_name}: {error}")
            return f"Error: {error}"

        finally:
            cursor.close()

    def get_primary_key_columns(self, table_name, owner, connection):
        primary_key_columns = []
        
        query = """
            SELECT acc.column_name
            FROM all_cons_columns acc
            JOIN all_constraints ac ON acc.constraint_name = ac.constraint_name
            WHERE ac.table_name = :table_name
            AND ac.constraint_type = 'P'
            AND ac.owner = :owner
        """
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, table_name=table_name.upper(), owner=owner.upper())
            rows = cursor.fetchall()
            for row in rows:
                primary_key_columns.append(row[0])
            logger.log(f"Primary key columns for table {table_name}: {primary_key_columns}")
            
        except cx_Oracle.Error as error:
            logger.log(f"Error fetching primary key columns for table {table_name}: {error}")
        
        finally:
            cursor.close()
        
        return primary_key_columns
    
    def add_primary_key_constraint(self, table_name, column_name_list, connection):

        pk_constraint = f"{table_name}_pk"
        pk_constraint_list = ",".join(column_name_list)
        query = f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {pk_constraint} PRIMARY KEY ({pk_constraint_list})
        """
        logger.log(f"Generated query to add primary key constraint: {query}")
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            logger.log(f"Primary key constraint {pk_constraint} added successfully to table {table_name}.")
        except cx_Oracle.Error as error:
            logger.log(f"Error adding primary key constraint to table {table_name}: {error}")
        finally:
            cursor.close()

    def create_new_table(self, table_lst, connection):
        for table_name, columns in table_lst.items():
            columns_sql = []
            primary_key_columns = [] 

            table_name = table_name
            for single_col in columns:

                col_name = single_col['db_name']
                col_type = single_col['col_type'].upper()
                db_size = single_col.get('db_size', None)
                is_key = single_col.get('key', False)
                mandatory = single_col.get('mandatory', 'false')

                col_def = ''
                if (col_type == 'CHAR' or col_type == 'VARCHAR') and db_size:
                    if db_size == '0':
                        col_def = f"{col_name} {col_type}(10)"  
                    else:
                        col_def = f"{col_name} {col_type}({db_size})"
                
                elif col_type == 'DECIMAL':
                    if db_size != '0':
                        col_def = f"{col_name} DECIMAL({db_size}, 2)"  
                    else:
                        col_def = f"{col_name} DECIMAL(5, 2)"  
                
                elif col_type == 'DATETIME':
                    col_def = f"{col_name} DATE" 

                else:
                    col_def = f"{col_name} {col_type}"  

                if is_key == True:
                    primary_key_columns.append(col_name)
                    
                if col_def != '':
                    columns_sql.append(col_def)

            columns_sql_str = ", ".join(columns_sql)
            
            create_table_sql = f"CREATE TABLE {table_name} ({columns_sql_str})"
            logger.log(f"create_table_sql ::: {create_table_sql}")

            cursor = connection.cursor()
            try:
                cursor.execute(create_table_sql)
                logger.log(f"Table {table_name} created successfully.")

                pk_constraint=f"{table_name}_pk"
                pk_constraint_list = ",".join(primary_key_columns)
                queryy = f"""ALTER TABLE {table_name}
                        ADD CONSTRAINT {pk_constraint} PRIMARY KEY ({pk_constraint_list})"""
                logger.log(f"queryy:: {queryy}")
                cursor.execute(queryy)

            except cx_Oracle.Error as error:
                logger.log(f"Error creating table {table_name}: {error}")

    def alter_table_add_columns(self, table_name, single_col, connection):

        col_name = single_col['db_name']
        col_type = single_col['col_type'].upper()
        db_size = single_col.get('db_size', 10)
        is_key = single_col.get('key', False)
        mandatory = single_col.get('mandatory', 'false')

        col_def = ''
        if (col_type == 'CHAR' or col_type == 'VARCHAR') and db_size:
            if db_size == '0':
                col_def = f"{col_name} {col_type}(10)"  
            else:
                col_def = f"{col_name} {col_type}({db_size})"
        
        elif col_type == 'DECIMAL':
            if db_size != '0':
                col_def = f"{col_name} DECIMAL({db_size}, 2)"  
            else:
                col_def = f"{col_name} DECIMAL(5, 2)"  
        
        elif col_type == 'DATETIME':
            col_def = f"{col_name} DATE" 

        else:
            col_def = f"{col_name} {col_type}"  

        # if is_key == True:
        #     col_def += " PRIMARY KEY"

        alter_table_sql = f"ALTER TABLE {table_name} ADD ({col_def})"
        logger.log(f"{alter_table_sql}")

        cursor = connection.cursor()
        try:
            cursor.execute(alter_table_sql)
            logger.log(f"Column {col_name} added successfully to table {table_name}.")
        except cx_Oracle.Error as error:
            logger.log(f"Error adding column {col_name} to table {table_name}: {error}")
            return False
        
    def get_column_from_main_table(self, columns_lst, main_table, table_name, column_name, main_table_col):
        for column in columns_lst:
            column = column['column']
            if column['table_name'].upper() == main_table.upper() and column['db_name'].upper() == main_table_col.upper():
                column['table_name'] = table_name.upper()
                column['db_name'] = column_name.upper()
                return column

    def create_alter_table(self, data, connection):
        logger.log(f"Start of Dynamic_Table_Creation Class")
        if "transaction" in data and "sql_models" in data['transaction']:
            for index,sql_models in enumerate(data["transaction"]["sql_models"]):
                columns = sql_models["sql_model"]["columns"]
                table_json = defaultdict(list)
                for column in columns:
                    column = column['column']
                    table_name = column['table_name']
                    column_name = column['db_name']
                    exists = self.check_table_exists(table_name.upper(), connection)
                    logger.log(f"table_name ::: {table_name}")
                    logger.log(f"exists ::: {exists}")
                    if exists:
                        logger.log(f"column_name ::: {column_name}")
                        column_exist = self.check_column_exists(table_name.upper(), column_name.upper(), connection)
                        logger.log(f"column_exist ::: {column_exist}")
                        if not column_exist:
                            logger.log(f"Inside column_exist ::: {table_name.upper(), column}")
                            self.alter_table_add_columns(table_name.upper(), column, connection)
                            
                            if column['key'] == True:
                                check_prmary_key_columns = self.get_primary_key_columns(table_name, "APPVISDEV", connection)
                                logger.log(f"check:: {check_prmary_key_columns}")
                                self.drop_constraint(table_name, "APPVISDEV", connection)
                                check_prmary_key_columns.append(column_name)
                                logger.log(f"check_prmary_key_columns ::: {check_prmary_key_columns}")
                                self.add_primary_key_constraint(table_name,check_prmary_key_columns,connection)
                    else:
                        table_json[table_name.upper()].append(column)
                logger.log(f"outside forloop ::: {dict(table_json)}")
                self.create_new_table(dict(table_json), connection)
                
                if "joins" in sql_models["sql_model"] and "join_predicates" in sql_models["sql_model"]['joins'] and "joins" in sql_models["sql_model"]['joins']['join_predicates']:
                    join_Data_list = sql_models["sql_model"]['joins']['join_predicates']['joins']
                    for single_join in join_Data_list:
                        if single_join['main_table'] == False:
                            main_table = single_join['join_table'].lower()
                            main_table_col = single_join['join_column'].lower()
                            table_name_toadd = single_join['table'].lower()
                            column_name_toadd  = single_join['column'].lower()
                            logger.log(f"column_name ::: {column_name_toadd}")
                            column_exist = self.check_column_exists(table_name_toadd.upper(), column_name_toadd.upper(), connection)
                            logger.log(f"column_exist ::: {column_exist}")
                            if not column_exist:
                                column = self.get_column_from_main_table(columns, main_table, table_name_toadd, column_name_toadd, main_table_col)
                                logger.log(f"Inside column_exist join ::: {column}")
                                self.alter_table_add_columns(table_name_toadd.upper(), column, connection)
                                
                                if column['key'] == True:
                                    check_prmary_key_columns = self.get_primary_key_columns(table_name_toadd, "APPVISDEV", connection)
                                    logger.log(f"check:: {check_prmary_key_columns}")
                                    self.drop_constraint(table_name_toadd, "APPVISDEV", connection)
                                    check_prmary_key_columns.append(column_name_toadd)
                                    logger.log(f"check_prmary_key_columns ::: {check_prmary_key_columns}")
                                    self.add_primary_key_constraint(table_name_toadd,check_prmary_key_columns,connection)


            
            logger.log(f"End of Dynamic_Table_Creation Class")
            return f"Success"

