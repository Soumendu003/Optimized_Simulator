import Macros as M
import numpy as np

'''OPCODES = {
    1: STORE,     # S1 <= S2                     (OP,S1,S2)
    2: AND_TEM,   # tem <= S1 and S2             (OP,S1,S2)
    3: OR_TEM,    # tem <= S1 or S2              (OP,S1,S2)
    4: NOT_TEM,   # tem <= not(S1)               (OP,S1)
    5: NOT,       # S1 <= not(S2)                (OP,S1,S2)
    6: DELAY_STORE_TEM, # S1 <= tem after t ns   (OP,S1,t)             // Here S1 is not original Signal index, But delayed index
    7: WAIT,        # wait for t ns              (OP,t)
    8: STORE_TEM,   # S1 <= tem                  (OP,S1)
    9: TEM_STORE,    # tem <= S1                 (OP,S1)
    10: TEM_AND,     # tem <= tem and S1         (OP,S1)
    11: TEM_OR,     # tem <= tem or S1           (OP,S1)
    12: TEM_NOT,     # tem <= not(tem)            (OP)
    13: REPORT,      # reports value of S1        (OP,S1)
}'''

class Kernel:

    def __init__(self):

        self.time = 0
        self.Signal = None
        self.Driver = None
        self.Signal_Update_Event = None
        self.Triggering_Process = None
        self.Instructions = None
        self.Signal_Triggered_Process = None
        self.Time_Triggered_Process = None
        self.Process_Trigger_Event = None
        self.Event_List = []
        self.Delayed_Assignment = None
        self.Tem = M.VALUE_Z
        self.Signal_to_Signal_Name = {}
        self.Value_Map = [ 'U', 'X', '0', '1', 'Z']
        
    def Initialize_Signal(self, Signals):

        assert (len(Signals) <= M.MAX_SIGNAL) , "Total number of Signal Exceeds "+str(M.MAX_SIGNAL)

        self.Signal = np.ndarray((len(Signals),),dtype=M.SIG_DATA_TYPE)

        self.Signal.fill((-1,-1,-1,-1,-1))
        
        i = 0
        for signal in Signals.values():

            signal.Hash_Val = i
            i+=1

    def Initialize_Signal_Update_Event(self, Signals):

        assert (len(Signals) <= M.MAX_SIGNAL) , "Total number of Signal Exceeds "+str(M.MAX_SIGNAL)

        self.Signal_Update_Event = np.ndarray((len(Signals)+1,),dtype='u1')
        self.Signal_Update_Event[0] = 0                         # By default head points to 0. Means Not event registered

    def Initialize_Driver(self, count):

        self.Driver = np.ndarray((count,),dtype='u1')
    
    def Initialize_Instructions(self, Size):

        self.Instructions = np.ndarray((Size,),dtype='u1')

    def Initialize_Signal_Triggered_Process(self, Size):

        self.Signal_Triggered_Process = np.ndarray((Size,),dtype=M.SIG_TRIGGERED_PROCESS_TYPE)

    def Initialize_Time_Triggered_Process(self, Size):

        self.Time_Triggered_Process = np.ndarray((Size,),dtype=M.TIME_TRIGGERED_PROCESS_TYPE)

    def Initialize_Triggering_Process(self, Size):

        self.Triggering_Process = np.ndarray((Size,),dtype='u1')

        self.Triggering_Process.fill(-1)
    
    def Initialize_Process_Trigger_Event(self, Size):

        self.Process_Trigger_Event = np.ndarray((Size+1,),dtype='u1')

        self.Process_Trigger_Event[0]=0                     # By default head points to 0. Means No Process Triggering Scheduled

    def Initialize_Delayed_Assignment(self, Size):

        self.Delayed_Assignment = np.ndarray((Size,),dtype=M.DELAYED_ASSIGNMENT_TYPE)
        self.Delayed_Assignment.fill((-1,-1,-1))


def Remove_Redundant_Signal_Assignments(Process_Set, Signals):

    for process in Process_Set:

        instructions=[]

        Sig_to_Ins={}

        flag = 0

        for ins in process.instructions:

            if(ins[0] == '<='):

                Sig_to_Ins.update({ins[1]:ins})

                hash_val=int(ins[1])

                Signals[hash_val].Driver.update({process:-1})

                flag = 1

            elif( ins[0] == 'report'):

                instructions.append(ins)

            elif(ins[0] == 'Delay'):

                instructions.append(ins)

                hash_val=int(ins[1])

                Signals[hash_val].Delay_Driver.append(process)

            elif(ins[0] == 'wait'):

                for Ins in Sig_to_Ins.values():

                    instructions.append(Ins)

                instructions.append(ins)
                Sig_to_Ins={}

                flag = 0

        if(flag == 1):

            for Ins in Sig_to_Ins.values():

                instructions.append(Ins)

        process.instructions=instructions


def Get_Operator(ele, operand):

    if ( ele == 'or' or ele == 'and' or ele == 'not'):

        return ele
    
    else:

        operand.append(ele)
        return 0


def Make_3_Adress(Sig, ins, Instructions, flag, delay_val=0, Delayed_Assignment_Collection=[]):

    if(flag == 1):

        Make_3_Adress(Sig, ins, Instructions, 0)

        last_instruction=Instructions.pop()

        #print("Last Instruction : "+str(last_instruction))

        if(last_instruction[0] == 1):

            Instructions.append([9,last_instruction[2]])
            Instructions.append([6,len(Delayed_Assignment_Collection), delay_val])
            Delayed_Assignment_Collection.append(last_instruction[1])
        
        elif(last_instruction[0] == 8):
            Instructions.append([6,len(Delayed_Assignment_Collection),delay_val])
            Delayed_Assignment_Collection.append(last_instruction[1])

        elif(last_instruction[0] == 5):

            Instructions.append(4,last_instruction[2])
            Instructions.append([6,len(Delayed_Assignment_Collection),delay_val])
            Delayed_Assignment_Collection.append(last_instruction[1])

        else:
            print("Invalid operand for delayed Assignment : "+str(last_instruction[0]))
            raise Exception()

    else:

        assert(len(ins) > 0)

        if(len(ins) == 1):

            Instructions.append([1,Sig,ins[0]])
            return
        
        if(len(ins) == 2):

            assert( 'not' in ins)

            Instructions.append([5,Sig,ins[0]])
            return
        
        flag = 0
        operand = []

        for ele in ins:

            operator = Get_Operator(ele,operand)

            if(operator != 0):

                if( operator == 'not'):

                    if( flag == 0 ):

                        Instructions.append([4,operand.pop()])
                        flag = 1

                    else:

                        Instructions.append([12])
                
                elif( operator == 'and' ):
                    
                    if( flag == 0 ):

                        Instructions.append([2,operand.pop(),operand.pop()])
                        flag = 1

                    else:

                        Instructions.append([10,operand.pop()])
                
                elif( operator == 'or' ):
                    
                    if( flag == 0 ):

                        Instructions.append([3,operand.pop(),operand.pop()])
                        flag = 1

                    else:

                        Instructions.append([11,operand.pop()])

        Instructions.append([8,Sig])
        return

                 

def Generate_Three_Address_Code(Process_Set, Delayed_Assignment_Collection):

    for process in Process_Set:

        Instructions=[]

        for ins in process.instructions:

            if(len(ins)>2):

                if(ins[0] == 'Delay'):
                    Make_3_Adress(ins[1],ins[2],Instructions,1,ins[3],Delayed_Assignment_Collection)
                else:
                    Make_3_Adress(ins[1],ins[2],Instructions,0)

            elif(len(ins) == 2):

                if(ins[0] == 'wait'):

                    Instructions.append([7,ins[1]])
                
                elif(ins[0] == 'report'):

                    Instructions.append([13,ins[1]])

        process.instructions=Instructions


def Initialize_Driver_Array(kernel, Signals):

    count = 0

    for signal in Signals.values():

        count+=len(signal.Driver)
        count+=len(signal.Delay_Driver)

    assert ( count <= M.MAX_DRIVER_SIZE) , "Total number of Driver exceeds "+str(M.MAX_DRIVER_SIZE)

    kernel.Initialize_Driver(count)

    index = 0
    for signal in Signals.values():

        signal.Driving_Head = index

        count = 0

        count+=len(signal.Driver)
        count+=len(signal.Delay_Driver)

        assert ( count <= M.MAX_SIGNAL_DRIVER) , "Maximum limit of Driver exceeded for a Signal : "+str(signal.name)

        index+=count
        signal.Driving_Count = count


def Initialize_Processes_And_Instructions(kernel, Process_Set):

    Signal_Triggered = []
    Time_Triggered = []
    Total_Instruction_Word = 0

    assert (len(Process_Set) <= M.MAX_PROCESS ) , "Total Number of Process exceeds "+str(M.MAX_PROCESS)

    for process in Process_Set:

        if(process.Id[0] == 'X'):

            process.Hash_Val = len(Signal_Triggered)

            Signal_Triggered.append(process)
        
        else:

            Time_Triggered.append(process)
        
        process.Instruction_Start = Total_Instruction_Word
        for ins in process.instructions:

            Total_Instruction_Word += len(ins)

        process.Instruction_End = Total_Instruction_Word - 1 

    assert ( Total_Instruction_Word <= M.MAX_INSTRUCTION_WORD) , "Maximum Allowed Instruction Word Exceeded . Limit = "+str(M.MAX_INSTRUCTION_WORD)
    
    kernel.Initialize_Instructions(Total_Instruction_Word)

    kernel.Initialize_Signal_Triggered_Process(len(Signal_Triggered))

    kernel.Initialize_Process_Trigger_Event(len(Signal_Triggered))

    kernel.Initialize_Time_Triggered_Process(len(Time_Triggered))


def Fill_Up_Processes(kernel, Process_Set):

    time_triggered = 0
    for process in Process_Set:

        if(process.Hash_Val < 0):

            kernel.Time_Triggered_Process[time_triggered][0] = process.Instruction_Start
            kernel.Time_Triggered_Process[time_triggered][1] = process.Instruction_End
            kernel.Time_Triggered_Process[time_triggered][2] = process.Instruction_Start

            time_triggered += 1
        
        else:

            kernel.Signal_Triggered_Process[process.Hash_Val][0] = process.Instruction_Start
            kernel.Signal_Triggered_Process[process.Hash_Val][1] = process.Instruction_End
            kernel.Signal_Triggered_Process[process.Hash_Val][2] = process.Instruction_Start
            kernel.Signal_Triggered_Process[process.Hash_Val][3] = 0
            

def Initialize_And_Fill_Up_Triggering_Process(kernel, Signals):

    Total_Count = 0

    for signal in Signals.values():

        if(len(signal.processes) > 0):

            signal.Triggering_Process_Start = Total_Count
            Total_Count += len(signal.processes)
    
    assert ( Total_Count <= M.MAX_TRIGGERING_PROCESS) , "Total Triggering Process Exceeds "+str(M.MAX_TRIGGERING_PROCESS)

    kernel.Initialize_Triggering_Process(Total_Count)

    for signal in Signals.values():

        for i in range(0,len(signal.processes)):

            kernel.Triggering_Process[signal.Triggering_Process_Start + i] = signal.processes[i][1].Hash_Val
    

def Fill_Up_Signals(kernel, Signals):

    for signal in Signals.values():

        kernel.Signal[signal.Hash_Val][0] = M.VALUE_Z
        kernel.Signal[signal.Hash_Val][1] = signal.Driving_Head
        kernel.Signal[signal.Hash_Val][2] = 0                                # Initially Number of Driving values = 0
        
        if(signal.Triggering_Process_Start < 0):
            kernel.Signal[signal.Hash_Val][3] = M.NON_TRIGGERING
        else:
            kernel.Signal[signal.Hash_Val][3] = signal.Triggering_Process_Start
        
        kernel.Signal[signal.Hash_Val][4] = len(signal.processes)              


def Resolve_And_Fill_Up_Instruction(kernel, Signals, Process_Set):

    for process in Process_Set:

        for ins in process.instructions:

            if( ins[0] != 6 and ins[0] != 7 and ins[0] != 12 ):

                for i in range(1,len(ins)):

                    if('Val' in ins[i]):

                        if( '1' in ins[i]):
                            ins[i] = M.VALUE_1
                        elif('0' in ins[i]):
                            ins[i] = M.VALUE_0
                        elif('U' in ins[i]):
                            ins[i] = M.VALUE_U
                        elif('X' in ins[i]):
                            ins[i] = M.VALUE_X
                        else:
                            raise Exception("Unknown Std_Value other than 1,0,X,U given by input")

                    else:

                        hash_val = int(ins[i]) 
                        ins[i] = Signals[hash_val].Hash_Val

                        if(ins[0] == 13):                     # 'report' Command . only Stores the required signal names in Dict

                            kernel.Signal_to_Signal_Name.update({Signals[hash_val].Hash_Val : Signals[hash_val].name})



    for process in Process_Set:

        index = 0
        for ins in process.instructions:

            for word in ins:

                kernel.Instructions[process.Instruction_Start+index] = word
                index += 1                     
    

def Initialize_And_Fill_Up_Delayed_Assignment(kernel, Signals, Delayed_Assignment_Collection):

    assert ( len(Delayed_Assignment_Collection) <= M.MAX_DELAYED_ASSIGNMENTS) , "Total Number of Delayed Assignments exceeds "+str(M.MAX_DELAYED_ASSIGNMENTS)
    
    kernel.Initialize_Delayed_Assignment(len(Delayed_Assignment_Collection))
    
    for i in range(0, len(Delayed_Assignment_Collection)):

        sig_index = Signals[int(Delayed_Assignment_Collection[i])].Hash_Val

        kernel.Delayed_Assignment[i][1] = sig_index
        kernel.Delayed_Assignment[i][2] = M.VALUE_Z


def Initialize_Event_List(kernel):

    kernel.Event_List.append([kernel.time])

    for i in range(0, kernel.Time_Triggered_Process.shape[0]):

        kernel.Event_List[0].append(kernel.Time_Triggered_Process[i])

    for i in range(0,kernel.Delayed_Assignment.shape[0]):

        kernel.Event_List[0].append(kernel.Delayed_Assignment[i])


def Optimizer(Entities, Signals, Process_Set):

    Remove_Redundant_Signal_Assignments(Process_Set, Signals)


    Delayed_Assignment_Collection = []                                    # Keeps record of Delayed Assignments
    Generate_Three_Address_Code(Process_Set, Delayed_Assignment_Collection)

    kernel = Kernel()

    kernel.Initialize_Signal(Signals)
    kernel.Initialize_Signal_Update_Event(Signals)

    Initialize_Driver_Array(kernel, Signals)

    Initialize_Processes_And_Instructions(kernel, Process_Set)

    Fill_Up_Processes(kernel, Process_Set)

    Initialize_And_Fill_Up_Triggering_Process(kernel, Signals)

    Fill_Up_Signals(kernel, Signals)

    Resolve_And_Fill_Up_Instruction(kernel, Signals, Process_Set)

    Initialize_And_Fill_Up_Delayed_Assignment(kernel, Signals, Delayed_Assignment_Collection)

    Initialize_Event_List(kernel)

    return kernel
