"""
The Node class for building trees
"""
class Node(object):
    """
    The basic Node of a Tree data structue

    Basic Usage:

    >>> a = Node('first')
    >>> b = Node('second')
    >>> a.add_child(b)
    """
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        """
        Adds a child node to the current node

        :param node: the child node being added to the
        current nod
        :type node: Node

        :return: None
        """
        self.children.append(node)


    def find(self, name):
        """
        Searches the node's path for a given node by
        the node's name

        :param name: the name of the node to find
        :type name: str

        :return: Node or None
        """
        if self.name == name:
            return self

        for node in self.children:
            node_ = node.find(name)

            if node_:
                return node_

        return None


    def create_path(self, paths):
        """
        Adds a series of nodes to a given node such that
        each node forms a chain of nodes to a given
        node

        :param paths: a series of node names
        :type paths: List<str>

        :return: None
        """
        current_node = self

        for path in paths:
            node = Node(path)

            if current_node:
                current_node.add_child(node)

            current_node = node
