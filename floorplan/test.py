from .floorplan import Floorplan, FloorplanModule
from base.point import Point2D
from .constrain_graph_pair import ConstrainGraphPair


def init_floorplan():
    floorplan = Floorplan()
    floorplan.add_module(FloorplanModule("c", Point2D(0, 0), 2, 3))
    floorplan.add_module(FloorplanModule("d", Point2D(2, 0), 2, 3))
    floorplan.add_module(FloorplanModule("a", Point2D(0, 3), 4, 2))
    floorplan.add_module(FloorplanModule("e", Point2D(4, 0), 2, 4))
    floorplan.add_module(FloorplanModule("b", Point2D(4, 4), 2, 2))
    floorplan.status = True
    for module in floorplan.modules:
        module.initialize()
    return floorplan


def TEST_CGP():
    floorplan = init_floorplan()
    cgp = ConstrainGraphPair(floorplan)
    cgp.print()
