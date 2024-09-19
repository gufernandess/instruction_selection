class Node():
    def __init__(self, instruction):
        self.instruction = instruction
        self.parent = None
        self.left = None
        self.right = None
        self.tile = []

    def getChildren(self):
        return (self.left, self.right)
    
    def getLeaves(self):
        leaves = []

        if(self.left == None and self.right == None):
            leaves.append(self)
        
        else:
            if(self.left):
                leaves += self.left.getLeaves()
            if(self.right):
                leaves += self.right.getLeaves()

        return leaves
    
    def getSingleValue(self, reg):
        if(self.instruction[:5] == "CONST"):
            return self.instruction[-1]
        
        elif(self.instruction == "FP"):
            return "fp"
        
        elif(self.instruction[:4] == "TEMP"):
            return "r" + str(self.instruction[-1])
        
        else: 
            return "r" + str(reg)