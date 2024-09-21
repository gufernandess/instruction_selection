from tree import *
from patterns import *
from instructions import *

def main():
    source = "source.txt"
    with open(source,'r') as file:
        instructionCounter = 1
        for line in file:
            if (line != "\n") :
                print(f"-=-=-=-=-=-=-=-=Instrução {instructionCounter}-=-=-=-=-=-=-=")
                print("\n-----Árvore-----")
                tree = Tree()

                tree.createTree(line)

                tree.draw()

                print("\n-----Padrões e custos-----\n")

                patterns = []

                patterns = traverseTree(tree.root, patterns)

                for i in range(len(patterns)):
                    print(patterns[i][1])

                print("\n")

                cost = calculateCost(patterns)

                print("Custo total = " + "" + str(cost))

                print("\n-----Instruções Assembly-----")

                print("\n")

                print(getInstructions(patterns))

                instructionCounter += 1

if __name__ == "__main__":
    main()
