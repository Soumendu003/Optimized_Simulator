-- Code your testbench here
library IEEE;
use IEEE.std_logic_1164.all;


entity testbench is
-- empty
end testbench; 


architecture tb of testbench is

-- DUT component


signal d: std_logic ;



begin
    
  	process
    begin
    
    	d <= '1' ;
        
        wait for 3 ns;
        
    end process;
    
    process
    begin
    	
        d <= '0' ;
        wait for 2 ns ;
    end process;
        
       
end tb;