import package_install as pkg
pkg.precheck_imports(['base64','pandas','pyodbc','cryptography'])


import pandas as pd
import base64
import pyodbc
import cryptography.fernet as f

def obfuscate(text):
    """No further details provided for security.

    Args:
        text (str): The string to be obfuscated.
    """
    k = b'MTJUSzFSbmJMcGFkOHlXTkl3Qnc3SUphUGtTRG5pTXBRLXBvWnRhSXpBaz0='
    obfs = f.Fernet(base64.b64decode(k))
    enc = obfs.encrypt(text.encode()).decode()
    return(enc) 
    
def deobfuscate(text):
    k = b'MTJUSzFSbmJMcGFkOHlXTkl3Qnc3SUphUGtTRG5pTXBRLXBvWnRhSXpBaz0='
    obfs = f.Fernet(base64.b64decode(k))
    decr = obfs.decrypt(text.encode()).decode()
    return decr


def connect(driver, server, database, user, enc_password):
    """Returns a secure connection to the SQL server specified. Does not have 
    default values to avoid giving context to unauthorised users.

    Args:
        driver (character): Name of the SQL Driver.
        server (character): Name of the SQL Server.
        database (character): Name of the database.
        user (character): SQL server username 
        password (character): Encrypted SQL server password

    Returns:
        conn: SQL Server secure connection
    """

    enc_password = deobfuscate(enc_password)

    if database != 'Survey_Sample_A18':
        raise Exception("This program is not intended to update the given database")

    conn = pyodbc.connect(f'Driver={driver}; Server={server}; Database={database}; Trusted_Connection=yes; uid={user};pwd={enc_password}')
    return conn
