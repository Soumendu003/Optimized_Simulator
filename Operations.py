import Macros as M


LOOK_UP_TABLE = [
    [M.VALUE_U, M.VALUE_X, M.VALUE_0, M.VALUE_1, M.VALUE_U],
    [M.VALUE_U, M.VALUE_X, M.VALUE_X, M.VALUE_X, M.VALUE_X],
    [M.VALUE_U, M.VALUE_X, M.VALUE_0, M.VALUE_X, M.VALUE_0],
    [M.VALUE_U, M.VALUE_X, M.VALUE_X, M.VALUE_1, M.VALUE_1],
    [M.VALUE_U, M.VALUE_X, M.VALUE_0, M.VALUE_1, M.VALUE_Z]
]

#INDEX_TABLE = {M.VALUE_U : 0, M.VALUE_X : 1, M.VALUE_0 : 2, M.VALUE_1 : 3, M.VALUE_Z : 4}


def AND_OPERATION(a,b):

    if(a == M.VALUE_U and b == M.VALUE_U):

        return M.VALUE_X

    elif(a == M.VALUE_0 or b == M.VALUE_0):

        return M.VALUE_0
    
    elif(a == M.VALUE_X or b == M.VALUE_X):

        return M.VALUE_X
    
    else:

        return M.VALUE_1

def OR_OPERATION(a,b):

    if(a == M.VALUE_1 or b == M.VALUE_1):

        return M.VALUE_1
    
    elif(a == M.VALUE_X or b == M.VALUE_X):

        return M.VALUE_X
    
    elif( a == M.VALUE_U and b == M.VALUE_U):

        return M.VALUE_X
    
    else:

        return M.VALUE_0

def NOT_OPERATION(a):

    if(a == M.VALUE_U or a == M.VALUE_X):

        return M.VALUE_X
    
    elif(a == M.VALUE_0):

        return M.VALUE_1

    elif(a == M.VALUE_1):

        return M.VALUE_0

    else:

        return a

def Resolve_Value(a,b):

    return LOOK_UP_TABLE[a - M.VALUE_U][b - M.VALUE_U]

def Insert_Driving_Value(Sig_Index,Value,kernel):

    if(not(bool(kernel.Signal[Sig_Index]['Driving_Count']))):              # Nobody registered for some value change

        kernel.Signal_Update_Event[0] += 1
        kernel.Signal_Update_Event[kernel.Signal_Update_Event[0]] = Sig_Index               # stores the Signal Index

    kernel.Driver[kernel.Signal[Sig_Index]['Driver_Head'] + kernel.Signal[Sig_Index]['Driving_Count']] = Value   # Stores Value 
    kernel.Signal[Sig_Index]['Driving_Count'] += 1


def Get_Signal_Value(Sig,kernel):

    if( Sig >= M.VALUE_U):                                # Std Value

        return Sig

    else:

        return kernel.Signal[Sig]['Eff_Val']             # Returns current Effective Value 


def Schedule_Time_Event(ele,delay,kernel):

    count = 0
    flag = 0

    for event in kernel.Event_List:

        if(event[0] == kernel.time + delay + 1):
            event.append(ele)
            flag = 1
            break

        elif(event[0] > kernel.time + delay + 1):

            kernel.Event_List.insert(count, [kernel.time+delay+1, ele])
            flag = 1
            break
        
        count += 1

    if(flag == 0):

        kernel.Event_List.append([kernel.time+delay+1, ele])

def Trigger_Sensitive_Processes(Sig_Index,kernel):

    if(bool(kernel.Signal[Sig_Index]['Triggered_Process_Count'])):

        for i in range(0,kernel.Signal[Sig_Index]['Triggered_Process_Count']):

            pro_id = kernel.Triggering_Process[kernel.Signal[Sig_Index]['Triggered_Process_Start'] + i]

            if(not(bool(kernel.Signal_Triggered_Process[pro_id]['Triggered_Bit']))):         # Need to be registered

                  kernel.Signal_Triggered_Process[pro_id]['Triggered_Bit'] = 1
                  kernel.Process_Trigger_Event[0] += 1
                  kernel.Process_Trigger_Event[kernel.Process_Trigger_Event[0]] = pro_id 


def STORE(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #S2 = kernel.Instructions[process['Current_Instruction_Index'] + 2]

    #Value = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel)

    Insert_Driving_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel), kernel)

    process['Current_Instruction_Index'] += 3
    return 0


def AND_TEM(process,kernel):

    #S1 = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)
    #S2 = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel)

    kernel.Tem = AND_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel), Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel))

    process['Current_Instruction_Index'] += 3
    return 0

def OR_TEM(process,kernel):

    #S1 = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)
    #S2 = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel)

    kernel.Tem = OR_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel), Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel))

    process['Current_Instruction_Index'] += 3
    return 0


def NOT_TEM(process,kernel):

    #S1 = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)

    kernel.Tem = NOT_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel))

    process['Current_Instruction_Index'] += 2
    return 0
    
def NOT(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #S2 = kernel.Instructions[process['Current_Instruction_Index'] + 2]

    #Value = NOT_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel))

    Insert_Driving_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], NOT_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 2], kernel)), kernel)

    process['Current_Instruction_Index'] += 3
    return 0

def DELAY_STORE_TEM(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]           *Delayed Asiignment Index
    #t = kernel.Instructions[process['Current_Instruction_Index'] + 2]

    #ele = kernel.Delayed_Assignment[kernel.Instructions[process['Current_Instruction_Index'] + 1]]
    
    kernel.Delayed_Assignment[kernel.Instructions[process['Current_Instruction_Index'] + 1]][2] = kernel.Tem

    Schedule_Time_Event(kernel.Delayed_Assignment[kernel.Instructions[process['Current_Instruction_Index'] + 1]], kernel.Instructions[process['Current_Instruction_Index'] + 2],kernel)

    process['Current_Instruction_Index'] += 3
    return 0

def WAIT(process,kernel):

    #t = kernel.Instructions[process['Current_Instruction_Index'] + 1]

    Schedule_Time_Event(process, kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)
    process['Current_Instruction_Index'] += 2
    return 1                                     # Suspention msg returned

def STORE_TEM(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]

    Insert_Driving_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel.Tem, kernel)
    process['Current_Instruction_Index'] += 2
    return 0

def TEM_STORE(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #Value = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)

    kernel.Tem = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)
    process['Current_Instruction_Index'] += 2
    return 0

def TEM_AND(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #Value = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)

    kernel.Tem = AND_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel), kernel.Tem)
    process['Current_Instruction_Index'] += 2
    return 0

def TEM_OR(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #Value = Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel)

    kernel.Tem = OR_OPERATION(Get_Signal_Value(kernel.Instructions[process['Current_Instruction_Index'] + 1], kernel), kernel.Tem)
    process['Current_Instruction_Index'] += 2
    return 0

def TEM_NOT(process,kernel):

    kernel.Tem = NOT_OPERATION(kernel.Tem)
    process['Current_Instruction_Index'] += 1
    return 0

def REPORT(process,kernel):

    #S1 = kernel.Instructions[process['Current_Instruction_Index'] + 1]
    #Value = kernel.Signal[kernel.Instructions[process['Current_Instruction_Index'] + 1]]['Eff_Val']

    print("Value of "+kernel.Signal_to_Signal_Name[kernel.Instructions[process['Current_Instruction_Index'] + 1]]+" = "+kernel.Value_Map[kernel.Signal[kernel.Instructions[process['Current_Instruction_Index'] + 1]]['Eff_Val'] - M.VALUE_U])
    print("Time = "+str(kernel.time))

    process['Current_Instruction_Index'] += 2
    return 0


OPCODES = {
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
    13: REPORT      # reports value of S1        (OP,S1)
}