lw $t0, $0, 20
lw $t1, $0, 24
add $t2, $t0, $t1
jal $0, next
next:
add $t2, $t0, $t1
add $t2, $t2, $t2
sub $t2, $t0, $t1
xor $t2, $t0, $t1
mul $t2, $t0, $t1