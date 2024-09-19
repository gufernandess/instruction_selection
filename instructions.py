'''
    A ideia é mapear os padrões da arquitetura Jouette para as instruções de máquina,
    assim, a partir de um padrão de um nó da árvore de expressão, é possível gerar
    a instrução de máquina correspondente.
'''

PATTERNS_INSTRUCTIONS = {
    0: "ADD r{i} <- {j} + {k}", # +
    1: "MUL r{i} <- {j} * {k}", # *
    2: "SUB r{i} <- {j} - {k}", # -
    3: "DIV r{i} <- {j} / {k}", # /
    4: "ADDI r{i} <- {j} + {c}", # + -> CONST
    5: "ADDI r{i} <- {j} + {c}", # + ---> CONST
    6: "ADDI r{i} <- r{j} + {c}", # CONST
    7: "SUBI r{i} <- {j} - {c}", # - ---> CONST
    8: "LOAD r{i} <- M[{j} + {c}]", # MEM --> + ---> CONST
    9: "LOAD r{i} <- M[{j} + {c}]", # MEM --> + -> CONST
    10: "LOAD r{i} <- M[r{j} + {c}]", # MEM --> CONST
    11: "LOAD r{i} <- M[r{j}]", # MEM
    12: "STORE M[{j} + {c}] <- r{i}", # MOVE -> MEM --> + ---> CONST
    13: "STORE M[{j} + {c}] <- r{i}", # MOVE -> MEM --> + -> CONST
    14: "STORE M[r{j} + {c}] <- r{i}", # MOVE -> MEM --> CONST
    15: "STORE M[r{j}] <- r{i}", # MOVE -> MEM
    16: "MOVEM M[r{j}] <- M[r{i}]", # MOVE -> MEM ===> MEM
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
            
        if(pattern == "TEMP" or pattern == "FP"):
            reg2 = reg1
            reg1 += 1
            
        if(pattern in [0, 1, 2, 3]):
            print(i+1, instruction.format(i=reg2, j=node.left.getSingleValue(reg1), k=node.right.getSingleValue(reg2)))

        if(pattern in [4, 5, 7]):
            right = node.right.getSingleValue(reg1) 
            left = node.left.getSingleValue(reg1+1)

            if(pattern == 4 or pattern == 7):
                print(i+1, instruction.format(i=reg2, j=left, c=right))

            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))   
            
        if(pattern == 6):
            print(i+1, instruction.format(i=reg2, j=0, c=node.getSingleValue(reg1)))
            
        if (pattern in [8, 9]):
            child = node.getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if (pattern == 8):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  
            
        if(pattern == 10):
            child = node.getChildren()[0]

            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if (pattern == 11):
            print(i+1, instruction.format(i=reg2, j=reg2, c=0))

        if(pattern in [12, 13]):
            child = node.getChildren()[0].getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg1+1)

            if(pattern == 12):
                print(i+1, instruction.format(i=reg2, j=left, c=right))
            else:
                print(i+1, instruction.format(i=reg2, j=right, c=left))  

        if(pattern == 14):
            child = node.getChildren()[0].getChildren()[0]
            print(i+1, instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if(pattern == 15):
            print(i+1, instruction.format(i=reg2, j=reg1, c=0))
            
        if(pattern == 16):
            print(i+1, instruction.format(i=reg2, j=reg1))