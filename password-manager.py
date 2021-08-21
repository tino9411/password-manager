from getpass import getpass
from database import MPDatabase

def setup():
    t = MPDatabase()
    t.create_master_table()
    print("Enter your email: ")
    email = input()
    password = input("Enter a password to hash: ")
def login():

    while True:
        print("Email: ")
        email = input()
        password = getpass()
        check = MPDatabase()
        correct = check.check_login(email, password)
        if correct:
            menu()
        else:
            print("Incorrect login details!")

def title():
    print('''

    ----------------------------------
        WELCOME TO PASSWORD MANAGER
    ----------------------------------        
     ''')

def add_password():

    pwd_not_added = True

    while pwd_not_added:
        website = input('''Website: ''')
        app = input("App: ")
        username = input("Username: ")
        email = input("Email: ")
        password = getpass("Password: ")
        confirm = getpass("Please confirm the password: ")
        if confirm == password:
            add = MPDatabase()
            add.add(username, email, password, website, app)
            print("Password has been added to the database.")
            choice = input("Would you like to add another? [Y/y N/n]. Press q to return to the main menu: ").lower()
            if choice == 'y':
                pwd_not_added = True
            elif choice == 'n':
                pwd_not_added = False
            elif choice == 'q':
                menu()
            elif choice == '':
                print("Please choose Y/y or N/n. Press q to return to the main menu: ")
            else:
                print("Please choose Y/y or N/n. Press q to return to the main menu: ")

        else:
            print("Password does not match!! Please try again")

def view_password():
    to_view = True

    while to_view:
        print('''
    ---------------------------------- 
              View Password
    ----------------------------------
    Press Q to return to the main menu
    ---------------------------------- \n''')
        app = input("Please enter the name of the app: ").lower()
        password = getpass("Password: ")
        get = MPDatabase()
        confirm =  get.get_master_password()
        if confirm == password:
            view = MPDatabase()
            v = view.view_by_app(app)
            print(v)
            
            choice = input("Would you like to view another? [Y/y N/n]. Press q to return to the main menu: ").lower()
            if choice == 'y':
                to_view = True
            elif choice == 'n':
                menu()
            elif choice == 'q':
                menu()
            elif choice == '':
                print("Please choose Y/y or N/n. Press q to return to the main menu: ")
            else:
                print("Please choose Y/y or N/n. Press q to return to the main menu: ")

        else:
            print("Password is incorrect!! Please try again")

def change_master():

        print('''
    ---------------------------------- 
          CHANGE MASTER PASSWORD
    ----------------------------------
    Press Q to return to the main menu
    ---------------------------------- \n''')

        not_correct = True
        
        while not_correct:
            email = input("Please enter the master email: ")
            get = MPDatabase()
            confirm =  get.get_master_password()
            get_email = MPDatabase()
            master_email = get_email.get_master_email()
            if email == master_email:
                password = getpass("Password: ")
                if confirm == password:
                    pwd = input("Please enter the a password to hash: ")
                    edit = MPDatabase()
                    edit.update_master_password(email, pwd)
                    print()
                    print("Master password has been generated and sent to your email address.".upper())
                    menu()

            elif email == 'q' or 'Q':
                menu()

            else:
                print("Details are incorrect!! Please try again")

def view():
    to_view = True
    while to_view:
        app = input("Enter the name of the app: ")
        password = getpass("Password: ")
        get = MPDatabase()
        confirm =  get.get_master_password()
        if confirm == password:
            find = MPDatabase()
            find.find(app)
        print()
        choice = input("Would you like to view another? [Y/y N/n]: ")
        if choice == 'y':
            to_view = True
        elif choice == 'n':
            menu()
        elif choice == 'q':
            menu()
        elif choice == '':
            print("Please choose Y/y or N/n. Press q to return to the main menu: ")
        else:
            print("Please choose Y/y or N/n. Press q to return to the main menu: ")

def menu():
    print('''
    ----------------------------------
                  Menu
    ----------------------------------
     What would you like to do? 
     Enter Q to quit.
    ----------------------------------
    1. Add Password
    2. View Password
    3. View Account
    4. Change Master Details
    ----------------------------------\n''')
    choice = input().lower()
    if choice == 'q':
         quit()
    elif choice == '1':
        add_password()
    elif choice == '2':
        view_password()
    elif choice == '3':
        view()
    elif choice == '4':
         change_master()


if __name__ == '__main__':
    title()

while True:

    t = MPDatabase()
    table_empty = t.is_empty()
    if table_empty:
        setup()
    else:
        login()
    