import random
file = open("assembly.txt", "w")
file2 = open("hex.txt", "w")
file3 = open("features.txt", "w")

file3.write("add, sub, xor, mult, a = 0, b = 0, a = ffffffff, b = ffffffff, a < 0, b < 0, a > 0, b > 0, c = 0, c < 0, c > 0, unsigned overflow, signed overflow, negative sub result, xor zero, xor all ones, zero mult result, jump, data bypass\n")

feature_string = list('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n')

def I():
	x = random.randint(0, 50)
	if x < 15:
		feature_string[0] = 1
		file2.write("005303b3\n")
		return "add"
	elif 15 <= x < 30:
		feature_string[2] = 1
		file2.write("405303b3\n")
		return "sub"
	elif 30 <= x < 40:
		feature_string[4] = 1
		file2.write("005343b3\n")
		return "xor"
	else:
		feature_string[6] = 1
		file2.write("025303b3\n")
		return "mult"

def randomint(input):
	x = random.randint(0, 100)
	if x < 25:
		if input == 'a':
			feature_string[8] = 1
		else:
			feature_string[10] = 1
		return "0"
	elif 25 <= x < 50:
		if input == 'a':
			feature_string[12] = 1
			feature_string[16] = 1
		else:
			feature_string[14] = 1
			feature_string[18] = 1
		return "ffffffff"
	else:
		s = str(hex(random.randint(0, 4294967295)))
		if s[0] == "1":
			if input == 'a':
				feature_string[16] = 1
			else:
				feature_string[18] = 1
		else:
			if input == 'a':
				feature_string[20] = 1
			else:
				feature_string[22] = 1
		return s[2:]

def feature_output(fstr):
	if fstr[0] == 1: #add
		fstr[30] = 0 #unsigned overflow
		fstr[32] = 0 #signed overflow
	elif fstr[2] == 1: #sub
		fstr[34] = 0 #negative sub result
	elif fstr[4] == 1: #xor
		fstr[36] = 0 #xor zero
		fstr[38] = 0 #xor all ones
	else:
		fstr[40] = int(fstr[8]) | int(fstr[10]) #zero mult result

for i in range(100):
	feature_string = list('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n')
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
	feature_output(feature_string)
	file3.write(''.join(str(e) for e in feature_string))

file.close()
file2.close()
file3.close()