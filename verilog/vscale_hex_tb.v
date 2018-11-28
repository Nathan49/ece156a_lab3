`include "vscale_ctrl_constants.vh"
`include "vscale_csr_addr_map.vh"
`include "vscale_alu_ops.vh"

// define paths to common modules for testing
`define ALU         DUT.vscale.pipeline.alu
`define PC          DUT.vscale.pipeline.PC_IF
`define INSTR       DUT.vscale.pipeline.inst_DX
`define REGS        DUT.vscale.pipeline.regfile.data
`define OP          DUT.vscale.pipeline.ctrl.opcode
`define MUL_RES     DUT.vscale.pipeline.md.result
`define MUL_STATE   DUT.vscale.pipeline.md.state
`define PC_SRC      DUT.vscale.pipeline.PC_src_sel
`define PIPELINE    DUT.vscale.pipeline

module vscale_hex_tb();

    localparam hexfile_words = 8192;

    reg clk;
    reg reset;

    wire htif_pcr_resp_valid;
    wire [`HTIF_PCR_WIDTH-1:0] htif_pcr_resp_data;

    reg [255:0]                reason = 0;
    reg [1023:0]               loadmem = 0;
    reg [1023:0]               vpdfile = 0;
    reg [  63:0]               max_cycles = 64;
    reg [  63:0]               trace_count = 0;
    integer                    stderr = 32'h80000002;
    integer fid;

    reg [127:0]                hexfile [hexfile_words-1:0];

    reg stop = 0;

    vscale_sim_top DUT(
        .clk(clk),
        .reset(reset),
        .htif_pcr_req_valid(1'b1),
        .htif_pcr_req_ready(),
        .htif_pcr_req_rw(1'b0),
        .htif_pcr_req_addr(`CSR_ADDR_TO_HOST),
        .htif_pcr_req_data(`HTIF_PCR_WIDTH'b0),
        .htif_pcr_resp_valid(htif_pcr_resp_valid),
        .htif_pcr_resp_ready(1'b1),
        .htif_pcr_resp_data(htif_pcr_resp_data)
    );

    initial begin
        clk = 0;
        reset = 1;

        // open file for writing
        fid = $fopen("flags.txt", "w");
    end

    always begin
        #5 clk = !clk;
    end
    // always #5 clk = !clk;

    always @(posedge stop) begin
        $fclose(fid);
        $finish;
    end

    integer i = 0;
    integer j = 0;

    initial begin
        $display("starting");
        loadmem = "hexFiles/tests.hex";
        $readmemh(loadmem, DUT.hasti_mem.mem);

        // if (loadmem) begin
        //     $readmemh(loadmem, hexfile);
        //     for (i = 0; i < hexfile_words; i = i + 1) begin
        //         for (j = 0; j < 4; j = j + 1) begin
        //             DUT.hasti_mem.mem[4*i+j] = hexfile[i][32*j+:32];
        //         end
        //     end
        // end

        $display("Loaded Instructions:");
        for (i = 0; i < 32; i=i+ 1) begin
            $display("%d: %h", i, DUT.hasti_mem.mem[i]);
        end

        #100 reset = 0;

    end // initial begin

    always @(posedge clk) begin
        trace_count = trace_count + 1;

        // print out debug info
        $display("Cycle %d, PC: %h, Instr: %h",
            trace_count, `PC, `INSTR);

        // if (trace_count == 20) begin
        //     $display("Registers:");
        //     for (i = 0; i < 32; i=i+ 1) begin
        //         $display("%d: %h", i, `REGS[i]);
        //     end
        // end

        if (max_cycles > 0 && trace_count > max_cycles)
          reason = "timeout";

        if (!reset) begin
            if (htif_pcr_resp_valid && htif_pcr_resp_data != 0) begin
                if (htif_pcr_resp_data == 1) begin
                    stop = 1;
                    // $finish;
                end else begin

                end
            end
        end

        if (reason) begin
            $display("*** FAILED *** (%s) after %d simulation cycles", reason, trace_count);
            stop = 1;
            // $finish;
        end

        // ---------------        
        //  DO TESTS HERE
        // ---------------

        // Unsigned overflow
        if (
            `ALU.op == `ALU_OP_ADD &&
            !`ALU.out[31] && (`ALU.in1[31] || `ALU.in2[31])
        ) begin
            $display("Signed Overflow: %b + %b = %b",
                `ALU.in1[31],
                `ALU.in2[31],
                `ALU.out[31]);
            $fwrite(fid, "Signed Overflow\n");
        end



        // Signed overflow
        if (
            `ALU.op == `ALU_OP_ADD &&
            (
                `ALU.out[31] && !`ALU.in1[31] && !`ALU.in2[31] ||
                !`ALU.out[31] && `ALU.in1[31] && `ALU.in2[31]
            )
        ) begin
            $display("Unsigned Overflow: %b + %b = %b",
                `ALU.in1[31],
                `ALU.in2[31],
                `ALU.out[31]);
            $fwrite(fid, "Unsigned Overflow\n");
        end

        // Negative result from subtraction
        if (
            `ALU.op == `ALU_OP_SUB &&
            `ALU.out[31]
        ) begin
            $display("Negative Subtraction: %h - %h = %h",
                `ALU.in1,
                `ALU.in2,
                `ALU.out);
            $fwrite(fid, "Negative Subtraction\n");
        end

        // Zero Output with multiplication
        if (`MUL_STATE == 2 && `MUL_RES == 0) begin
            $display("Zero Multiplication: %h", `MUL_RES);
            $fwrite(fid, "Zero Mult\n");
        end

        // XOR zero result
        if (
            `ALU.op == `ALU_OP_XOR &&
            `ALU.out == 0
        ) begin
            $display("Zero XOR: %h ^ %h = %h",
                `ALU.in1,
                `ALU.in2,
                `ALU.out);
            $fwrite(fid, "Zero XOR\n");
        end

        // all ones XOR result
        if (
            `ALU.op == `ALU_OP_XOR &&
            `ALU.out == 32'hffffffff
        ) begin
            $display("Ones XOR: %h ^ %h = %h",
                `ALU.in1,
                `ALU.in2,
                `ALU.out);
            $fwrite(fid, "Ones XOR\n");
        end

        // a jump happened
        if (`PC_SRC == `PC_JAL_TARGET) begin
            $display("jumped");
            $fwrite(fid, "Jumped\n");
        end

        // Data Bypass
        if (`PIPELINE.bypass_rs1 || `PIPELINE.bypass_rs2) begin
            if (`PIPELINE.bypass_rs1) begin
                $display("RS1 Bypassed");
            end

            if (`PIPELINE.bypass_rs2) begin
                $display("RS2 Bypassed");
                $fwrite(fid, "Data Bypass\n");
            end
        end
    end

endmodule // vscale_hex_tb

