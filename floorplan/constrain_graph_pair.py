from base.graph import DirectedGraph
from .floorplan import Floorplan


class ConstrainGraphPair:
    def __init__(self, floorplan: Floorplan):
        self.vcg = DirectedGraph()
        self.hcg = DirectedGraph()

        self.hcg.add_vertex("s", 0)
        self.hcg.add_vertex("t", 0)

    def create_vcg(self, floorplan: Floorplan):
        self.vcg.add_vertex("s", 0)
        self.vcg.add_vertex("t", 0)
        for module in floorplan.modules:
            self.vcg.add_vertex(module.name)
            # self.vcg.add_edge("s", module.name)
            # self.vcg.add_edge(module.name, "t")

    def create_hcg(self, floorplan: Floorplan):
        pass
