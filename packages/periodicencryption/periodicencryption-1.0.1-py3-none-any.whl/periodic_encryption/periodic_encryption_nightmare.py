# source
# splitting chars : https://www.geeksforgeeks.org/python-split-string-into-list-of-characters/
# idea of how vignere table work : https://www.youtube.com/watch?v=jVpsLMCIB0Y
# get ASCII code : https://www.programiz.com/python-programming/examples/ascii-character

import string

# Periodic Table Date: Current as of January 2022
periodic_table = {
    1: ['H', 'Hydrogen'],
    2: ['He', 'Helium'],
    3: ['Li', 'Lithium'],
    4: ['Be', 'Beryllium'],
    5: ['B', 'Boron'],
    6: ['C', 'Carbon'],
    7: ['N', 'Nitrogen'],
    8: ['O', 'Oxygen'],
    9: ['F', 'Fluorine'],
    10: ['Ne', 'Neon'],
    11: ['Na', 'Sodium'],
    12: ['Mg', 'Magnesium'],
    13: ['Al', 'Aluminum'],
    14: ['Si', 'Silicon'],
    15: ['P', 'Phosphorus'],
    16: ['S', 'Sulfur'],
    17: ['Cl', 'Chlorine'],
    18: ['Ar', 'Argon'],
    19: ['K', 'Potassium'],
    20: ['Ca', 'Calcium'],
    21: ['Sc', 'Scandium'],
    22: ['Ti', 'Titanium'],
    23: ['V', 'Vanadium'],
    24: ['Cr', 'Chromium'],
    25: ['Mn', 'Manganese'],
    26: ['Fe', 'Iron'],
    27: ['Co', 'Cobalt'],
    28: ['Ni', 'Nickel'],
    29: ['Cu', 'Copper'],
    30: ['Zn', 'Zinc'],
    31: ['Ga', 'Gallium'],
    32: ['Ge', 'Germanium'],
    33: ['As', 'Arsenic'],
    34: ['Se', 'Selenium'],
    35: ['Br', 'Bromine'],
    36: ['Kr', 'Krypton'],
    37: ['Rb', 'Rubidium'],
    38: ['Sr', 'Strontium'],
    39: ['Y', 'Yttrium'],
    40: ['Zr', 'Zirconium'],
    41: ['Nb', 'Niobium'],
    42: ['Mo', 'Molybdenum'],
    43: ['Tc', 'Technetium'],
    44: ['Ru', 'Ruthenium'],
    45: ['Rh', 'Rhodium'],
    46: ['Pd', 'Palladium'],
    47: ['Ag', 'Silver'],
    48: ['Cd', 'Cadmium'],
    49: ['In', 'Indium'],
    50: ['Sn', 'Tin'],
    51: ['Sb', 'Antimony'],
    52: ['Te', 'Tellurium'],
    53: ['I', 'Iodine'],
    54: ['Xe', 'Xenon'],
    55: ['Cs', 'Cesium'],
    56: ['Ba', 'Barium'],
    57: ['La', 'Lanthanum'],
    58: ['Ce', 'Cerium'],
    59: ['Pr', 'Praseodymium'],
    60: ['Nd', 'Neodymium'],
    61: ['Pm', 'Promethium'],
    62: ['Sm', 'Samarium'],
    63: ['Eu', 'Europium'],
    64: ['Gd', 'Gadolinium'],
    65: ['Tb', 'Terbium'],
    66: ['Dy', 'Dysprosium'],
    67: ['Ho', 'Holmium'],
    68: ['Er', 'Erbium'],
    69: ['Tm', 'Thulium'],
    70: ['Yb', 'Ytterbium'],
    71: ['Lu', 'Lutetium'],
    72: ['Hf', 'Hafnium'],
    73: ['Ta', 'Tantalum'],
    74: ['W', 'Tungsten'],
    75: ['Re', 'Rhenium'],
    76: ['Os', 'Osmium'],
    77: ['Ir', 'Iridium'],
    78: ['Pt', 'Platinum'],
    79: ['Au', 'Gold'],
    80: ['Hg', 'Mercury'],
    81: ['Tl', 'Thallium'],
    82: ['Pb', 'Lead'],
    83: ['Bi', 'Bismuth'],
    84: ['Po', 'Polonium'],
    85: ['At', 'Astatine'],
    86: ['Rn', 'Radon'],
    87: ['Fr', 'Francium'],
    88: ['Ra', 'Radium'],
    89: ['Ac', 'Actinium'],
    90: ['Th', 'Thorium'],
    91: ['Pa', 'Protactinium'],
    92: ['U', 'Uranium'],
    93: ['Np', 'Neptunium'],
    94: ['Pu', 'Plutonium'],
    95: ['Am', 'Americium'],
    96: ['Cm', 'Curium'],
    97: ['Bk', 'Berkelium'],
    98: ['Cf', 'Californium'],
    99: ['Es', 'Einsteinium'],
    100: ['Fm', 'Fermium'],
    101: ['Md', 'Mendelevium'],
    102: ['No', 'Nobelium'],
    103: ['Lr', 'Lawrencium'],
    104: ['Rf', 'Rutherfordium'],
    105: ['Db', 'Dubnium'],
    106: ['Sg', 'Seaborgium'],
    107: ['Bh', 'Bohrium'],
    108: ['Hs', 'Hassium'],
    109: ['Mt', 'Meitnerium'],
    110: ['Ds', 'Darmstadtium'],
    111: ['Rg', 'Roentgenium'],
    112: ['Cn', 'Copernicium'],
    113: ['Nh', 'Nihonium'],
    114: ['Fl', 'Flerovium'],
    115: ['Mc', 'Moscovium'],
    116: ['Lv', 'Livermorium'],
    117: ['Ts', 'Tennessine'],
    118: ['Og', 'Oganesson']
}



letters = string.ascii_letters
digits = string.digits
special_characters = string.punctuation
unicode_characters = "ÀÁÂÃÄÅàáâãäåÈÉÊËèéêëÌÍÎÏìíîïÒÓÔÕÖØòóôõöøÙÚÛÜùúûüÝŸýÿ"

row = letters + digits + special_characters + unicode_characters





increment = 3 #how many numbers you want ascii code to be into (like 3 zeros, zfilled)



def generate_vignere_row(r,n,w):

    for i in range(0,n+1): #for each displacement needed

        cursor=0
        while (r[cursor]!=w[i]): #while not on the searched letter, continue
            cursor+=1
        
        #now move the letter all the way to the front
        sp = r.split(w[i]) #split stuff
        r = w[i] + sp[0] + sp[1] #concatenate stuff
    
    return r



def generate_vignere_table(r,w):
    table = []

    while(len(w)<len(r)): #repeat w until its same or longer than row
        w+=w
    
    w=w[:len(r)] #truncate to row lenght
    
    for i in range(0,len(r)):
        lst = [*generate_vignere_row(r,i,w)] #split each char to a list
        table.append(lst)
    
    return table



def vignere_encode_message(r, key, message, keystream):
    while len(keystream) < len(message):  # Repeat keystream until it's at least as long as the message
        keystream += keystream

    keystream = keystream[:len(message)]  # Truncate to match the length of the message

    encoded = ""
    vignere_table = generate_vignere_table(r, key)
    for i in range(len(message)):
        # Find index from keystream and message
        k_i = r.find(keystream[i])
        m_i = r.find(message[i])

        # Find corresponding char within the table
        c = vignere_table[m_i][k_i]

        encoded += c

    return encoded



def turn_message_into_ascii(inc,message):
    res=[]

    for i in message:
        ascii = ord(i)
        if (ascii > max(periodic_table.keys())):
            print("         Character need to be adjusted")
            ascii = ascii % max(periodic_table.keys())
            print("         Adjusted to : ",ascii)
            
        res.append(str(ascii).zfill(inc))

    return res



def encode_once(inc,r,message):

    print("Step 1 | Turn into ASCII")

    #turn to ascii
    step1 = turn_message_into_ascii(inc,message)

    print("         Result : ",step1)

    #############################################################

    print("Step 2 | Turn into periodic table initials")

    #find initials
    step2 = ""
    key = ""
    keystream = ""

    for i in range(len(step1)):
        elem = periodic_table[int(step1[i])]
        step2 += elem[0] #add the initial

        if i == 0: #If there is only one character, the key is the same as the character
            opposite_elem = periodic_table[int(step1[-1])]
            key += elem[1] + opposite_elem[0] #add the element name and the opposite element initial
        else:
            opposite_elem = periodic_table[int(step1[i - 1])]
            key += opposite_elem[0] #add the opposite element initial

        opposite_elem = periodic_table[int(step1[(i + 1) % len(step1)])] #get the next element
        keystream += elem[1] + opposite_elem[0]

    print("         Result : ",step2)
    print("         Vignere key : ",key)
    print("         Encoding Vignere key : ",keystream)

    #############################################################

    print("Step 3 | Encode with a Vignere table")

    #encode with vignere
    step3 = vignere_encode_message(r,key,step2,keystream)

    print("         Result : ",step3)

    #############################################################

    print("Step 4 | Reverse it")

    #reverse it
    res = step3[::-1]

    print("         Result : ",res)

    return res


def encode(inc,r,round,message):

    if (len(message)>0):

        res=message

        for i in range(0,round):
            print("Round ",i+1)

            res=encode_once(inc,r,res)
        
        return res
    else:
        raise Exception("Il faut au moins 1 caractère")
    
    




print("\n\n========================================================\n\n")
print(encode(increment,row,1,"sale pute"))