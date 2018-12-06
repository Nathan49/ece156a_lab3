sim:
	iverilog ./verilog/*.v -I verilog/
	vvp a.out

runSim:
	python3 run/run.py

learns:
	python3 learn/learn.py

# writes genertor/features.txt
#                /hex.txt
generate:
	python3 generator/assemblyassembler.py

clean:
	rm -f a.out generator/features.csv generator/hex.txt
	rm -rf __pycache__ compiler/__pycache__