class Graph:
    def __init__(self):
        self.nodes = {}

    def init_wrapper(outerself, init):
        def wrapper(self, label, *args):
            init(self, label, *args)
            outerself.nodes[self.label] = self
        return wrapper

    def connect_wrapper(outerself, connect):
        def wrapper(self, other_label):
            connect(self, outerself.nodes[other_label])
        return wrapper

    def __getitem__(self, key):
        return self.nodes[key]

    def node_class(self):
        class _Node:
            @self.init_wrapper
            def __init__(self, label, flow_rate):
                self.label = label
                self.connections = set()
                self.flow_rate = flow_rate

            @self.connect_wrapper
            def connect(self, node):
                self.connections.add(node)
                node.connections.add(self)

            def __repr__(self):
                return f"Node {self.label}: FR: {self.flow_rate}, CN: ({','.join(c.label for c in self.connections)})"
        return _Node



graph = Graph()

Node = graph.node_class()


PROD = False

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

connection_queue = []
for line in lines:
    label = line.split(" ",2)[1]
    rate = int(line.split("=")[1].split(";")[0])
    conn = line.split("valve")[1]
    conn = conn[conn.index(" ")+1:].split(", ")
    connection_queue.append((label, conn))
    Node(label, rate)

[[graph[label].connect(c) for c in conn]  for label,conn in connection_queue]

print(graph["AA"].connections)