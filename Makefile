sim: a.out
	vvp a.out

a.out: verilog/vscale_hex_tb.v
	iverilog ./verilog/*.v -I verilog/

runSim:
	python3 run/run.py

learns:
	python3 learn/learn.py

everything:
	make generate
	make runSim
	make learns

# writes genertor/features.txt
#                /hex.txt
generate:
	python3 generator/generate.py

compile:
	python3 compiler/riscCompile.py compiler/test.s compiler/out.hex

clean:
	rm -f a.out generator/features.csv generator/hex.txt
	rm -rf __pycache__ compiler/__pycache__