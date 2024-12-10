# same file as gailbotplugins , use it solely for the purpose of retrieving
# the complete url (including creator id) to a plugin in the bucket

import mysql.connector
from mysql.connector import Error



class RDSClient:
    def __init__(self):
        self.host = "plugin-db.c3aqee64crhq.us-east-1.rds.amazonaws.com"
        self.user = "admin"
        self.password = 'hilab12#'
        self.database = "gailbot"
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )


        except Error as e:
            print(f"Error connecting to RDS: {e}")
            self.connection = None
    
    def fetch_plugin_info(self, plugin_id):
        plugin_info = dict()
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT user_id FROM Plugins WHERE id = %s"
            cursor.execute(query, (plugin_id,))
            result = cursor.fetchone()
            
            print("Database row:", result)

            if result:
                plugin_info["user_id"] = result["user_id"]
            else:
                print(f"No user id found for plugin ID {plugin_id}")
                return None

            query = "SELECT name FROM Plugins WHERE id = %s"
            cursor.execute(query, (plugin_id,))
            result = cursor.fetchone()

            if result:
                plugin_info["name"] = result["name"]
            else:
                print(f"No name found for plugin ID {plugin_id}")
                return None

            query = "SELECT version FROM Plugins WHERE id = %s"
            cursor.execute(query, (plugin_id,))
            result = cursor.fetchone()

            if result:
                plugin_info["version"] = result["version"]
            else:
                print(f"No version found for plugin ID {plugin_id}")
                return None
            
            query = "SELECT s3_url FROM Plugins WHERE id = %s"
            cursor.execute(query, (plugin_id,))
            result = cursor.fetchone()
            
            if result:
                plugin_info["s3_url"] = result["s3_url"]
            else:
                print(f"No s3_url found for plugin ID {plugin_id}")
                return None

            
        except Error as e:
            print(f"Error fetching info for plugin in RDS Connect: {e}")
            return None
        finally:
            cursor.close()
        return plugin_info

    

        # CODE TO CHECK COLUMNS
        # if self.connection is None:
        #     print("No database connection.")
        #     return None

        # try:
        #     cursor = self.connection.cursor()
        #     query = "SHOW COLUMNS FROM Plugins"
        #     cursor.execute(query)
        #     columns = cursor.fetchall()

        #     column_names = [column[0] for column in columns]  # Extract column names
        #     print("column: ", column_names)
        #     return column_names
        # except Error as e:
        #     print(f"Error fetching column names: {e}")
        #     return None
        # finally:
        #     cursor.close()


    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            # print("RDS connection closed")
