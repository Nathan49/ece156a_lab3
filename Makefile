all:
	iverilog ./verilog/* -I ./verilog/
	vvp a.out

clean:
	rm -f a.out