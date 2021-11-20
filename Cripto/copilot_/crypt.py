import random
import time

def randint(range):
    random.seed(int(time.time()) % range)
    return random.randint(0, range)

class Encrypt:
    """
    Encrypts a string using a key.
    """
    def __init__(self, string, key):
        self.key = key
        self.string = string
   
    def encrypt_string(self):
        """
        Encrypts a string using a key.
        """
        encrypted_string = ''
        print(self.string)
        for char in self.string:
            encrypted_string += chr(ord(char) + self.key)
        return encrypted_string

class Decrypt:
    """
    Decrypt some string using a key.
    """
    def __init__(self, encrypted_string, key) -> None:
        self.encrypted_string = encrypted_string
        self.key = key
    
    def decrypt_string(self):
        """
        Decrypts a string using a key.
        """
        decrypted_string = ''
        for char in self.encrypted_string:
            decrypted_string += chr(ord(char) - self.key)
        return decrypted_string
        

class Log:
    def __init__(self, string):
        self.string = string

    def log_string(self):
        """
        Logs a string to a file.
        """
        with open('log.txt', 'a') as log:
            log.write(self.string)


flag = 'bCTF{fake_flag_for_testing}'

Log(f"{time.time()} -> {Encrypt(flag, randint(100)).encrypt_string()}").log_string()
print(open('log.txt').read())


