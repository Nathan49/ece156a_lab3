import random
from featureList import featureList
file = open("generator/assembly.txt", "w")
file2 = open("generator/hex.txt", "w")
file3 = open("generator/features.csv", "w")

file3.write("add, sub, xor, mult, a = 0, b = 0, a = ffffffff, b = ffffffff, a < 0, b < 0, a > 0, b > 0, ass < 0, bs < 0, ass > 0, bs > 0, unsigned overflow, signed overflow, negative sub result, xor zero, xor all ones, zero mult result, jump, data bypass\n")

featureMap = {}

# featureList = (
# 	"add",
# 	"sub",
# 	"xor",
# 	"mult",
# 	"a = 0",
# 	"b = 0",
# 	"a = ffffffff",
# 	"b = ffffffff",
# 	"a < 0",
# 	"b < 0",
# 	"a > 0",
# 	"b > 0",
# 	"ass < 0",
# 	"bs < 0",
# 	"ass > 0",
# 	"bs > 0",
# 	"unsigned overflow",
# 	"signed overflow",
# 	"negative sub result",
# 	"xor zero",
# 	"xor all ones",
# 	"zero mult result",
# 	"jump",
# 	"data bypass"
# )

def I():
	x = random.randint(0, 50)
	if x < 15:
		featureMap["add"] = True
		file2.write("005303b3\n")
		return "add"
	elif 15 <= x < 30:
		featureMap["sub"] = True
		file2.write("405303b3\n")
		return "sub"
	elif 30 <= x < 40:
		featureMap["xor"] = True
		file2.write("005343b3\n")
		return "xor"
	else:
		featureMap["mult"] = True
		file2.write("025303b3\n")
		return "mult"

def randomint(input):
	x = random.randint(0, 100)
	if x < 25:
		if input == 'a':
			featureMap["a = 0"] = True
		else:
			featureMap["b = 0"] = True
		return "0"
	elif 25 <= x < 50:
		if input == 'a':
			featureMap["a = ffffffff"] = True
			featureMap["a > 0"] = True
			featureMap["ass < 0"] = True
		else:
			featureMap["b = ffffffff"] = True
			featureMap["b > 0"] = True
			featureMap["bs < 0"] = True
		return "ffffffff"
	else:
		s = random.randint(0, 0xffffffff)
		featureMap["a > 0"] = True
		featureMap["b > 0"] = True
		if s & 0x80000000:
			if input == 'a':
				featureMap["ass < 0"] = True
			else:
				featureMap["bs < 0"] = True
		else:
			if input == 'a':
				featureMap["ass > 0"] = True 
			else:
				featureMap["bs > 0"] = True
		s = hex(s)
		return s[2:]

def feature_output(a, b):
	a = int(a, 16)
	b = int(b, 16)
	ass = (a ^ 0xffffffff) + 1
	bs = (b ^ 0xffffffff) + 1
	if featureMap["add"] == True: #add
		if a + b >= 2**32:
			featureMap["unsigned overflow"] = True #unsigned overflow
		if (ass > 0 and bs > 0 and ass + bs < 0) or (ass < 0 and bs < 0 and ass + bs > 0):
			featureMap["signed overflow"] = True #signed overflow
	elif featureMap["sub"] == True: #sub
		if b > a:
			featureMap["negative sub result"] = True #negative sub result
	elif featureMap["xor"] == True: #xor
		if a ^ b == 0:
			featureMap["xor zero"] = True #xor zero
		elif a ^ b == int("ffffffff", 16):
			featureMap["xor all ones"] = True #xor all ones
	else: #mult
		featureMap["zero mult result"] = featureMap["a = 0"] | featureMap["b = 0"] #zero mult result

for i in range(100):
	for key in featureList:
		featureMap[key] = False
	file.write("lw $t0, $0, 12\n")
	file2.write("00c02283\n")
	file.write("lw $t1, $0, 16\n")
	file2.write("01002303\n")
	file.write(I() + " $t2, $t0, $t1\n")
	#file.write("end:\n")
	a = randomint('a')
	file.write(a + "\n")
	file2.write(a + "\n")
	b = randomint('b')
	file.write(b + "\n")
	file2.write(b + "\n")
	feature_output(a, b)
	file3.write(','.join([('1' if featureMap[feature] else '0') for feature in featureList]) + '\n')

file.close()
file2.close()
file3.close()