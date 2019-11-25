`define __QUARTUS__
`ifdef __QUARTUS__
    `define __IP_SPRAM__
`endif

module ram(
        input   wire            clk,
        input   wire            we,
        input   wire    [31:0]  addr,
        output  wire    [31:0]  data_read,
        input   wire    [31:0]  data_write
    );

    `ifndef __IP_SPRAM__
        reg [31:0] ram_block[255:0];
        
        assign data_read = ram_block[addr[7:0]];
        
        always @(posedge clk)
        begin
            if(we && (addr[31:8] == 24'h0))
                ram_block[addr[7:0]] <= data_write;
        end
    `else
        // use ip_spram
        ip_spram	u_ip_spram (
        .address    (   addr[7:0]       ),
        .clock      (   clk             ),
        .data       (   data_write      ),
        .wren       (   we              ),
        .q          (   data_read       )
        );
    `endif

endmodule // ram