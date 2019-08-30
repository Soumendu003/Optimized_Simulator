-- Code your testbench here
library IEEE;
use IEEE.std_logic_1164.all;

entity Simple_Gate_Flop is
    port(
        a: in std_logic;
        b: in std_logic;
        o: in std_logic);
end Simple_Gate_Flop;


architecture Behavioral of Simple_Gate_Flop is

signal d: std_logic ;

begin

    process(a,b)

    begin

        d <= a and b ;
    
    end process;

    process

    begin

        o <= d ;
    
    end process;

    process(o)
    begin

        report "Value of o is "&std_logic'image(o) ;
    
    end process ;
    
end Behavioral;