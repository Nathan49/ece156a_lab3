from subprocess import call

flagList = [
    "Unsigned Overflow",
    "Negative Subtraction",
    "Zero Mult",
    "Zero XOR",
    "Ones XOR",
    "Jumped",
    "Data Bypass"
]

def parseFlags(flagFile):
    flags = {}
    with open(flagFile, 'r') as f:
        for line in f:
            flags[line[:-1]] = True

    # for key in flags:
    #     print(key)

    return [True if flag in flags else False for flag in flagList]

parseFlags('generator/flags.txt')

def main():
    hexSourcePath = 'generator/hex.txt'
    assemblyPath = 'generator/assembly.txt'
    tablePath = 'generator/features.csv'

    hexFile = open(hexSourcePath, 'r')
    assemblyFile = open(assemblyPath, 'r')
    tableFile = open(tablePath, 'r');

    flags = tableFile.readline()[:-1].split(', ')
    print(flags)

    progs = []
    i = 0
    while True:
        line = hexFile.readline()
        if line == '':
            break
        if i == 0:
            progs.append('')
        i += 1
        if i == 5:
            i = 0
        progs[-1] += line

    for p in progs:
        with open('hexFiles/temp.hex', 'w') as progFile:
            progFile.write(p);
        call(["make sim"], shell = True)

        input()

    hexFile.close()
    assemblyFile.close()
    tableFile.close()