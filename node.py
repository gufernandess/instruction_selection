class Node():
    def __init__(self, instruction):
        self.instruction = instruction
        self.parent = None
        self.left = None
        self.right = None

    def getChildren(self):
        return (self.left, self.right)
    
    def getSingleValue(self, reg):
        if(self.instruction[:5] == "CONST"):
            return self.instruction[-1]
        
        elif(self.instruction == "FP"):
            return "fp"
        
        elif(self.instruction[:4] == "TEMP"):
            return "r" + str(self.instruction[-1])
        
        else: 
            return "r" + str(reg)