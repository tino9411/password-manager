from os import writev
from cryptography.fernet import Fernet

class EncryptDecrypt:
    def __init__(self):
        
        key = Fernet.generate_key()
        self.key = key
    
    def write_key(self):
        """
        Generates a new key and saves it to a file.
        """
        with open("secret.key", "wb") as key_file:
            key_file.write(self.key)

    def load_key(self):
        """
        Loads the current key.
        """
        file = open("password-manager/secret.key", "rb")
        k = file.read()
        file.close()
        return k

    def encrypt_password(self, pwd):

        """ Encrypts the password the user would like to save"""

        k = EncryptDecrypt().load_key()
        f = Fernet(k)
        epwd = f.encrypt(pwd.encode()).decode()

        return epwd
    
    def decrypt_password(self, epwd):

        """ 
        Decrypts the password so the user can retrieve it
        """
        k = EncryptDecrypt().load_key()
        f = Fernet(k)
        pwd = f.decrypt(epwd.encode()).decode()

        return pwd


'''e = EncryptDecrypt()
p = e.encrypt_password("hello")
print(p)'''