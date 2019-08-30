'''
Date : 9th July, 2019

This is a simple Python VHDL Simiulator

only one Entity is allowed per file

only one architecture allowed per entity

Process Naming is not allowed

No spaces allowed in Sensitivity list of a Process

conditional statmements are not allowed in process

only '<=' ,'after' and 'wait' is allowed in Instructions

Evaluation Statements should be space separated

If you put 'not' , then keep the clause in a parenthesis

Using variables are not allowed

Simple wait for is allowed

Wait for 0 ns is not allowed

Delayed Assignment is allowed

Maximum Number of Signal Supported is 251

Values of Std_Logic supported is 'U','X','0','1','Z'

only simple report statements are allowed . e.g report "Value of a is "&std_logic'image(a) ;

'''

import sys
import Parser as P
import Optimizer as OP
import Simulation as Sim

def main(argv):

    Tb_no=int(argv[1])

    File_names=[]

    for i in range(0,Tb_no):
        File_names.append(argv[2+i])

    try: 
        Entities,Signals,Process_Set=P.Parser(File_names)
    
    except Exception as e:

        print("\n\nFrom Main Failed : "+str(e)+"\n\n")

    try:
        kernel = OP.Optimizer(Entities,Signals,Process_Set)

    except Exception as e:

        print("\n\nFrom Main Failed : "+str(e)+"\n\n")

    Max_Time=int(argv[2+Tb_no])

    try:
        Sim.Simulation(kernel,Max_Time)

    except Exception as e:

        print("\n\nFrom Main Failed : "+str(e)+"\n\n")
   



if __name__ == '__main__':
    main(sys.argv)
