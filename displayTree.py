# # -*- coding: utf-8 -*-

# import matplotlib.pyplot as plt
# import networkx as nx

# # Define a function to create a BST
# def add_edges(graph, node, pos, level=0, width=4., vert_gap=0.4, x=0, y=0, nodes={}, node_counter=[0]):
#     if node is not None:
#         # Create a unique identifier for the node
#         unique_id = f"{node.instruction}_{node_counter[0]}"
#         node_counter[0] += 1  # Increment the counter for uniqueness
        
#         # Add the node to the graph with a unique identifier
#         graph.add_node(unique_id, pos=(x, y))
#         nodes[unique_id] = (x, y)
        
#         # Check if the node has only a left child and no right child
#         if node.left and not node.right:
#             # Align the left child vertically with the parent
#             child_unique_id = f"{node.left.instruction}_{node_counter[0]}"
#             graph.add_edge(unique_id, child_unique_id)
#             add_edges(graph, node.left, pos, level + 1, width, vert_gap, x, y - vert_gap, nodes, node_counter)

#         else:
#             # Add left child with increased horizontal spacing
#             if node.left:
#                 child_unique_id = f"{node.left.instruction}_{node_counter[0]}"
#                 graph.add_edge(unique_id, child_unique_id)
#                 add_edges(graph, node.left, pos, level + 1, width * 1.5, vert_gap, 
#                           x - width / (2 ** (level + 1)), y - vert_gap, nodes, node_counter)
            
#             # Add right child with increased horizontal spacing
#             if node.right:
#                 child_unique_id = f"{node.right.instruction}_{node_counter[0]}"
#                 graph.add_edge(unique_id, child_unique_id)
#                 add_edges(graph, node.right, pos, level + 1, width * 1.5, vert_gap, 
#                           x + width / (2 ** (level + 1)), y - vert_gap, nodes, node_counter)




# # Define the BST structure
# class TreeNode:
#     def __init__(self, value, left=None, right=None):
#         self.value = value
#         self.left = left
#         self.right = right


# def draw(tree):
#     G = nx.Graph()
#     nodes = {}
#     add_edges(G, tree, pos={}, nodes=nodes)
    
#     # Draw the graph
#     pos = nx.get_node_attributes(G, 'pos')
#     labels = {n: n for n in G.nodes()}
#     nx.draw(G, pos, labels=labels, with_labels=True, node_size=1000, node_color='lightblue', font_size=8, font_weight='bold', edge_color='gray')
#     plt.title('Binary Search Tree')
#     plt.savefig('bst.png')
#     plt.show()

# """
# root = TreeNode(8,
#                 TreeNode(3,
#                          TreeNode(1),
#                          TreeNode(6, TreeNode(4), TreeNode(7))),
#                 TreeNode(10, None, TreeNode(14, TreeNode(13)))
#                )
# """