`timescale 1ns/100ps

//`define __QUARTUS__
`ifndef __QUARTUS__
    `include "./Src/top.v"
`endif

module top_tb;

    reg clk = 0;
    reg reset_n = 1;

    /*  Instance  */
    top u_top(clk,reset_n);

    always
        #10 clk=~clk;

    integer i;
    initial
    begin
        $dumpfile("top.vcd");
        $dumpvars(0,top_tb);

        // load file
        $readmemb("../Sim/rom_test.dat",u_top.u_rom.rom_block);

        #20 reset_n = 0;
        #20 reset_n = 1;

        #200 $finish;
    end
endmodule