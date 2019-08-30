-- Code your testbench here
library IEEE;
use IEEE.std_logic_1164.all;


entity testbench is
-- empty
end testbench; 


architecture tb of testbench is

-- DUT component
component Module_test is
	port(
    	a: in std_logic;
        b: in std_logic;
        clk: in std_logic;
        d: out std_logic);
end component;

signal d: std_logic ;
signal a_in: std_logic ;
signal b_in: std_logic ;
signal clk_in: std_logic ;
signal d_in: std_logic ;


begin
uut: Module_test port map(a_in,b_in,clk_in,d_in);
    
process
begin
    
a_in <= '1' ;
d <= '1' after 3 ns ;
        
wait for 3 ns;
        
end process;
    
process
begin
        
d <= '0' ;
wait for 2 ns ;
end process;       
end tb;