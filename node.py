class Node():
    def __init__(self, instruction):
        self.instruction = instruction
        self.parent = None
        self.left = None
        self.right = None
        self.isRoot = True
        self.pattern = None

    def getChildren(self):
        return (self.left, self.right)
    
    def getSingleValue(self, reg):
        if(self.instruction is not None):
            if(self.instruction[:5] == "CONST" or self.instruction[:4] == "TEMP"):
                return self.instruction[-1]
            elif(self.instruction == "FP"):
                return "fp"
        else: 
            return reg