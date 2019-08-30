library IEEE;
use IEEE.std_logic_1164.all;


entity testbench is
-- empty
end testbench; 

architecture tb of testbench is

    -- DUT component
  
signal a: std_logic ;
signal b: std_logic ;   
signal c: std_logic ;
signal d: std_logic ;
    
begin

    process(a)
    begin

        b <= a ;
        c <= b ;
        d <= c ;
        report "Value of a is "&std_logic'image(a) ;
        

    end process;

    process
    begin


        a <= '1' ;

        wait for 2 ns ;

        a <= '0' ;

        wait for 2 ns ;

        a <= '1' ;

        wait for 2 ns ;

        a <= '0' ;

        wait for 2 ns ;


    
    end process;


 end tb;
        