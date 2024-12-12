import periodictable as pt
import re
from periodicencryption import vigenerecipher as vc
from periodicencryption import element as el

def giveKeysFromList(elementList: list[pt.core.Element]) -> tuple[str, str]:
    """
    Generates the private and public keys, needed for the encryption process, from a list of Chemical Elements.
    """
    if len(elementList) == 0:
        raise ValueError("Element list cannot be empty.")

    firstElement = elementList[0]
    lastElement = elementList[-1]

    # private key : 1st element name + last element symbol + 1st element symbol + last element name
    privateKey = firstElement.name.capitalize() + lastElement.symbol + firstElement.symbol + lastElement.name.capitalize()
    # public key : last element mass + 1st element name + last element name + 1st element mass
    publicKey = str(lastElement.mass) + firstElement.name.capitalize() + lastElement.name.capitalize() + str(firstElement.mass)

    return "".join(dict.fromkeys(publicKey)), "".join(dict.fromkeys(privateKey)) # remove duplicates



def giveKeysFromString(string: str) -> tuple[str, str]:
    """
    Generates the private and public keys, needed for the encryption process, from a string.
    """
    publicKey, privateKey = giveKeysFromList(el.turnStringIntoElements(string))
    return publicKey, privateKey



def encrypt(row: str, message: str) -> str:
    """
    Encrypts a message using the Vigenère cipher and the periodic table elements.
    """
    if len(message) == 0:
        raise ValueError("Message cannot be empty.")

    # 1 - turn message into elements

    elementList = el.turnStringIntoElements(message)

    # 2 - encode message using Vigenère cipher

    publicKey, privateKey = giveKeysFromList(elementList)

    stringElement = ''.join([e.symbol for e in elementList])

    encodedMessage = vc.encode(row, publicKey, privateKey, stringElement)
    
    return encodedMessage



def decrypt(row: str, publicKey: str, privateKey: str, message: str) -> str:
    """
    Decrypts a message using the Vigenère cipher and the periodic table elements.
    """
    if len("".join(dict.fromkeys(publicKey))) != len(publicKey) or len("".join(dict.fromkeys(privateKey))) != len(privateKey):
        raise ValueError("Public and private keys must not contain duplicates.")
    
    if len(message) == 0:
        raise ValueError("Message cannot be empty.")
    
    # 1 - decode message using Vigenère cipher

    decodedMessage = vc.decode(row, publicKey, privateKey, message)

    # 2 - turn elements into message

    elementNames = re.findall('[A-Z][^A-Z]*', decodedMessage)
    elementList = [el.getElementBySymbol(name) for name in elementNames]

    finalMessage = el.turnElementsIntoString(elementList)

    return finalMessage