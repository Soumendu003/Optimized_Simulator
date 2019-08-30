-- Code your design here
library IEEE;
use IEEE.std_logic_1164.all;

entity Module_test is
	port(
    	a: in std_logic;
        b: in std_logic;
        clk: in std_logic;
        q: inout std_logic;
        d: inout std_logic);
end Module_test;


architecture Behavioral of Module_test is


begin
process(clk,a,b)
    
begin
        
q <= d ;
d <= ( not a ) and ( not b ) ;
end process;
end Behavioral;
