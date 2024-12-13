import string
import pandas as pd

def generateRow() -> str:
    """
    Generates a row of characters that can be used for Vigenère cipher.
    It includes ASCII letters, digits, special characters, whitespace, and some accented  letters.
    """
    letters = string.ascii_letters
    digits = string.digits
    special_characters = string.punctuation
    whitespace = string.whitespace
    unicode_characters = "ÀÁÂÃÄÅàáâãäåÈÉÊËèéêëÌÍÎÏìíîïÒÓÔÕÖØòóôõöøÙÚÛÜùúûüÝŸýÿ"

    return letters + digits + special_characters + whitespace + unicode_characters



def generateTable(row: str, publicKey: str) -> pd.DataFrame:
    """
    Generates the Vigenère table by shifting the row based on the `publicKey`.\n
    The `publicKey` determines the shifting for each row.
    """
    rowWithoutKey = "".join([char for char in row if char not in publicKey])
    dfRow = list(publicKey + rowWithoutKey)

    df = pd.DataFrame(columns=list(dfRow), index=list(dfRow))

    # Create the first row
    df.loc[dfRow[0]] = dfRow

    df.index
    # Create the following rows
    for i in range(1, len(row)):
        dfRow = dfRow[1:] + dfRow[:1]

        df.loc[
            df.index.tolist()[i]
        ] = dfRow

    return df



def encode(row: str, publicKey: str, privateKey: str, message: str) -> str:
    """
    Encodes a message using the Vigenère cipher.
    """
    table = generateTable(row, publicKey)
    encoded_message = ""

    # Ensure len(privateKey) is at least len(message)
    privateKey = (privateKey * ((len(message) // len(privateKey)) + 1))[:len(message)]

    for m,k in zip(message, privateKey):
        encoded_message += table.loc[m][k]
    
    return encoded_message



def decode(row: str, publicKey: str, privateKey: str, encoded_message: str) -> str:
    """
    Decodes a message using the Vigenère cipher.
    """
    table = generateTable(row, publicKey)
    decoded_message = ""

    # Ensure len(privateKey) is at least len(encoded_message)
    privateKey = (privateKey * ((len(encoded_message) // len(privateKey)) + 1))[:len(encoded_message)]

    for m,k in zip(encoded_message, privateKey):
        # Find the column (publicKey) and look for the original row (message character)
        decoded_message += table[table[k] == m].index[0]
    
    return decoded_message