
# Maximum number of Signal Supported
MAX_SIGNAL = 251

# Maximum number of Process supported
MAX_PROCESS = 254

#Signal values
VALUE_U = 251
VALUE_X = 252
VALUE_0 = 253
VALUE_1 = 254
VALUE_Z = 255

# Structured Signal Data Type

SIG_DATA_TYPE = [('Eff_Val','u1'),('Driver_Head','u2'),('Driving_Count','u1'),('Triggered_Process_Start','u2'),('Triggered_Process_Count','u1')]

# Maximum no of Delayed Assignments

MAX_DELAYED_ASSIGNMENTS = 255

# Delayed Assignment Data Type

DELAYED_ASSIGNMENT_TYPE = [('Id','i1'),('Sig_Index','u1'),('Value','u1')]


# Maximum words in Instruction Array

MAX_INSTRUCTION_WORD = 65535

# Maximum Size of Driver Array

MAX_DRIVER_SIZE = 65535

# Maximum Trigerring Process Count

MAX_TRIGGERING_PROCESS = 65535

# If a Signal do not triggering any Process, then its Driving Head will be

NON_TRIGGERING = 65535

# Maximum Driver number for single Signal

MAX_SIGNAL_DRIVER = 255

# Signal Triggered Process Data Type

SIG_TRIGGERED_PROCESS_TYPE = [('Instruction_Start_Index','u2'),('Instruction_End_Index','u2'),('Current_Instruction_Index','u2'),('Triggered_Bit','u1')]

# Time Triggered Process Data Type

TIME_TRIGGERED_PROCESS_TYPE = [('Instruction_Start_Index','u2'),('Instruction_End_Index','u2'),('Current_Instruction_Index','u2')]