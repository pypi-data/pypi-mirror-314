import loggerutility as logger

class Function_Defination:

    def execute_function(self, function_sql, connection):
        logger.log(f"Start of Function_Defination Class")
        for i, func in enumerate(function_sql, start=1):
            logger.log(f"Function {i}:\n{'-'*80}\n{func}\n{'-'*80}")

            cursor = connection.cursor()
            cursor.execute(func)
            logger.log(f"Function {i} executed successfully.")

            cursor.close()
        logger.log(f"End of Function_Defination Class")
            

