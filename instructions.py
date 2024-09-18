'''
    A ideia é mapear os padrões da arquitetura Jouette para as instruções de máquina,
    assim, a partir de um padrão de um nó da árvore de expressão, é possível gerar
    a instrução de máquina correspondente.
'''

PATTERNS_INSTRUCTIONS = {
    "+": "ADD r{i} <- {j} + {k}",
    "*": "MUL r{i} <- {j} * {k}",
    "-": "SUB r{i} <- {j} - {k}",
    "/": "DIV r{i} <- {j} / {k}",
    "+ -> CONST": "ADDI r{i} <- {j} + {c}",
    "+ ---> CONST": "ADDI r{i} <- {j} + {c}",
    "CONST": "ADDI r{i} <- r{j} + {c}",
    "- ---> CONST": "SUBI r{i} <- {j} - {c}",
    "MEM --> + ---> CONST": "LOAD r{i} <- M[{j} + {c}]",
    "MEM --> + -> CONST" : "LOAD r{i} <- M[{j} + {c}]",
    "MEM --> CONST" : "LOAD r{i} <- M[r{j} + {c}]",
    "MEM": "LOAD r{i} <- M[r{j}]",
    "MOVE -> MEM --> + ---> CONST": "STORE M[{j} + {c}] <- r{i}",
    "MOVE -> MEM --> + -> CONST": "STORE M[{j} + {c}] <- r{i}",
    "MOVE -> MEM --> CONST": "STORE M[r{j} + {c}] <- r{i}",
    "MOVE -> MEM": "STORE M[r{j}] <- r{i}",
    "MOVE -> MEM ===> MEM": "MOVEM M[r{j}] <- M[r{i}]",
}

'''
    A função getInstructions recebe uma lista de listas, onde cada lista contém um nó da árvore de expressão
    e o padrão correspondente a esse nó. O padrão serve para que a função possa mapear o padrão para a instrução,
    enquanto o nó serve para que a função possa acessar os valores dos nós da árvore de expressão.

    A lista respeita o seguinte formato:

    [
        [Node, pattern],
        [Node, pattern],
        ...
    ]
'''

def getInstructions(patterns):
    reg1 = 1
    reg2 = 2

    patterns = patterns[::-1]

    for i in range(len(patterns)):
        node = patterns[i][0]
        pattern = patterns[i][1]
        
        instruction = PATTERNS_INSTRUCTIONS[pattern]
            
        if(pattern == "TEMP"):
            reg2 = reg1
            reg1 += 1
            
        if(pattern in ["+","*","-","/"]):
            print(i+1, instruction.format(i=reg2, j=node.left.getSingleValue(reg1), k=node.right.getSingleValue(reg2)))

        if(pattern in ["+ -> CONST", "+ ---> CONST", "- ---> CONST"]):
            right = node.right.getSingleValue(reg1) 
            left = node.left.getSingleValue(reg1+1)

            if(pattern == "+ -> CONST" or pattern == "- ---> CONST"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))

            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))   
            
        if(pattern == "CONST"):
            print(i+1, instruction.format(i=reg2, j=0, c=node.getSingleValue(reg1)))
            
        if (pattern in ["MEM --> + ---> CONST", "MEM --> + -> CONST"]):
            child = node.getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if (pattern == "MEM --> + ---> CONST"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  
            
        if(pattern == "MEM --> CONST"):
            child = node.getChildren()[0]

            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if (pattern == "MEM"):
            print(i+1, instruction.format(i=reg2, j=reg2, c=0))

        if(pattern in ["MOVE -> MEM --> + ---> CONST", "MOVE -> MEM --> + -> CONST"]):
            child = node.getChildren()[0].getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if(pattern == "MOVE -> MEM --> + ---> CONST"):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  

        if(pattern == "MOVE -> MEM --> CONST"):
            child = node.getChildren()[0].getChildren()[0]
            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if(pattern == "MOVE -> MEM"):
            print(i+1, instruction.format(i=reg2, j=reg1, c=0))
            
        if(pattern == "MOVE -> MEM ===> MEM"):
            print(i+1, instruction.format(i=reg2, j=reg1))