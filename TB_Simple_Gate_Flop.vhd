library IEEE;
use IEEE.std_logic_1164.all;


entity testbench is
-- empty
end testbench; 

architecture tb of testbench is

component Simple_Gate_Flop is
    port(
        a: in std_logic;
        b: in std_logic;
        o: in std_logic);
end component;

signal a_in: std_logic ;
signal b_in: std_logic ;
signal o_out: std_logic ;

begin

    uut: Simple_Gate_Flop port map(a_in,b_in,o_out);

    process

    begin

        a_in <= '0' ;
        b_in <= '0' ;

        wait for 2 ns;

        a_in <= '1' ;
        b_in <= '0' ;

        wait for 2 ns;

        a_in <= '0' ;
        b_in <= '1' ;

        wait for 2 ns;

        a_in <= '1' ;
        b_in <= '1' ;

        wait for 2 ns;
    
    end process;

end tb;


