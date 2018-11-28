all:
	iverilog ./verilog/*.v -I ./verilog/
	vvp a.out

clean:
	rm -f a.out
	rm -rf __pycache__ compiler/__pycache__