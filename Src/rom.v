`define __QUARTUS__
`ifdef __QUARTUS__
    `define __IP_SPROM__
`endif

module rom(
        input   wire            clk,
        input   wire            aclr,
        output  wire    [31:0]  dout,
        input   wire    [10:0]  addr
    );

    // use 256 words rom
    
    `ifndef __IP_SPROM__
        reg [31:0] rom_block [255:0];
        
        reg [10:0] q_addr=11'h0;
        
        always@(posedge clk or posedge aclr)
        begin
            if(aclr)
                q_addr <= 11'h0;
            else
                q_addr <= addr;
        end

        assign dout = rom_block[q_addr[9:2]];
    `else
        // use ip_sprom
        ip_sprom u_ip_sprom (
            .aclr       ( aclr      ),
            .address    ( addr[9:2] ),
            .clock      ( clk       ),
            .q          ( dout      )
        );
    `endif
    
endmodule // rom