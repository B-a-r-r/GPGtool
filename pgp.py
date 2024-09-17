import gnupg
import os

gpg = gnupg.GPG(gnupghome = '/home/cleme/.gnupg')
gpg.encoding = 'utf-8'

def keygen()->None:
    key = gpg.gen_key(
        gpg.gen_key_input(
            name_email = str(input("[!] Enter your email: ")),
            passphrase = str(input("[!] Enter your passphrase: ")),
            key_type = 'RSA',
            key_length = 2048
        )
    )
    
def encrypt_file(path_to_file:str)->None:
    with open(path_to_file, 'rb') as f:
        status = gpg.encrypt_file(
            f, 
            recipients = [str(input("[!] Enter recipient's email: "))],
            output = path_to_file + '.enc'
        )
    print(status.ok)
    print(status.stderr)

def decrypt_file(path_to_file:str)->None:
    with open(path_to_file, 'rb') as f:
        status = gpg.decrypt_file(
            f,
            passphrase = str(input("[!] Enter your passphrase: ")),
            output = path_to_file + '.dec'
        )
    print(status.ok)
    print(status.stderr)