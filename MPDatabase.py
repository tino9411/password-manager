from config import config
import psycopg2
from PasswordGen import hash_password, set_password
class MPDatabase:
    def __init__(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()
            self.params = params
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**self.params)
            self.conn = conn
            # create a cursor
            cur = self.conn.cursor()
            self.cur = cur
        except (Exception, psycopg2.DatabaseError) as error:
             print(error)

    def create_master_table(self):
        """ Create master table in the PostgreSQL database. This table will store the hashed"""
        self.conn = None
        try:
          
            self.cur.execute('''CREATE TABLE IF NOT EXISTS master_credentials (
                master_password VARCHAR(255) NOT NULL,
                master_email VARCHAR(255) NOT NULL)''')
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def add_master_details(self, pwd, email):
        try:
            hashpwd = set_password(pwd)
            # create table 
            query = 'INSERT INTO master_credentials (master_password, master_email) VALUES (%s,%s)'
            data_to_insert = (hashpwd, email)
            self.cur.execute(query, data_to_insert)
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def delete_master_details(self, email):
        conn = None
        try: 
            answer = input("ARE YOU SURE YOU WANT TO DELETE THIS DATA? YOU WILL HAVE TO MAKE A NEW ACCOUNT! (Yy/Nn): ").lower()
            if answer == "y":
                query = '''DELETE FROM master_credentials 
                       WHERE master_email = %s;'''
                data_to_insert = (email,)
                self.cur.execute(query, data_to_insert)
                # close communication with the PostgreSQL database server
                self.cur.close()
                # commit the changes
                self.conn.commit()
                print("Account", email, "has been removed!")
            elif answer == "n":
                
                print("No Changes Have Been Made!")
            else:
                print("Please type Y or N")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def update_master_password(self):
        conn = None
        try:
            email = input("Please type in your email address: ")
            pwd = input("Please type in a new password: ")
            hashpwd = set_password(pwd)

            # create table 
            query = '''UPDATE master_credentials SET master_password = %s WHERE master_email = %s'''
            data_to_insert = (hashpwd, email)
            self.cur.execute(query, data_to_insert)
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def update_master_email(pwd, email):
        conn = None
        try:

            email = input("Please type in your new email address:")
            pwd = input("Please enter your password to confirm: ")
            hashpwd = hash_password(pwd)
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table 
            query = '''UPDATE master_credentials SET master_email = %s WHERE master_password = %s'''
            data_to_insert = (email, hashpwd)
            cur.execute(query, data_to_insert)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def is_empty():
        ''' This is used to check whether there is an existing user in master_credentials'''
        conn = None
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table 
            query = '''SELECT COUNT(*) FROM master_credentials'''
            cur.execute(query)
            entries = cur.fetchall()
            if entries[0][0] == 0:
                return True
            return False
            # close communication with the PostgreSQL database server
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def login_check():
        pass

    def get_email():
        pass
