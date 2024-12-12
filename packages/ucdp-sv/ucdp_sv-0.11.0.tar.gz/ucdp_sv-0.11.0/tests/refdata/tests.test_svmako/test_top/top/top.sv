// =============================================================================
//
// THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
//
//  MIT License
//
//  Copyright (c) 2024 nbiotcloud
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
// =============================================================================
//
// Module:     top.top
// Data Model: top.top.TopMod
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module top #( // top.top.TopMod
  parameter integer               param_p   = 10,
  parameter integer               width_p   = $clog2(param_p + 1),
  parameter logic   [param_p-1:0] default_p = {param_p {1'b0}}
) (
  // main_i
  input  wire                main_clk_i,
  input  wire                main_rst_an_i, // Async Reset (Low-Active)
  // intf_i: RX/TX
  output logic               intf_rx_o,
  input  wire                intf_tx_i,
  // bus_i
  input  wire  [1:0]         bus_trans_i,
  input  wire  [31:0]        bus_addr_i,
  input  wire                bus_write_i,
  input  wire  [31:0]        bus_wdata_i,
  output logic               bus_ready_o,
  output logic               bus_resp_o,
  output logic [31:0]        bus_rdata_o,
  `ifdef ASIC
  output logic [8:0]         brick_o,
  `endif // ASIC
  input  wire  [param_p-1:0] data_i,
  output logic [width_p-1:0] cnt_o,
  // key_i
  input  wire                key_valid_i,
  output logic               key_accept_o,
  input  wire  [8:0]         key_data_i,
  inout  wire  [3:0]         bidir_io
  `ifdef ASIC
  ,
  output logic [8:0]         value_o
  `endif // ASIC
);



  // ------------------------------------------------------
  //  Local Parameter
  // ------------------------------------------------------
  localparam logic [param_p-1:0] const_c = default_p / 'd2;


  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  // key_s
  logic               key_valid_s;
  logic               key_accept_s;
  logic [8:0]         key_data_s;
  logic [3:0]         bidir_s;
  logic               clk_s;
  logic [7:0]         array_s       [0:param_p-1];
  logic [8:0]         data_r;
  logic [param_p-1:0] data2_r;


  // ------------------------------------------------------
  //  glbl.clk_gate: u_clk_gate
  // ------------------------------------------------------
  clk_gate u_clk_gate (
    .clk_i(main_clk_i),
    .clk_o(clk_s     ),
    .ena_i(1'b0      )  // TODO
  );


  // ------------------------------------------------------
  //  top.top_core: u_core
  // ------------------------------------------------------
  top_core #(
    .param_p(10            ),
    .width_p($clog2(10 + 1))
  ) u_core (
    // main_i
    .main_clk_i   (clk_s             ),
    .main_rst_an_i(main_rst_an_i     ), // Async Reset (Low-Active)
    .p_i          ({10 {1'b0}}       ), // TODO
    .p_o          (                  ), // TODO
    .data_i       ({8 {1'b0}}        ), // TODO
    .data_o       (                  ), // TODO
    `ifdef ASIC
    .brick_o      (brick_o           ),
    `endif // ASIC
    .some_i       (3'h4              ),
    .bits_i       (data_i[3:2]       ),
    // key_i
    .key_valid_i  (1'b0              ), // TODO
    .key_accept_o (                  ), // TODO
    .key_data_i   (9'h000            ), // TODO
    .open_rail_i  (                  ), // RAIL - TODO
    .open_string_i(""                ), // TODO
    .open_array_i ('{4{6'h00}}       ), // TODO
    .open_matrix_i('{2{'{10{6'h00}}}}), // TODO
    .matrix_down_i('{2{'{10{6'h00}}}}), // TODO
    .open_rail_o  (                  ), // RAIL - TODO
    .open_string_o(                  ), // TODO
    .open_array_o (                  ), // TODO
    .open_matrix_o(                  ), // TODO
    .note_i       (7'h00             ), // TODO
    .nosuffix0    (7'h00             ), // I - TODO
    .nosuffix1    (                  ), // O - TODO
    .array_i      (array_s           ),
    .array_open_i ('{8{8'h00}}       ), // TODO
    // intf_i: RX/TX
    .intf_rx_o    (intf_rx_o         ),
    .intf_tx_i    (intf_tx_i         )
  );


  // ------------------------------------------------------
  //  glbl.sync: u_sync
  // ------------------------------------------------------
  sync u_sync (
    // main_i
    .main_clk_i   (main_clk_i   ),
    .main_rst_an_i(main_rst_an_i), // Async Reset (Low-Active)
    .data_i       (1'b0         ), // TODO
    .data_o       (             )  // TODO
  );


  // ------------------------------------------------------
  //  Flip-Flops
  // ------------------------------------------------------

  always_ff @(posedge main_clk_i or negedge main_rst_an_i) begin: proc_seq_0
    if (main_rst_an_i == 1'b0) begin
      data_r  <=  9'h000;
      data2_r <=  {param_p {1'b0}};
    end else begin
      data_r  <=  key_data_s;
      data2_r <=  data_i;
    end
  end

  // ------------------------------------------------------
  //  Assigns
  // ------------------------------------------------------
  `ifdef ASIC
  assign value_o      = key_data_s;
  `endif // ASIC
  // key_s
  assign key_valid_s  = key_valid_i;
  assign key_accept_o = key_accept_s;
  assign key_data_s   = key_data_i;

endmodule // top

`default_nettype wire
`end_keywords
// =============================================================================
//
// THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
