from typing import Tuple, Union, Iterable, Dict, List

Node = Union[str, int]
Edge = Tuple[Node, Node]


class Graph:
    """Graph data structure, undirected by default."""

    def __init__(self, edges: Iterable[Edge] = [], directed: bool = False):
        self.directed = directed
        self.adjacency_list: Dict[Node, List[Node]] = {}
        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node: Node) -> bool:
        """Whether a node is in graph"""
        return node in self.adjacency_list

    def has_edge(self, edge: Edge) -> bool:
        """Whether an edge is in graph"""
        node1, node2 = edge
        return node1 in self.adjacency_list and node2 in self.adjacency_list[node1]

    def add_node(self, node: Node):
        """Add a node"""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, edge: Edge):
        """Add an edge (node1, node2). For directed graph, node1 -> node2"""
        node1, node2 = edge
        self.add_node(node1)
        self.add_node(node2)
        self.adjacency_list[node1].append(node2)
        if not self.directed:
            self.adjacency_list[node2].append(node1)

    def remove_node(self, node: Node):
        """Remove all references to node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not found in the graph.")

        del self.adjacency_list[node]
        for n in self.adjacency_list:
            if node in self.adjacency_list[n]:
                self.adjacency_list[n].remove(node)

    def remove_edge(self, edge: Edge):
        """Remove an edge from graph"""
        node1, node2 = edge
        if node1 not in self.adjacency_list or node2 not in self.adjacency_list:
            raise ValueError(f"Edge {edge} not found in the graph.")

        if node2 in self.adjacency_list[node1]:
            self.adjacency_list[node1].remove(node2)
        if not self.directed and node1 in self.adjacency_list[node2]:
            self.adjacency_list[node2].remove(node1)

    def indegree(self, node: Node) -> int:
        """Compute indegree for a node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not found in the graph.")
        return sum(1 for edges in self.adjacency_list.values() if node in edges)

    def outdegree(self, node: Node) -> int:
        """Compute outdegree for a node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not found in the graph.")
        return len(self.adjacency_list[node])

    def __str__(self) -> str:
        return str(self.adjacency_list)

    def __repr__(self) -> str:
        return f"Graph(directed={self.directed}, edges={self.adjacency_list})"
