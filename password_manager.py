from os import writev
from cryptography.fernet import Fernet



def write_key():                                    # This function generates the key needed to encrypt the password, then writes it to 'key.key'
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:         # Open the file key.key and assign to key_files
        key_file.write(key)

def load_key():                                    # This function loads the key needed to encrypt the password from 'key.key'
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key 


def view():
    with open("passwords.txt", 'r') as r:  # Create new file if it does not exit and add data.
        for line in r.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())


def add():
    name = input("Account Name: ")
    pwd = input("Password: ")

    with open("passwords.txt", 'a') as f:  # Create new file if it does not exit and add data.
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

master_pwd = input("What is the master password? ")
key = load_key() + master_pwd.encode()
fer = Fernet(key)


while True:
    mode = input("Would you like to add a new password or view exisiting ones (view or add)? Press q to quit: ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue