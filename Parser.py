'''  This Module basically parse the VHDL source codes and
creates the data structures for further  evaluation     '''
import Datastructures as D

# Parses the Entities and Create Signal objects for each port of the Entity 
def ParseEntities(file, Signals, Entities):

    f = open(file,"r")

    lines = f.readlines()


    state = 0               

    for line in lines:

        words = line.split()                           # Splits each line based on space separator

        if(len(words) > 0 and state == 0 and words[0] == 'entity'):

            state = 1

            entity = D.Entity(words[1])                # Creates Entity Object
            Entities.update({words[1]:entity})         # Stores in Dictionary
            
        if(state == 1 and len(words) > 0 and ':' in words[0]):

            signal_name = words[0][0:-1]               # Gets the port signal name of each Entity
            
            entity.ports.append(signal_name)           # Stores the port names in order, for further resolution
            Signal_object = D.Signal()                 # Creates Signal object for each port signal

            Signal_object.name = signal_name + "." + entity.name        # Stores like  "Signal.Entity" 

            signal_hash=hash((entity.name,signal_name))

            Signal_object.hash=signal_hash

            Signals.update({signal_hash:Signal_object})           # Stores in Signal Dictionary

        if(state==1 and len(words)>0 and words[0]=='end'):

            break

def Resolve_key(val, entity, Signals, signal_map):

    if(val == "'1'" or val == "'0'" or val == "'X'" or val == "'U'" or val == "'Z'"):

        return "Val" + val

    Ret=hash((entity, val))

    if(Ret not in Signals):

        Val = signal_map[val]

        Ret = hash((Val[0],Val[1]))

    return str(Ret)

def Make_Postfix_Expression(tokens, entity, Signals, signal_map):

    Y = []

    Stack = []

    Stack.append('(')
    tokens.append(')')

    for token in tokens:

        if(token == '('):

            Stack.append(token)

        elif(token == 'and' or token == 'or' or token == 'not'):

            while(Stack[-1] != '('):

                Y.append(Stack.pop())

            Stack.append(token)
        
        elif(token == ')' ):

            while(Stack[-1] != '('):

                Y.append(Stack.pop())
                
            Stack.pop()
        else:
            Y.append(Resolve_key(token, entity, Signals, signal_map))


    return Y

def ParseInstructions(process, entity, Signals, Instructions, signal_map):
    
    for inst in Instructions:

        tokens = inst.split()

        if('<=' and 'after' in inst):                           # Resolves Dealayed Assignment Signal

            left_val = Resolve_key(tokens[0], entity, Signals, signal_map)

            command = 'Delay'

            indx = tokens.index('after')

            postfix_expression = Make_Postfix_Expression(tokens[2:indx], entity, Signals, signal_map)

            Delay_val = int(tokens[indx+1])

            process.instructions.append([command, left_val, postfix_expression, Delay_val])

        elif('<=' in inst):                                     # Resolves Signal Assignment 

            left_val = Resolve_key(tokens[0], entity, Signals, signal_map)

            command = '<='

            postfix_expression = Make_Postfix_Expression(tokens[2:-1], entity, Signals, signal_map)

            process.instructions.append([command, left_val, postfix_expression])

        elif('wait' in inst):                                   # Resolves Wait Instruction

            command = 'wait'

            val = int(tokens[2])

            process.instructions.append([command, val])

        elif('report' in inst):                                 # Resolves Wait Instruction

            command = 'report'

            for token in tokens:

                if('&std_logic\'image' in token):

                    sig = token[token.index('(')+1:-1]
                    break
            
            Sig_Val = Resolve_key(sig, entity, Signals, signal_map)
            process.instructions.append([command, Sig_Val])

# Parses the Processes
def ParseProcess(lines, Signals, entity, signal_map, Process_Set):

    state = 0
    for line in lines:

        words = line.split()

        if(len(words)>0):

            if(state == 0 and '(' in words[0]):

                process = D.Process()
                Process_Set.add(process)
                process.Id = ['X', process]                           # 'X' indicates Signal Sensitive Process

                Instructions = []
                Sensitivity_list = words[0][words[0].index('(')+1:-1].split(',')

                for ele in Sensitivity_list:
                        
                    sig_hash = hash((entity,ele))
                    Signals[sig_hash].processes.append(process.Id)
        
                state = 1
            
            elif(state == 0 and '(' not in words[0]):

                process = D.Process()
                Process_Set.add(process)
                process.Id = ['P', process]                          # 'P' indicates Time Sensitive Process
                
                Instructions = []
                state = 1
            
            elif(state == 1 and words[0] == 'begin'):

                state = 2

            elif(state == 2 and words[0] != 'end'):

                Instructions.append(line)
            
            elif(state == 2 and words[0] == 'end'):

                ParseInstructions(process, entity, Signals, Instructions, signal_map)
                break


# Parses Architecture of each Entity
def ParseArchitectures(file, Signals, Entities, Process_Set):


    f = open(file,"r")

    lines = f.readlines()

    inst_lst = []                                 # Reads concurrent instructions of Architecture Body

    signal_map = {}                               # Local Signal to Other Signal Map


    state = 0
    count = -1

    for line in lines:

        words = line.split()

        count += 1
        if(len(words) > 0):
            
            if(state == 0 and words[0] == 'architecture'):

                entity = words[3]
                state = 1
        
            elif(state == 1 and words[0] == 'signal'):                   # Parses Signals local to Architecture

                signal_name = words[1][0:-1]
            

                Signal_object = D.Signal()

                Signal_object.name = signal_name + "." + entity

                signal_hash = hash((entity, signal_name))

                Signal_object.hash = signal_hash

                Signals.update({signal_hash:Signal_object})
        
            elif(state == 1 and words[0] == 'begin'):

                state = 2                          # Inside Architecture Body
            

            elif(state == 2 and 'port map' in line):

                ported_entity = words[1]
                signals = words[3][words[3].index('(')+1:-2].split(',')           # Gets port map signal name sequentially
                
                cnt = 0                                                           # Indicates ported signal index 

                obj = Entities[ported_entity]

                for sig in signals:

                    if(hash((entity,sig)) in Signals):

                        del Signals[hash((entity,sig))]                           # This signals are actually directing other signals

                    ori_name = obj.ports[cnt]

                    val = [ported_entity,ori_name]

                    signal_map.update({sig:val})
                    cnt += 1

            elif(state == 2 and 'process' in words[0]):

                state = 3

                ParseProcess(lines[count:], Signals, entity, signal_map, Process_Set)

            elif(state == 3 and words[0] == 'end'):
                
                state = 2
            
            elif(state == 2 and words[0] != 'end' and 'begin' not in line and 'port' not in line):

                inst_lst.append(line)         # Instruction Local to Architecture

            elif(state == 2 and words[0] == 'end' and 'end process' not in line):
                break
            
        

    
    if(len(inst_lst) > 0):                          # Some Concurrent Instructions

        process = D.Process()                      # Creates New Process, with those concurrent Instructions
        process.Id=['P',process]
        Process_Set.add(process)

        ParseInstructions(process,entity,Signals,inst_lst,signal_map)


def Parser(FileNames):

    Signals = {}
    Entities = {}
    Process_Set = set()

    for file in FileNames:

        ParseEntities(file,Signals,Entities)
    
    for file in FileNames:
        
        ParseArchitectures(file,Signals,Entities,Process_Set)



    return Entities,Signals,Process_Set


            




    
            

            

                






