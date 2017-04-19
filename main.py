'''
grammer as below:
expr   :  term  (( ADD | SUB ) term )*
term   :  factor(( MUL | DIV ) factor )*
factor :  Integer | LPA  expr  RPA
'''

EOF, ADD, SUB, MUL, DIV = ( 'EOF', 'ADD', 'SUB', 'MUL', 'DIV' )
LPA, RPA = ( 'LPA', 'RPA' )
INTEGER = 'INTEGER'

class Token:
    def __init__(self, type, value):
        self.type  = type
        self.value = value

class Scanner:
    def __init__(self, text):
        # assume text is not empty
        self.text = text
        self.pos  = 0
        self.currChar = text[ self.pos ]

    def Unknown(self, c):
        raise Exception('Unknown char "{}"'.format(c) )

    def forward(self):
        self.pos += 1
        if len( self.text ) > self.pos :
            self.currChar = self.text[ self.pos ]
        else:
            self.currChar = None

    def NextT(self):
        if self.pos >= len( self.text ):
            return Token(EOF, None)

        while self.currChar and self.currChar.isspace() :
           self.forward()

        if not self.currChar:
            return Token(EOF, None)

        if self.currChar == '+':
            self.forward()
            return Token(ADD, '+')
        if self.currChar == '-':
            self.forward()
            return Token(SUB, '-')
        if self.currChar == '*':
            self.forward()
            return Token(MUL, '*')
        if self.currChar == '/':
            self.forward()
            return Token(DIV, '/')
        if self.currChar == '(':
            self.forward()
            return Token(LPA, '(')
        if self.currChar == ')':
            self.forward()
            return Token(RPA, ')')

        integer = ''
        while self.currChar and self.currChar.isdigit():
            integer += self.currChar
            self.forward()
        if integer:
            return Token(INTEGER, integer)

        self.Unknown( self.currChar )


class Parser:
    def __init__(self, scan):
        self.scannr = scan
        self.currT  = scan.NextT()

    def validSyntax(self, t):
        if self.currT.type != t :
            raise Exception('Syntax Error, type mismatch, expect {} got {}'.format(t, self.currT.type) )
        else:
            self.currT = self.scannr.NextT()

    def getNextToken(self):
        self.currT = self.scannr.NextT()

    def getInt(self):
        val = self.currT.value
        if self.currT.type == INTEGER:
            self.validSyntax(INTEGER)
            val = int( val )
            val = self.getOp( val, MUL, DIV )
        elif self.currT.type == LPA:

            self.validSyntax(LPA)
            val = self.parse()
            self.validSyntax(RPA)
            val = self.getOp( val, MUL, DIV )

        return int(val)

    def getOp(self, left, *args):
        val = left
        while self.currT.type in args:
            if self.currT.type == MUL:
                self.getNextToken()
                val = val * self.getInt()
            elif self.currT.type == DIV:
                self.getNextToken()
                val = val / self.getInt()
            elif self.currT.type == ADD:
                self.getNextToken()
                val = val + self.getInt()
            elif self.currT.type == SUB:
                self.getNextToken()
                val = val - self.getInt()

        return val

    def parse(self):
        ret = self.getInt()
        ret = self.getOp( ret, ADD, SUB )
        return ret


class Interpreter(Parser):
    def __init__(self, text):
        self.scannr = Scanner(text)
        self.parser = Parser(self.scannr)

    def go(self):
        return self.parser.parse()

def main():
    while True:
        try:
            text = raw_input('myCalculator> ')
        except Exception, err:
            print err
            break

        if not text:
            continue

        try:
            interpretr  = Interpreter(text)
            print interpretr.go()
        except Exception, err:
            print err


if __name__ == '__main__':
    main()
