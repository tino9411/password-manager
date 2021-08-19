from config import config
import psycopg2
from PasswordGen import hash_password, set_password
from encryption import *
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
            hashpwd = hash_password(pwd)
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

    def update_master_email(self, pwd, email):
        try:

            email = input("Please type in your new email address:")
            pwd = input("Please enter your password to confirm: ")
            hashpwd = hash_password(pwd)
            query = '''UPDATE master_credentials SET master_email = %s WHERE master_password = %s'''
            data_to_insert = (email, hashpwd)
            self.cur.execute(query, data_to_insert)
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def is_empty(self):
        ''' This is used to check whether there is an existing user in master_credentials'''
        try:
            # create table 
            query = '''SELECT COUNT(*) FROM master_credentials'''
            self.cur.execute(query)
            entries = self.cur.fetchall()
            if entries[0][0] == 0:
                return True
            return False
            # close communication with the PostgreSQL database serve
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def get_master_email(self):
        try:

            self.conn.autocommit = True
            query = "SELECT master_email FROM master_credentials"
            self.cur.execute(query)
            self.conn.commit()
            result = self.cur.fetchone()
            self.cur.close()
            email = result[0]
        except(Exception, psycopg2.Error) as error:
            print(error)
        return email
    
    def get_master_password(self):
        try:

            self.conn.autocommit = True
            query = "SELECT master_password FROM master_credentials"
            self.cur.execute(query)
            self.conn.commit()
            result = self.cur.fetchone()
            self.cur.close()
            pwd = result[0]
        except(Exception, psycopg2.Error) as error:
            print(error)
        return pwd

    def check_login(self, email, pwd):
        match = False
        em = MPDatabase()
        password = MPDatabase()
        e = em.get_master_email()
        p = password.get_master_password()
        if email == e:
            if pwd == p:
                match = True
        else:
            match = False
        
        return match

    def find(self, app):
        try:

            self.conn.autocommit = True
            query = "SELECT * FROM credentials WHERE app = ""'" + app + "'"
            data_to_insert = app
            self.cur.execute(query, data_to_insert)
            self.conn.commit()
            rows = self.cur.fetchall()
            for row in rows:
                print("USERNAME:", row[0])
                print("EMAIL:", row[1])
                decrypt = EncryptDecrypt()
                pwd = decrypt.decrypt_password(row[2])
                print("PASSWORD:", pwd)
                print("WEBSITE:", row[3])
                print("APP:", row[4])
            self.cur.close()
        except(Exception, psycopg2.Error) as error:
            print(error)

    def add(self, username, email, pwd, website, app):
        try:
            encrypt = EncryptDecrypt()
            enpwd = encrypt.encrypt_password(pwd)
            # create table 
            query = 'INSERT INTO credentials (user_name, user_email, password, website, app) VALUES (%s,%s,%s,%s,%s)'
            data_to_insert = (username, email, enpwd, website, app)
            self.cur.execute(query, data_to_insert)
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
            print("Details have been added successfully!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def view_by_app(self, app):
        
        try:

            self.conn.autocommit = True
            query = "SELECT password FROM credentials WHERE app = ""'" + app + "'"
            data_to_insert = app
            self.cur.execute(query, data_to_insert)
            self.conn.commit()
            result = self.cur.fetchone()
            self.cur.close()
            enpwd = result[0]
            decrypt = EncryptDecrypt()
            pwd = decrypt.decrypt_password(enpwd)
        except(Exception, psycopg2.Error) as error:
            print(error)
        return pwd

    def view_by_user(self, username):
        try:

            self.conn.autocommit = True
            query = "SELECT password FROM credentials WHERE user_name = ""'" + username + "'"
            data_to_insert = username
            self.cur.execute(query, data_to_insert)
            self.conn.commit()
            result = self.cur.fetchone()
            self.cur.close()
            enpwd = result[0]
            decrypt = EncryptDecrypt()
            pwd = decrypt.decrypt_password(enpwd)
        except(Exception, psycopg2.Error) as error:
            print(error)
        return pwd
    
    def view_by_email(self, email):
        try:

            self.conn.autocommit = True
            query = "SELECT password FROM credentials WHERE user_email = ""'" + email + "'"
            data_to_insert = email
            self.cur.execute(query, data_to_insert)
            self.conn.commit()
            result = self.cur.fetchone()
            self.cur.close()
            enpwd = result[0]
            decrypt = EncryptDecrypt()
            pwd = decrypt.decrypt_password(enpwd)
        except(Exception, psycopg2.Error) as error:
            print(error)
        return pwd

    def create_user_table(self):
    
        """ create tables in the PostgreSQL database"""
        try:

        # create table 
            self.cur.execute('''CREATE TABLE credentials (
                user_name VARCHAR(255) NOT NULL,
                user_email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                website VARCHAR(255) NOT NULL,
                app VARCHAR(255) NOT NULL)''')
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
            print('Table successfully created.')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                    self.conn.close()

    def delete_user_table(self):
    
        """ Delete tables in the PostgreSQL database"""
        try:

        # create table 
            self.cur.execute(''' DROP TABLE credentials''')
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
            print('Table successfully deleted.')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                    self.conn.close()

'''view = MPDatabase()

t = view.find('reddit')
print(t)
'''
