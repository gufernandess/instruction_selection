# -*- coding: utf-8 -*-

from tree import *
from networkx import *
#trial
def main():
    sourceCode = "sourceCode.txt"
    with open(sourceCode,'r') as file:
        for line in file:
            myTree = Tree()
            myTree.createTree(line)
            a = "deu certo"
            print("deu certo")

if __name__ == "__main__":
    main()
    
"""
Considerações:
    - Preciso averiguar melhor se esse "for line in file"
    também extrai as linhas de breakline
"""