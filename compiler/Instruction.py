from registerMap import *

class Instruction:
    opcodeMap = {
        'add': 0b0110011,
        'sub': 0b0110011,
        'addi': 0b0010011,
        'mul': 0b0110011,
        'lw': 0b0000011,
        'lui': 0b0110111,
        'ori': 0b0010011,
        'xor': 0b0110011,
        'beq': 0b1100011,
        'blt': 0b1100011,
        'bge': 0b1100011,
        'bne': 0b1100011,
        'jal': 0b1101111,
        'sw': 0b0100011,
        'srl': 0b0110011
    }

    typeMap = {
        'add': 'R',
        'sub': 'R',
        'addi': 'I',
        'mul': 'R',
        'xor': 'R',
        'lw': 'I',
        'lui': 'U',
        'ori': 'I',
        'beq': 'SB',
        'blt': 'SB',
        'bge': 'SB',
        'bne': 'SB',
        'jal': 'UJ',
        'sw': 'S',
        'srl': 'R'
    }

    func3Map = {
        'add': '000',
        'sub': '000',
        'sll': '001',
        'slt': '010',
        'sltu': '011',
        'xor':  '100',
        'srl': '101',
        'sra': '101',
        'or': '110',
        'and': '111',

        'mul': '000',

        'addi': '000',
        'slti': '010',
        'sltiu': '011',
        'xori': '100',
        'ori': '110',
        'andi': '111',

        'slli': '001',
        'srli': '101',
        'srai': '101',

        'lb': '000',
        'lh': '001',
        'lw': '010',
        'lbu': '100',
        'lhu': '101',

        'sb': '000',
        'sh': '001',
        'sw': '010',

        'beq': '000',
        'bne': '001',
        'blt': '100',
        'bge': '101'
    }

    func7Map = {
        'slli': '0000000',
        'srli': '0000000',
        'srai': '0100000',

        'add': '0000000',
        'sub': '0100000',
        'mul': '0000001',
        'sll': '0000000',
        'slt': '0000000',
        'sltu': '0000000',
        'xor':  '0000000',
        'srl': '0000000',
        'sra': '0100000',
        'or': '0000000',
        'and': '0000000'
    }

    def __init__(self, string, lineN):
        self.lineN = lineN
        self.args = string[1:]
        self.instr = string[0]
        self.opcode = Instruction.opcodeMap[self.instr]
        self.type = Instruction.typeMap[self.instr]
        self.string = ' '.join(string)
        self.rd = None
        self.rs1 = None
        self.rs2 = None
        self.funct3 = None
        self.funct7 = None
        self.imm = None
        self.label = None
        self.binString = None
        self.hexString = None
    
    def parseArgs(self, labelMap):
        if self.type is 'R':
            self.rd = parseRegister(self.args[0])
            self.rs1 = parseRegister(self.args[1])
            self.rs2 = parseRegister(self.args[2])
        
        elif self.type is 'I':
            self.rd = parseRegister(self.args[0])
            self.rs1 = parseRegister(self.args[1])
            self.imm = parseNumber(self.args[2], labelMap)

        elif self.type is 'S':
            self.rs1 = parseRegister(self.args[0])
            self.rs2 = parseRegister(self.args[1])
            self.imm = parseNumber(self.args[2], labelMap)

        elif self.type is 'SB':
            self.rs1 = parseRegister(self.args[0])
            self.rs2 = parseRegister(self.args[1])
            self.label = self.args[2]

        elif self.type is 'U':
            self.rd = parseRegister(self.args[0])
            self.imm = parseNumber(self.args[1], labelMap)

        elif self.type is 'UJ':
            self.rd = parseRegister(self.args[0])
            self.label = self.args[1]

    def __repr__(self):
        res = '{}({}): '.format(self.instr, self.type)
        if self.type is 'R':
            res += '{}, {}, {}'.format(
                self.rd,
                self.rs1,
                self.rs2
            )
        elif self.type is 'I':
            res += '{}, {}, imm: {}'.format(
                self.rd,
                self.rs1,
                self.imm
            )
        elif self.type is 'S':
            res += '{}, {}, imm: {}'.format(
                self.rs1,
                self.rs2,
                self.imm
            )
        elif self.type is 'SB':
            res += '{}, {}, jumps to {}'.format(
                self.rs1,
                self.rs2,
                self.imm
            )
        elif self.type is 'U':
            res += '{}, imm: {}'.format(
                self.rd,
                self.imm
            )
        elif self.type is 'UJ':
            res += '{}, jumps to {}'.format(
                self.rd,
                self.imm
            )
        
        return res

    def updateLabel(self, labelMap):
        if self.type is 'SB':
            self.imm = (labelMap[self.label] - self.lineN)
        
        elif self.type is 'UJ':
            self.imm = (labelMap[self.label] - self.lineN)

    def setBinString(self):
        opcodeStr = binString(self.opcode, 7)

        if self.type is 'R':
            rdStr = binString(self.rd, 5)
            func3Str = Instruction.func3Map[self.instr]
            rs1Str = binString(self.rs1, 5)
            rs2Str = binString(self.rs2, 5)
            func7Str = Instruction.func7Map[self.instr]
            self.binString =   func7Str     \
                             + rs2Str       \
                             + rs1Str       \
                             + func3Str     \
                             + rdStr        \
                             + opcodeStr
        
        elif self.type is 'I':
            rdStr = binString(self.rd, 5)
            func3Str = Instruction.func3Map[self.instr]
            rs1Str = binString(self.rs1, 5)
            immStr = binString(self.imm, 12)
            self.binString =   immStr       \
                             + rs1Str       \
                             + func3Str     \
                             + rdStr        \
                             + opcodeStr

        elif self.type is 'S':
            func3Str = Instruction.func3Map[self.instr]
            rs1Str = binString(self.rs1, 5)
            rs2Str = binString(self.rs2, 5)
            immStr = binString(self.imm, 12)
            self.binString =   immStr[:12-5]    \
                             + rs2Str           \
                             + rs1Str           \
                             + func3Str         \
                             + immStr[11-4:]    \
                             + opcodeStr

        elif self.type is 'SB':
            func3Str = Instruction.func3Map[self.instr]
            rs1Str = binString(self.rs1, 5)
            rs2Str = binString(self.rs2, 5)
            immStr = binString(self.imm, 13)
            immA = immStr[12-12]
            immB = immStr[12-10:13-5]
            immC = immStr[12-4:13-1]
            immD = immStr[12-11]
            self.binString =   immA         \
                             + immB         \
                             + rs2Str       \
                             + rs1Str       \
                             + func3Str     \
                             + immC         \
                             + immD         \
                             + opcodeStr

        elif self.type is 'U':
            rdStr = binString(self.rd, 5)
            immStr = binString(self.imm, 20)
            self.binString =   immStr       \
                             + rdStr        \
                             + opcodeStr

        elif self.type is 'UJ':
            rdStr = binString(self.rd, 5)
            immStr = binString(self.imm//2, 21)
            # print(self.imm)
            # print(immStr)
            immA = immStr[21-20]
            immB = immStr[21-10:22-1]
            immC = immStr[21-11]
            immD = immStr[21-19:22-12]
            self.binString =   immA         \
                             + immB         \
                             + immC         \
                             + immD         \
                             + rdStr        \
                             + opcodeStr

        self.setHexString()

    def setHexString(self):
        n = int(self.binString, 2)
        n = hex(n)[2:]
        if len(n) < 8:
            n = '0'*(8-len(n)) + n
        self.hexString = n

# Returns a two's complement string of the number
# binString( 7, 16) ==> '0000000000000111'
# binString(-7, 16) ==> '1111111111111001'
def binString(num, numLen):
    # for positive num: add extra 0 padding
    # for negative num: do 2's complement adjustment
    num += 2**numLen

    # get binary string without the '0b'
    res = bin(num)[2:]

    # remove the extra '1' from positive numbers
    if len(res) is numLen+1:
        res = res[1:]

    return res

def parseRegister(string):
    # remove the $
    if string[0] == '$':
        string = string[1:]

    # remove the comma
    string = string.strip(',')

    return registerMap[string]


def parseNumber(string, labelMap):
    num = None

    # special case: number is a label
    if string[0].isalpha():
        return labelMap[string]

    try:
        num = int(string)
    except:
        # not easy to parse as number
        if len(string) > 2:
            # try binary
            if string[0:2] == '0b':
                try:
                    num = int(string[2:], 2)
                except:
                    pass
            elif string[0:2] == '0x':
                try:
                    num = int(string[2:], 16)
                except:
                    pass

    return num