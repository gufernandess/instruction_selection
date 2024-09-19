# -*- coding: utf-8 -*-

from tree import *
from instructions import *
#from networkx import *
#from displayTree import *

if __name__ == "__main__":
    sourceCode = "sourceCode.txt"
    with open(sourceCode,'r') as file:
        for line in file:
            myTree = Tree()
            myTree.createTree(line)
            leaves =myTree.root.getLeaves()
            getTiles(leaves)
            #draw(myTree.root)
    
"""
Considerações:
    - Preciso averiguar melhor se esse "for line in file"
    também extrai as linhas de breakline
"""
