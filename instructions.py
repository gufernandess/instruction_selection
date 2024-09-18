PATTERNS_INSTRUCTIONS = {
    "+": "ADD r{i} <- r{j} + r{k}",
    "*": "MUL r{i} <- r{j} * r{k}",
    "-": "SUB r{i} <- r{j} - r{k}",
    "/": "DIV r{i} <- r{j} / r{k}",
    "+ -> CONST {c}": "ADDI r{i} <- r{j} + {c}",
    "+ ---> CONST {c}": "ADDI r{i} <- r{j} + {c}",
    "CONST {c}": "ADDI r{i} <- r{j} + {c}",
    "- ---> CONST {c}": "SUBI r{i} <- r{j} - {c}",
    "MEM --> + ---> CONST {c}": "LOAD r{i} <- M[r{j} + {c}]",
    "MEM --> + -> CONST {c}" : "LOAD r{i} <- M[r{j} + {c}]",
    "MEM --> CONST {c}" : "LOAD r{i} <- M[r{j} + {c}]",
    "MEM": "LOAD r{i} <- M[r{j}]",
    "MOVE -> MEM --> + ---> CONST {c}": "STORE M[r{j} + {c}] <- r{i}",
    "MOVE -> MEM --> + -> CONST {c}": "STORE M[r{j} + {c}] <- r{i}",
    "MOVE -> MEM --> CONST {c}": "STORE M[r{j} + {c}] <- r{i}",
    "MOVE -> MEM": "STORE M[r{j}] <- r{i}",
    "MOVE -> MEM ===> MEM": "MOVEM M[r{j}] <- M[r{i}]",
}

def getInstructions(patterns):
    reg1 = reg2 = 1

    patterns = patterns[::-1]

    for i in range(len(patterns)):
        node = patterns[i][0]
        pattern = patterns[i][1]
        
        instruction = PATTERNS_INSTRUCTIONS[pattern]
            
        if(pattern == "TEMP {i}"):
            reg2 = reg1
            reg1 += 1
            
        if(pattern in ["+","*","-","/"]):
            print(i+1, instruction.format(i=reg2, j=node.left.getSingleValue(reg1), k=reg2))

        if(pattern in ["+ -> CONST {c}", "+ ---> CONST {c}", "- ---> CONST {c}"]):
            right = node.right.getSingleValue(reg1) 
            left = node.left.getSingleValue(reg1+1)

            if(pattern == "+ -> CONST {c}" or pattern == "- ---> CONST {c}"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))

            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))   
            
        if(pattern == "CONST {c}"):
            print(i+1, instruction.format(i=reg2, j=0, c=node.getSingleValue(reg1)))
            
        if (pattern in ["MEM --> + ---> CONST {c}", "MEM --> + -> CONST {c}"]):
            child = node.getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if (pattern == "MEM --> + ---> CONST {c}"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  
            
        if(pattern == "MEM --> CONST {c}"):
            child = node.getChildren()[0]

            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if (pattern == "MEM"):
            print(i+1, instruction.format(i=reg2, j=reg2, c=0))

        if(pattern in ["MOVE -> MEM --> + ---> CONST {c}", "MOVE -> MEM --> + -> CONST {c}"]):
            child = node.getChildren()[0].getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if(pattern == "MOVE -> MEM --> + ---> CONST {c}"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  

        if(pattern == "MOVE -> MEM --> CONST {c}"):
            child = node.getChildren()[0].getChildren()[0]
            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if(pattern == "MOVE -> MEM"):
            print(i+1, instruction.format(i=reg2, j=reg1, c=0))
            
        if(pattern == "MOVE -> MEM ===> MEM"):
            print(i+1, instruction.format(i=reg2, j=reg1))