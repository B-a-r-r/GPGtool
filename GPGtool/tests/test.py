import copy
import gnupg
from os import path
import time

class Inputs:
    def __init__(self, **kwargs):
        self.args = kwargs

class GPGtool:
    
    gpg: gnupg.GPG
    keys: dict
    args: dict
    
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome = path.expanduser('~/.gnupg'))
    
    def testKwargs(self, **kwargs):
        karwargs = {}
        for key, value in kwargs.items():
            karwargs[key] = value
        return karwargs
    
    # Un script qui génère une paire de clés GPG.
    def generate_key(self, inputs: Inputs):
        karwargs = {
                'name_email' : "vds@svsooooo.com",
                'passphrase' : "1234",
                'name_real' : "VDS",
                'key_type' : "RSA",
                'key_length' : 2048,
                'key_usage' : "Test"
        }
        
        key_input = self.gpg.gen_key_input(
            name_email = "vds@svsooooo.com",
            passphrase = "1234",
            name_comment = "VDS",
            key_type = "RSA",
            key_length = 2048,
            expire_date = 0
        )
        tmp = self.gpg.gen_key(key_input)
        print(tmp)
        
    # lister les clés
    def list_keys(self):
        prop = ""
        for char in self.gpg.list_keys().__repr__():
            if char=='{':
                prop = "{"
            if (char == ',') :
                prop += '\n' 
            else :
                prop += char
        print(prop)
                
    # supprimer une clé
    def delete_key(self, key_id):
        self.gpg.delete_keys(key_id)
            
gpg = GPGtool()
gpg.generate_key(Inputs(
        name_email = "vds@svsooooo.com",
        passphrase = "1234",
        name_real = "VDS",
        key_type = "RSA",
        key_length = 2048,
        key_usage = "Test"
))
gpg.list_keys()

""" Un exemple de clé dans le keyring gnuPG:
{
    'type': 'pub'
    'trust': 'u'
    'length': '2048'
    'algo': '1'
    'keyid': '4B01A496D9C32959'
    'date': '1727629170'
    'expires': ''
    'dummy': ''
    'ownertrust': 'u'
    'sig': ''
    'cap': 'escarESCA'
    'issuer': ''
    'flag': ''
    'token': ''
    'hash': ''
    'curve': ''
    'compliance': '23'
    'updated': ''
    'origin': '0'
    'keygrip': '447736B9D9031295D5D1E841252AD6610018DD27'
    'uids': ['Alexandre Normand (Generated by GPGtool) <caca@boudin.com>']
    'sigs': []
    'subkeys': []
    'fingerprint': 'E1DF316E94BF5CBEC99AA0294B01A496D9C32959'
} 
"""