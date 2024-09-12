from typing import *

LEFT_CHILD = False
RIGHT_CHILD = True
global whereToinsert

class Node():
    def __init__(self, instruction):
        self.instruction:str = instruction
        self.parent:Node = None
        self.left:Node = None
        self.right:Node = None

class Tree():
    def __init__(self, root = None):
        self.root = root
        self.scope = []
        self.reducibleInstructions = ["MOVE", "MEM", "+", "-", "*", "/"]
        self.irreducibleInstructions = ["CONST", "FP", "TEMP"]
        self.instructions = self.reducibleInstructions + self.irreducibleInstructions
        self.validSeparators = [",", "(", ")"]
        
    def isIrredutiableInstruction(self, instruction) -> bool:
        """
        Uma instrução é irredutível se não pode ser
        derivada em outras instruções. Neste caso,
        elas são as folhas da árvore de instrução.
        No contexto da arquitetura Joutte, elas per-
        tecem a este conjunto {CONST X, FP, TEMP i}
        """        
        return instruction in self.irreducibleInstructions
   
    def isCompoundInstruction(self, instruction:str) -> bool:
        """
        Uma instrução é dita composta se existe um espaço
        entre o seu tipo e o valor associado a ele. Por
        exemplo, 'CONST 2' é uma instrução composta, pois
        existe um espaço separando o 'CONST' e o '2'.
        Todas as instruções compostas são irredutíveis,
        mas o inverso não é verdadeiro.
        """
        return instruction in ["CONST", "TEMP"]
    
    def createTree(self, linearCode:str):
        spacelessLinearCode = linearCode.split()
        reducibleInstructions = []
        
        #for instruction in spacelessLinearCode:
        #    if instruction in self.reducibleInstructions:
        #        reducibleInstructions.append(instruction)
        """
        De início, a insertção dos filhos começa sempre
        nas sub-árvores esquerdas. Só começamos a inserir
        nas subárvores direitas quando lemos uma vírgula. 
        """
        whereToInsert = LEFT_CHILD #ORIGINAL
        #global whereToinsert
        currentNode:Node = None
        previousNode:Node = None
        
        for indexInstruction in range(len(spacelessLinearCode)):
            #nonlocal whereToinsert
            currentInstruction = spacelessLinearCode[indexInstruction]
            
            """
            Se lermos uma instrução composta, é necessário avançar o index 2 vezes,
            pois se a primeira metade da instrução composta estiver no i-ésimo
            indice, a sua segunda metade estará no i+1-ésimo indice, o que fará
            com que tenhamos que pular um indice ao final do código. A flag 
            "jumpIndex" indica a necessidade de pular mais um indice.
            """
            jumpIndex = False
            if (currentInstruction in self.instructions):
                if (self.isCompoundInstruction(currentInstruction)):
                    """
                    É necessário concatenar as duas partes
                    """
                    secondHalfInstruction = spacelessLinearCode[indexInstruction+1]
                    currentInstruction += " " + secondHalfInstruction
                    jumpIndex = True
                
                newNode = Node(currentInstruction)
                
                """
                Se eu não tiver nenhum escopo pronto,
                significa que a árvore está vazia e 
                que é necessário criá-la
                """
                if (len(self.scope) == 0):
                    self.root = newNode
                    previousNode = newNode
                
                elif (previousNode):
                    newNode.parent = previousNode
                    if (whereToInsert == LEFT_CHILD):
                        self.scope[-1].left = newNode
                    else:
                        self.scope[-1].right = newNode
                        whereToInsert = LEFT_CHILD
                    previousNode = newNode
                
                if currentInstruction in self.reducibleInstructions:
                    self.scope.append(newNode)
                
                if (jumpIndex):
                    indexInstruction +=1
                    
            elif (currentInstruction == "("):
                continue
            elif (currentInstruction == ")"):
                self.scope.pop()
                if (len(self.scope) != 0):
                    previousNode = self.scope[-1]
            elif (currentInstruction == ","):
                whereToInsert = RIGHT_CHILD #COPY
        