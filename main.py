# -*- coding: utf-8 -*-

from tree import *
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
            # leaves = myTree.root.getLeaves()
            # getTiles(leaves)
            # draw(myTree.root)
    
"""
Considerações:
    - Preciso averiguar melhor se esse "for line in file"
    também extrai as linhas de breakline
"""
