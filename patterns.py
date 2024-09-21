from node import Node

patterns = []

'''
    A ideia aqui foi criar um algoritmo que percorre a árvore de cima para baixo
    e a cada nó visitado, ele verifica se o nó já foi visitado.
    Se o nó já foi visitado, ele passa para o próximo nó.
    Se o nó não foi visitado, ele verifica o padrão do nó
    e o armazena em uma lista de padrões.

    Aqui os custos são mapeados para cada padrão.
'''

INSTRUCTION_COSTS = {
    "TEMP": 0,
    "FP": 1,
    "+": 1,
    "*": 1,
    "-": 1,
    "/": 1,
    "+ -> CONST": 1,
    "+ --> CONST": 1,
    "CONST": 1,
    "- --> CONST": 1,
    "MEM -> + --> CONST" : 1,
    "MEM -> + -> CONST": 1,
    "MEM -> CONST": 1,
    "MEM" : 1,
    "MOVE -> MEM -> + --> CONST": 1,
    "MOVE -> MEM -> + -> CONST": 1,
    "MOVE -> MEM -> CONST": 1,
    "MOVE -> MEM" : 1,
    "MOVE -> MEM ===> MEM": 2,
}

def calculateCost(patterns):
    cost = 0
    for i in range(len(patterns)):
        cost += INSTRUCTION_COSTS[patterns[i][1]]

    return cost

def traverseTree(node:Node):
    if node is None:
        return
    
    if node.isUsed:
        if node.right is not None:
            traverseTree(node.right)
        if node.left is not None:
            traverseTree(node.left)

    else:
        patterns.append([node, treeToPattern(node)])
    
        traverseTree(node.right)

        traverseTree(node.left)

    return patterns


def treeToPattern(node:Node):
    pattern = ""

    if(node.instruction[:5] == "CONST"):
        pattern += "CONST"
        node.isUsed = True
    if(node.instruction[:4] == "TEMP"):
        pattern += "TEMP"
        node.isUsed = True
    if(node.instruction == "FP"):
        pattern += "FP"
        node.isUsed = True
    if(node.instruction == "+"):
        pattern += "+"
        node.isUsed = True
        if(node.left.instruction[:5] == "CONST"):
            pattern += " -> CONST"
            node.left.isUsed = True
        elif(node.right.instruction[:5] == "CONST"):
            pattern += " --> CONST"
            node.right.isUsed = True
    if(node.instruction == "-"):
        pattern += "-"
        node.isUsed = True
        if(node.right.instruction[:5] == "CONST"):
            pattern += " --> CONST"
            node.right.isUsed = True
    if(node.instruction == "*"):
        pattern += "*"
        node.isUsed = True
    if(node.instruction == "/"):
        pattern += "/"
        node.isUsed = True
    if(node.instruction == "MEM"):
        pattern += "MEM"
        node.isUsed = True
        if(node.left.instruction == "+"):
            pattern += " -> +"
            node.left.isUsed = True
            if(node.left.right.instruction[:5] == "CONST"):
                pattern += " --> CONST"
                node.left.right.isUsed = True
            elif(node.left.left.instruction[:5] == "CONST"):
                pattern += " -> CONST"
                node.left.left.isUsed = True
        elif(node.left.instruction[:5] == "CONST"):
            pattern += " -> CONST"
            node.left.isUsed = True
    if(node.instruction == "MOVE"):
        pattern += "MOVE"
        node.isUsed = True
        if(node.left.instruction == "MEM" and node.right.instruction == "MEM"):
            pattern += " -> MEM ===> MEM"
            node.left.isUsed = True
            node.right.isUsed = True
        else:
            if(node.left.instruction == "MEM"):
                pattern += " -> MEM"
                node.left.isUsed = True
                if(node.left.left.instruction == "+"):
                    pattern += " -> +"
                    node.left.left.isUsed = True
                    if(node.left.left.left.instruction[:5] == "CONST"):
                        pattern += " -> CONST"
                        node.left.left.left.isUsed = True
                    else:
                        pattern += " --> CONST"
                        node.left.left.right.isUsed = True
                elif(node.left.left.instruction[:5] == "CONST"):
                    pattern += " -> CONST"
                    node.left.left.isUsed = True

    return pattern
