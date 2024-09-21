from tree import *
from patterns import *
from instructions import *

def main():
    source = "source.txt"
    with open(source,'r') as file:
        instructionCounter = 1
        for line in file:
            if (line != "\n") :
                print(f"-=-=-=-=-=-=-=-=intrução {instructionCounter}-=-=-=-=-=-=-=")
                print("\n-----Árvore-----")
                tree = Tree()

                tree.createTree(line)

                tree.draw()

                print("\n-----Custos-----\n")

                patterns = traverseTree(tree.root)

                for i in range(len(patterns)):
                    print(patterns[i][1])

                print("\n")

                print("Custo total = " + "" + str(calculateCost(patterns)))

                print("\n-----INSTRUÇÕES ASSEMBLY-----")
                
                instructions = getInstructions(patterns)

                for instruction in instructions:
                    print(instruction)

                instructionCounter += 1

if __name__ == "__main__":
    main()
