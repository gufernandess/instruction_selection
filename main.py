# -*- coding: utf-8 -*-

from tree import *
from patterns import *
from instructions import *
# from networkx import *
# from displayTree import *

if __name__ == "__main__":
    source = "source.txt"
    with open(source,'r') as file:
        for line in file:
            tree = Tree()

            tree.createTree(line)

            tree.printTree(tree.root)

            print("\n\n")

            patterns = traverseTree(tree.root)

            for i in range(len(patterns)):
                print(patterns[i][1])

            print("\n")

            print("Custo total = " + "" + str(calculateCost(patterns)))

            print("\n")

            print(getInstructions(patterns))
"""
Considerações:
    - Preciso averiguar melhor se esse "for line in file"
    também extrai as linhas de breakline
"""
