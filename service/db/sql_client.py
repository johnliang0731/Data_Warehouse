import pymysql
import os
import csv

class SqlClient:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if SqlClient.__instance != None:
            raise Exception("This class is a singleton! Please SqlClient.get_instance() instead of SqlClient() to get the singleton instance!")
        else:
            SqlClient.__instance = self


    '''
    Make sql client as a singleton class
    '''
    @staticmethod
    def get_instance():
        """ Static access method. """
        if SqlClient.__instance is None:
            SqlClient()
        return SqlClient.__instance


    """
    Initialize the database, create tables, insert sample data
    """
    def init_database(self, init_from_backup=True):
        try:
            if init_from_backup:
                self.change_database()
            else:
                self.create_database()
                self.create_tables()
                self.insert_data()
        except Exception as e:
            print("Initialize database failed.\n{}".format(e))


    """
    Read file content into a string
    :param file_name: name of the file
    :return: string
    """
    def get_sql_command_from_file(self, file_name):
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_path, file_name)
        sql = ""
        with open(file_path) as f:
            for line in f.readlines():
                sql += line.replace("\r", "").replace("\n", "")
        return sql

    def change_database(self):
        connection = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456')
        try:
            with connection.cursor() as cursor:
                cursor.execute("USE cs6400;")
        except Exception as e:
            print("execute sql command failed" + str(e))
        finally:
            connection.close()

    def create_database(self):
        connection = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456')
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP DATABASE IF EXISTS cs6400;")
                cursor.execute("CREATE DATABASE IF NOT EXISTS cs6400;")
                cursor.execute("USE cs6400;")
        except Exception as e:
            print("execute sql command failed" + str(e))
        finally:
            connection.close()

    def create_tables(self):
        connection = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', database="cs6400")
        try:
            with connection.cursor() as cursor:
                sql_commands = self.get_sql_command_from_file("schema.sql").split(";")
                for sql in sql_commands:
                    if len(sql.strip()) > 0:
                        cursor.execute(sql + ";")
        except Exception as e:
            print("execute sql command failed" + str(e))
        finally:
            connection.close()
    
    def insert_data(self): 
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_path, "sample_data") 
        table_names = ['Manufacturer', 'Product', 'Category', 'CategorizedBy', 'Date', 'Holiday', 'NonHoliday', 'City', 'Store', 'Membership', 'Sold', 'OnSale', 'YellowJacket', 'GiantHornet']
        for table in table_names:
            print("insert table {}".format(table))
            with open(os.path.join(file_path, table + ".csv"), mode='r') as csv_file: 
                csv_reader = csv.DictReader(csv_file)
                sql_command = self.build_insert_sql_command_from_csv_reader(table, csv_reader)
                self.exec_command(sql_command)

    def fetch_data_with_command(self, command):
        connection = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', database="cs6400")
        try:
            with connection.cursor() as cursor:
                cursor.execute(command)
                return cursor.fetchall()
        except Exception as e:
            print("execute sql command failed.\n{}".format(e))
        finally:
            connection.close()

    def exec_command(self, command):
        connection = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', database="cs6400")
        try:
            with connection.cursor() as cursor:
                cursor.execute(command)
            connection.commit()
        except Exception as e:
            print("execute sql command failed.\n{}".format(e))
        finally:
            connection.close()

        
    def close_db_connection(self):
        # self.connection.close()
        print("closed sql connection.")

    def build_insert_sql_command_from_csv_reader(self, table_name, csv_reader):
        sql_command = "INSERT INTO {}({}) VALUES ".format(table_name, ",".join(csv_reader.fieldnames))
        for row in csv_reader:
            values = []
            for value in row.values():
                # if value has characters, it is a string, so add "" around it.
                values.append(value if all(c.isdigit() for c in value) else "\"{}\"".format(value))
            sql_command += "({}),".format(",".join(values))
        return sql_command[:-1] + ";"


    def build_insert_sql_command_from_dict(self, table_name, dict):
        fields = []
        values = []
        for field_name, value in dict.items():
            fields.append(field_name)
            # if value has characters, it is a string, so add "" around it.
            values.append("\"{}\"".format(value) if any(c.isalpha() for c in value) else value)
        return "INSERT INTO {}({}) VALUES ({});".format(table_name, ",".join(fields), ",".join(values))

