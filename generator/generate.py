from random import randint

featureNames = [
    "add",
    "sub",
    "xor",
    "mul",
    "a == 0",
    "a == ffffffff",
    "b == 0",
    "b == ffffffff",
    "a == b",
    "a == !b",
    "a + b >= 2^32",
    "a_signed < 0",
    "b_signed < 0",
    "a_signed > 0",
    "b_signed > 0",
    "a_signed + b_signed >= 2^31",
    "a_signed + b_signed < -2^31"
]

def randHex():
    x = randint(0,99)
    if x < 20:
        return 0x00000000
    elif x < 40:
        return 0xffffffff
    else:
        return randint(0,2**32-1)

def makeTest():
    res = {}
    x = randint(0, 99)
    if x < 25:
        res['op'] = 'add'
    elif x < 50:
        res['op'] = 'sub'
    elif x < 75:
        res['op'] = 'xor'
    else:
        res['op'] = 'mul'

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
    return features

def getHexNum(n):
    res = hex(n)[2:]
    res = '0'*(8-len(res)) + res
    return res

def getHex(test):
    res = '01002283\n01402303\n'
    op = test['op']
    if op == 'add':
        res += '005303b3'
    elif op == 'sub':
        res += '405303b3'
    elif op == 'xor':
        res += '005343b3'
    elif op == 'mul':
        res += '025303b3'
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
for i in range(10):
    test = makeTest()
    features = getTestFeatures(test)
    hx = getHex(test)
    fStr = getFeatureStr(features)
    hexFile.write(hx)
    featuresFile.write(fStr+'\n')
hexFile.close()
featuresFile.close()
