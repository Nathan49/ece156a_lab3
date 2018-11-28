# trigger signed and unsigned overflow and data bypass
addi $t1, $0, -1	# reg[6] = ffffffff
ori $t0, $0, 1  	# reg[5] = 00000001
add $t0, $t0, $t1

# trigger only signed overflow (add two positives and get a negative)
addi $t1, $0, -1
addi $t0, $0, 1
srl $t1, $t1, $t0
ori $t0, $0, 1
add $t0, $t0, $t1

# trigger negative sub
ori $t0, $0, 5
ori $t1, $0, 7
sub $t3, $t0, $t1

# trigger zero multiply
ori $t0, $0, 10
mul $t0, $t0, $0

# xor
lui $t0, 0xfffff
ori $t0, $t0, 0xfff
xor $t1, $t0, $t0 # all zeros
xor $t1, $t0, $0 # all ones

# jump
jal $0, next
add $t0, $t0, $t0 # skipped
add $t0, $t0, $t0 # skipped
add $t0, $t0, $t0 # skipped
next:
jal $0 next