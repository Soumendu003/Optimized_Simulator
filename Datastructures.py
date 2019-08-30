
class Entity():

    def __init__(self,name):

        self.name=name

        self.ports=[]


class Process:

    def __init__(self):

        self.Hash_Val=-1

        self.Id=[]

        self.execution_contex=0

        self.instructions=[]

        self.Instruction_Start = -1
        self.Instruction_End = -1



class Signal:

    def __init__(self):

        self.name=''

        self.Hash_Val=-1                # Corresponding Index of Signal in Light_Signal Array

        self.hash=''

        self.Driver={}      # Make a mapping from process to  here   { Process_Hash : process_object }

        self.Delay_Driver = []

        self.processes=[]

        self.Driving_Head = -1

        self.Driving_Count = 0

        self.Triggering_Process_Start = -1
    
