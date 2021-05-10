from Section2.queue import Queue
from Section2.stack import Stack


class Vertex:
    """
    An example implementation of a Vertex or Node of a graph.
    """
    def __init__(self, key):
        """
        Creates a new Vertex.
        """
        self._neighbors = []
        self._key = key

    def add_neighbor(self, neighbor_vertex, weight):
        self._neighbors.append((neighbor_vertex, weight))

    def get_connections(self):
        return self._neighbors

    def get_key(self):
        return self._key

    def get_weight(self, to_vertex):
        for neighbor in self._neighbors:
            if to_vertex == neighbor[0].get_key():
                return neighbor[1]


class Graph:
    """
    An example implementation of Directed Graph ADT.
    """
    def __init__(self):
        """
        Creates a new, empty Graph.
        """
        self._vertices = {}

    def add_vertex(self, vertex):
        """
        Adds a new vertex into the graph.
        :param vertex: The Vertex to be added into the Graph.
        :return: None.
        """
        v = Vertex(vertex)
        self._vertices[vertex] = v

    def add_edge(self, from_vertex, to_vertex, weight):
        """
        Add a directed edge between two vertices
        :param from_vertex: Starting vertex of the edge
        :param to_vertex: Where the edge ends.
        :param weight: weight of the edge
        :return: None
        """
        if from_vertex not in self._vertices:
            self.add_vertex(from_vertex)

        if to_vertex not in self._vertices:
            self.add_vertex(to_vertex)

        self._vertices[from_vertex].add_neighbor(self._vertices[to_vertex], weight)

    def get_vertices(self):
        """
        Get all the vertices of the directed Graph.
        :return: List of vertices of the graph.
        """
        vertices = self._vertices.keys()
        vertices.sort()
        return vertices

    def get_edges(self):
        """
        Get all the edges of the directed graph.
        :return: List of edges of the graph.
        """
        edges = []
        for vertex in self._vertices:
            neighbors = self._vertices[vertex].get_connections()
            for neighbor in neighbors:
                edges.append((vertex, neighbor[0].get_key(), self._vertices[vertex].get_weight(neighbor[0].get_key())))

        return edges

    def get_vertex(self, vertex_key):
        for vertex in self._vertices:
            if vertex == vertex_key:
                return self._vertices[vertex]

        return None

    def BFS(self, start_vertex):
        start_vertex = self.get_vertex(start_vertex)

        if start_vertex is None:
            raise Exception("Vertex {} is not found in graph".format(start_vertex))

        visited = [False] * len(self._vertices)
        traversed = []

        q = Queue()
        q.enqueue(start_vertex)

        while not q.isEmpty():
            v = q.dequeue()
            key = v.get_key()

            if not visited[key]:
                visited[key] = True
                traversed.append(key)

                for neighbor in v.get_connections():
                    if not visited[neighbor[0].get_key()]:
                        q.enqueue(neighbor[0])

        return traversed

    def dfs_topological_sort(self, start_vertex_key, visited, sorted):
        start_vertex = self.get_vertex(start_vertex_key)

        # Set that the vertex is visited.
        visited[start_vertex_key] = True
        for neighbor in start_vertex.get_connections():
            # For each unvisited neighbor of the vertex, recursively call the DFS.
            if not visited[neighbor[0].get_key()]:
                self.dfs_topological_sort(neighbor[0].get_key(), visited, sorted)

        # When there are no more nodes unvisited nodes to traverse from the current vertex,
        # push it onto the sorted stack.
        sorted.push(start_vertex_key)

    def topological_sort(self, start_vertex_key):
        # Visit only unvisited nodes.
        visited = [False] * len(g.get_vertices())

        # The stack that holds the topological sort.
        sorted = Stack()

        # Call the modified version of the DFS.
        self.dfs_topological_sort(start_vertex_key, visited, sorted)

        # pop into a list till the stack is empty to get the topological sort.
        topo_sort = []
        while not sorted.isEmpty():
            topo_sort.append(sorted.pop())

        return topo_sort


if __name__ == "__main__":

    """
    graph = {
        "0" : [("1", 5), ("2", 3)],
        "1" : [("3", 3)],
        "2" : [("1", 2), ("3", 5), ("4", 6)],
        "3" : [],
        "4" : ["3", 1]
    }
    """

    g = Graph()

    for v in range(5):
        g.add_vertex(v)

    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 3)
    g.add_edge(2, 1, 2)
    g.add_edge(2, 3, 5)
    g.add_edge(2, 4, 6)
    g.add_edge(4, 3, 1)

    print("DFS:The nodes traversed from {} are: {}".format(0, g.topological_sort(0)))
