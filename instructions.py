'''
    A ideia é mapear os padrões da arquitetura Jouette para as instruções de máquina,
    assim, a partir de um padrão de um nó da árvore de expressão, é possível gerar
    a instrução de máquina correspondente.
'''

from tree import *

PATTERNS_INSTRUCTIONS = {
    "+": "ADD r{i} <- {j} + {k}", # +
    "*": "MUL r{i} <- {j} * {k}", # *
    "-": "SUB r{i} <- {j} - {k}", # -
    "/": "DIV r{i} <- {j} / {k}", # /
    "+ -> CONST": "ADDI r{i} <- {j} + {c}", # + -> CONST
    "+ --> CONST": "ADDI r{i} <- {j} + {c}", # + --> CONST
    "CONST": "ADDI r{i} <- r{j} + {c}", # CONST
    "- --> CONST": "SUBI r{i} <- {j} - {c}", # - --> CONST
    "MEM -> + --> CONST": "LOAD r{i} <- M[{j} + {c}]", # MEM -> + --> CONST
    "MEM -> + -> CONST": "LOAD r{i} <- M[{j} + {c}]", # MEM -> + -> CONST
    "MEM -> CONST": "LOAD r{i} <- M[r{j} + {c}]", # MEM -> CONST
    "MEM": "LOAD r{i} <- M[{j} + {c}]", # MEM
    "MOVE -> MEM -> + --> CONST": "STORE M[{j} + {c}] <- r{i}", # MOVE -> MEM -> + --> CONST
    "MOVE -> MEM -> + -> CONST": "STORE M[{j} + {c}] <- r{i}", # MOVE -> MEM -> + -> CONST
    "MOVE -> MEM -> CONST": "STORE M[r{j} + {c}] <- r{i}", # MOVE -> MEM -> CONST
    "MOVE -> MEM": "STORE M[r{j} + {c}] <- r{i}", # MOVE -> MEM
    "MOVE -> MEM ===> MEM": "MOVEM M[r{j}] <- M[r{i}]", # MOVE -> MEM ===> MEM
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
    instructions = []
    
    reg1 = 1
    reg2 = 2
    
    line_count = 0
    patterns = patterns[::-1]

    for i in range(len(patterns)):
        node = patterns[i][0]
        pattern = patterns[i][1]

        if(pattern == "FP" or pattern == "TEMP"):
            line_count += 1
            continue
        
        instruction = PATTERNS_INSTRUCTIONS[pattern]
        line_count += 1

        if(pattern == "+"):
            instructions.append(instruction.format(i=reg1, j=node.left.getSingleValue(reg1), k=node.right.getSingleValue(reg2)))

        if pattern in ["*", "-", "/"]:
            left_value = node.left.getSingleValue(reg1) if node.left.instruction[:5] != "CONST" else "r" + str(reg1)
            right_value = node.right.getSingleValue(reg2) if node.right.instruction[:5] != "CONST" else "r" + str(reg2)
            instructions.append(instruction.format(i=reg2, j=left_value, k=right_value))

        if(pattern in ["+ -> CONST", "+ --> CONST", "- --> CONST"]):
            right = node.right.getSingleValue(reg1) 
            left = node.left.getSingleValue(reg2)
            if(pattern == "+ -> CONST" or pattern == "- --> CONST"):
                instructions.append(instruction.format(i=reg2, j=right, c=left))
            else:
                instructions.append(instruction.format(i=reg2, j=left, c=right))   

        if(pattern == "CONST"):
            instructions.append(instruction.format(i=reg2, j=0, c=node.getSingleValue(reg1)))

        if (pattern in ["MEM -> + --> CONST", "MEM -> + -> CONST"]):
            child = node.getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg2)
            if (pattern == "MEM -> + --> CONST"):
                instructions.append(instruction.format(i=reg1, j=left, c=right))
            else:
                instructions.append(instruction.format(i=reg1, j=right, c=left))  

        if(pattern == "MEM -> CONST"):
            child = node.getChildren()[0]
            instructions.append(instruction.format(i=reg2, j=0, c=child.getSingleValue(reg1)))

        if (pattern == "MEM"):
            instructions.append(instruction.format(i=reg2, j=reg1, c=0))

        if(pattern in ["MOVE -> MEM -> + --> CONST", "MOVE -> MEM -> + -> CONST"]):
            child = node.getChildren()[0].getChildren()[0]
            right = child.right.getSingleValue(reg1) 
            left = child.left.getSingleValue(reg2)
            if(pattern == "MOVE -> MEM -> + --> CONST"):
                instructions.append(instruction.format(j=left, c=right, i=reg2))
            else:
                instructions.append(instruction.format(j=right, c=left, i=reg2))  

        if(pattern == "MOVE -> MEM -> CONST"):
            child = node.getChildren()[0].getChildren()[0]
            instructions.append(instruction.format(j=reg2, c=child.getSingleValue(reg1), i=0))

        if(pattern == "MOVE -> MEM"):
            instructions.append(instruction.format(j=reg1, c=0, i=reg2))

        if(pattern == "MOVE -> MEM ===> MEM"):
            instructions.append(instruction.format(i=reg2, j=reg1))

    return instructions
