import Macros as M
import Operations as OP


def Execute_Instruction(process,kernel):


    return OP.OPCODES.get(kernel.Instructions[process['Current_Instruction_Index']])(process,kernel)
    


def Execute_Process(process, kernel):                      

    suspend = 0                                        # if 1, then process should be suspended

    if(process['Current_Instruction_Index'] >= process['Instruction_End_Index']):        #Exceded own region

        process['Current_Instruction_Index'] = process['Instruction_Start_Index']        # resets

    while(not(bool(suspend))):

        if(process['Current_Instruction_Index'] >= process['Instruction_End_Index']):        

            process['Current_Instruction_Index'] = process['Instruction_Start_Index']

            suspend = 1

            if(len(process) == 3):                                     # Time Sensitive Process

                OP.Schedule_Time_Event(process,0,kernel)                  # Schedules process event in the next timestrap

        else:

            suspend = Execute_Instruction(process,kernel)              # Executes the Instruction pointed by  process['Current_Instruction_Index']


        
def Resolve_Signal(Sig_Index, kernel):          #(Make sure you put driving count = 0 after resolving values)

    final_val = M.VALUE_Z
    for i in range(0,kernel.Signal[Sig_Index]['Driving_Count']):

        final_val = OP.Resolve_Value(final_val, kernel.Driver[kernel.Signal[Sig_Index]['Driver_Head'] + i])
    
    if(final_val != kernel.Signal[Sig_Index]['Eff_Val']):

        kernel.Signal[Sig_Index]['Eff_Val'] = final_val

        OP.Trigger_Sensitive_Processes(Sig_Index,kernel)

    kernel.Signal[Sig_Index]['Driving_Count'] = 0



def Execute_Time_Events(kernel):

    for ele in kernel.Event_List[0][1:]:

        if( ele[0] < 0):                                 # Delayed Signal

            OP.Insert_Driving_Value(ele[1],ele[2],kernel)                 # ele[1] = Sig_Index , ele[2] = Value
        
        else:

            Execute_Process(ele, kernel)                                  # process and kernel sent

    kernel.Event_List.pop(0)                                              # Removes already happed time events

    for i in range(1,kernel.Signal_Update_Event[0]+1):

        Resolve_Signal(kernel.Signal_Update_Event[i], kernel)            # Signal_index and kernel sent

    
    kernel.Signal_Update_Event[0] = 0                                    # Resets the Signal Update Head

    while(bool(kernel.Process_Trigger_Event[0])):             # if Some process trigering is registered, then entered in while

        for i in range(1,kernel.Process_Trigger_Event[0]+1):

            Execute_Process(kernel.Signal_Triggered_Process[kernel.Process_Trigger_Event[i]], kernel)
            kernel.Signal_Triggered_Process[kernel.Process_Trigger_Event[i]]['Triggered_Bit'] = 0         # Resets. Now it can again be registered for Trigering

        kernel.Process_Trigger_Event[0] = 0                             # Resets the Process Trigger Head

        for i in range(1,kernel.Signal_Update_Event[0]+1):
            
            Resolve_Signal(kernel.Signal_Update_Event[i], kernel)            # Signal_index and kernel sent
            
        kernel.Signal_Update_Event[0] = 0                                    # Resets the Signal Update Head



def Simulation(kernel,Max_Time):

    

    while( kernel.time <= Max_Time):

        Execute_Time_Events(kernel)
        
        kernel.time = kernel.Event_List[0][0]                            # Ensure that the already occured Events are removed