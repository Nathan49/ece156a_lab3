from Instruction import *
from sys import argv

labelMap = {}
baseAddr = 0x000

def compile(inFileName, outFileName):
    global labelMap, baseAddr

    inFile = open(inFileName, 'r');

    instrs = []
    lineN = 0
    for line in inFile:
        # clean up the line
        line = removeComments(line)
        line = line.strip().split(' ')

        if len(line) is 1 and line[0] is '':
            # ignore blank lines
            continue

        # print(line)

        if line[0][-1] is ':':
            labelMap[line[0][:-1]] = baseAddr + lineN
        else:
            instrs.append(Instruction(line, lineN))
            lineN += 4

    inFile.close()

    # parse arguments in instructions
    for instr in instrs:
        # print(instr.string)
        instr.parseArgs(labelMap)

    # use labels to set jump/branch addresses
    for instr in instrs:
        instr.updateLabel(labelMap)

    # get binary representations
    for instr in instrs:
        instr.setBinString()

    # print("\nParsed",len(instrs),"instructions:")

    # print("Labels:",labelMap)

    for i in instrs:
        print(i.string + (' '*(40 - len(i.string))) + ' ==> ' + i.hexString)

    s = ''
    for i in instrs:
        s += i.hexString + '\n'

    with open(outFileName, 'w') as file:
        file.write(s)

def removeComments(string):
    poundI = string.find('#');
    if poundI == -1:
        return string
    return string[0:poundI]

def main():
    if len(argv) != 3:
        print("ERROR: please call the RISC V python compiler with input and output file names")
        print("Example: python3 riscCompile.py hexFiles/test5.s hexFiles/test2.hex")
        return

    compile(argv[1], argv[2])

main()