from subprocess import call

flagList = [
    "Unsigned Overflow",
    "Signed Overflow",
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

    return ['1' if flag in flags else '0' for flag in flagList]

def main():
    hexSourcePath = 'generator/hex.txt'
    assemblyPath = 'generator/assembly.txt'
    tablePath = 'generator/features.csv'

    hexFile = open(hexSourcePath, 'r')
    assemblyFile = open(assemblyPath, 'r')
    tableFile = open(tablePath, 'r');

    featureNames = tableFile.readline()[:-1].split(', ')

    progs = []      # hex file strings
    features = []   # boolean array that maps to featureList
    flags = []      # boolean array of which flags were tripped

    # set the features
    with open('generator/features.csv', 'r') as f:
        f.readline()
        for line in f:
            features.append(line[:-1].split(','))

    # set the programs
    i = 0
    while True:
        line = hexFile.readline()
        if line == '':
            break
        if i == 0:
            progs.append('')
        i += 1
        if i == 6:
            i = 0
        progs[-1] += line

    # run the programs and see which flags were set
    for p in progs:
        with open('hexFiles/temp.hex', 'w') as progFile:
            progFile.write(p);
        call(["make sim"], shell = True)
        flags.append(parseFlags('run/flags.txt'))
        # print(flags[-1])

    # save all the info in an output file
    with open('run/out.txt', 'w') as f:
        f.write(','.join(featureNames) + '\n')
        f.write(','.join(flagList) + '\n')
        for i in range(len(features)):
            f.write(','.join(features[i]) + '\n')
            f.write(','.join(flags[i]) + '\n')

    hexFile.close()
    assemblyFile.close()
    tableFile.close()

main()