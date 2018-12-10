from random import randint

nTests = 1000

featureNames = [
    'add',
    'sub',
    'xor',
    'mul',
    'jal',
    'a == 0',
    'a == ffffffff',
    'b == 0',
    'b == ffffffff',
    'a == b',
    'a == !b',
    'a + b >= 2^32',
    'a_signed < 0',
    'b_signed < 0',
    'a_signed > 0',
    'b_signed > 0',
    'a_signed + b_signed >= 2^31',
    'a_signed + b_signed < -2^31',
    'b_signed > a_signed',
    'a_signed - b_signed < -2^31',
    'a_signed - b_signed >= 2^31',
    'rs1 == t2',
    'rs2 == t2'
]

opcodes = ['add', 'sub', 'xor', 'mul', 'jal']

regMap = ['00101', '00110', '00111']

def randHex():
    x = randint(0,99)
    if x < 20:
        return 0x00000000
    elif x < 40:
        return 0xffffffff
    else:
        return randint(0,2**32-1)

def randOpCode():
    return opcodes[randint(0,len(opcodes)-1)]

def makeTest():
    res = {}
    res['op'] = opcodes[randint(0,3)]
    res['op2'] = opcodes[randint(0,4)]
    res['rs1'] = randint(0,2)
    res['rs2'] = randint(0,2)

    res['a'] = randHex()
    res['b'] = randHex()
    return res

def getSigned(n):
    return n - 2**32 if n >= 2**31 else n

def getTestFeatures(test):
    features = {}
    for fn in featureNames:
        features[fn] = False
    features[test['op']] = True
    if test['op2'] == 'jal':
        features['jal'] = True
    else:
        if test['rs1'] == 2:
            features['rs1 == t2'] = True
        elif test['rs2'] == 2:
            features['rs2 == t2'] = True
    a = test['a']
    b = test['b']
    if a == 0:
        features['a == 0'] = True
    elif a == 0xffffffff:
        features["a == ffffffff"] = True
    if b == 0:
        features['b == 0'] = True
    elif b == 0xffffffff:
        features["b == ffffffff"] = True
    if a == b:
        features['a == b'] = True
    if a == (b ^ 0xffffffff):
        features["a == !b"] = True
    if a + b >= 2**32:
        features['a + b >= 2^32'] = True
    a_signed = getSigned(a)
    b_signed = getSigned(b)
    if a_signed > 0:
        features['a_signed > 0'] = True
    elif a_signed < 0:
        features['a_signed < 0'] = True
    if b_signed > 0:
        features['b_signed > 0'] = True
    elif b_signed < 0:
        features['b_signed < 0'] = True
    if a_signed + b_signed >= 2**31:
        features["a_signed + b_signed >= 2^31"] = True
    elif a_signed + b_signed < -2**31:
        features["a_signed + b_signed < -2^31"] = True
    if b_signed > a_signed:
        features["b_signed > a_signed"] = True
    if a_signed - b_signed < -2**31:
        features['a_signed - b_signed < -2^31'] = True
    if a_signed - b_signed >= 2**31:
        features['a_signed - b_signed >= 2^31'] = True
    return features

def getHexNum(n):
    res = hex(n)[2:]
    res = '0'*(8-len(res)) + res
    return res

def getInstrHex(op, rs1, rs2):
    res = ''
    if op == 'add':
        res += '0000000' + regMap[rs2] + regMap[rs1] + '000' + regMap[2] + '0110011'
    elif op == 'sub':
        res += '0100000' + regMap[rs2] + regMap[rs1] + '000' + regMap[2] + '0110011'
    elif op == 'xor':
        res += '0000000' + regMap[rs2] + regMap[rs1] + '100' + regMap[2] + '0110011'
    elif op == 'mul':
        res += '0000001' + regMap[rs2] + regMap[rs1] + '000' + regMap[2] + '0110011'
    return getHexNum(int(res, 2))

def getHex(test):
    res = '01002283\n01402303\n'
    op = test['op']
    if op == 'add':
        res += '006283b3'
    elif op == 'sub':
        res += '406283b3'
    elif op == 'xor':
        res += '0062c3b3'
    elif op == 'mul':
        res += '026283b3'
    res += '\n'
    if test['op2'] == 'jal':
        res += '0040006f'
    else:
        res += getInstrHex(test['op2'], test['rs1'], test['rs2'])
    res += '\n0000006f\n'
    res += getHexNum(test['a']) + '\n'
    res += getHexNum(test['b']) + '\n'
    return res

def getFeatureStr(features):
    return ','.join(['1' if features[f] else '0' for f in featureNames])

# make sure all features show up
for fn in featureNames:
    while True:
        test = makeTest()
        f = getTestFeatures(test)
        if f[fn]:
            break

hexFile = open('generator/hex.txt', 'w')
featuresFile = open('generator/features.csv', 'w')
featuresFile.write(','.join(featureNames)+'\n')
for i in range(nTests):
    test = makeTest()
    # test = {'op': 'sub', 'a': 0xfffffff0, 'b': 0x10}
    features = getTestFeatures(test)
    hx = getHex(test)
    fStr = getFeatureStr(features)

    # print(test)
    # print(features)
    # print(hx)
    # continue

    hexFile.write(hx)
    featuresFile.write(fStr+'\n')
    # print('op: {}, a: {}, b: {}'.format(
    #     test['op'],
    #     hex(test['a']),
    #     hex(test['b'])
    # ))
    # for f in features:
    #     if features[f]:
    #         print(f)
    # # print(features)
    # print(hx)
hexFile.close()
featuresFile.close()
