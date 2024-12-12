import periodictable as pt

##############################################
# CUSTOM ELEMENT TO HANDLE CODES OUT OF RANGE
##############################################

class LoopCounterElement(pt.core.Element):
    """
    A custom element class to handle elements with codes out of the periodic table range.\n
    It store in the mass: `900 + loop counter` how many time we looped out of range over the periodic table to finaly fit the ASCII code in the table.\n
    The name store the element that we finally are able to fit into as last part this element name.\n
    """
    def __init__(self, cnt: int, el: pt.core.Element):        
        # Initialize the parent class
        super().__init__(
            name=f"Loopcounterium-{cnt}-{el.name}",
            symbol=f"Lc{el.symbol}{cnt}",
            Z=900 + cnt,
            ions=(),
            table="public"
        )
        
        self._mass = 900 + cnt

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

##############################################
# GET ELEMENTS
##############################################

def getElementByNumber(number: int) -> pt.core.Element:
    return pt.elements[number]

def getElementByName(name: str) -> pt.core.Element:
    return pt.elements.name(name)

def getLastElement() -> pt.core.Element:
    bst = 0
    for e in pt.elements:
        if e.number > bst:
            bst = e.number
    return getElementByNumber(bst)

##############################################
# TEXT ----> ELEMENTS
##############################################

def turnCharacterIntoElement(character: chr) -> pt.core.Element:
    el = None
    last = getLastElement().number

    code = ord(character)

    #gotta truncate or it won't fit periodic table
    if code > last:
        quot = code // last
        truncated_code = code % last

        return LoopCounterElement(
            quot,
            getElementByNumber(truncated_code)
        )

    else:
        return getElementByNumber(code)

def turnStringIntoElements(string: str) -> list[pt.core.Element]:
    lst: list[pt.core.Element] = []
    for c in string:
        lst.append(turnCharacterIntoElement(c))
    return lst

##############################################
# ELEMENTS ----> TEXT
##############################################

def turnElementIntoCharacter(element: pt.core.Element) -> chr:
    if (element.number < 900):
        #its a normal element
        return chr(element.number)
    else:
        #its a loop counter element
        loopCount = element.number - 900
        normalElementName = element.name.split("-")[-1]

        excess = loopCount * getLastElement().number

        return chr(excess + getElementByName(normalElementName).number)

def turnElementsIntoString(elementList: list[pt.core.Element]) -> str:
    string = ""
    for e in elementList:
        string += turnElementIntoCharacter(e)
    return string