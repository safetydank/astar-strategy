import astar
import grid

class MapState(object):
    def __init__(self, map, face):
        self.map = map
        self.face = face

    def estimate_cost(self, goal):
        (u,v), (gu,gv) = self.face, goal.face
        return max(abs(u - gu), abs(v - gv))

    def __eq__(self, other):
        (u,v), (ou,ov) = self.face, other.face
        return u == ou and v == ov

    def successors(self):
        succ = [ self.map.map_state(n) 
                 for n in grid.neighbours2(self.face)
                 if self.map.valid_face(n) ]
        return [ (s, self.map.cost(s.face)) for s in succ ]

    def rep(self):
        (u,v) = self.face
        return "(%d,%d)" % (u, v)

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def map_state(self, face):
        return MapState(self, face)

    def valid_face(self, (u, v)):
        return u >= 1 and u <= self.width \
               and v >= 1 and v <= self.height

    def cost(self, face):
        (u, v) = face
        if u == 5 or (u == 4 and v == 3):
            return 10
        elif u == 6 and v == 3:
            return 20

        return 1

if __name__ == '__main__':
    search = astar.AStar()

    map = Map(10, 10)
    
    start = map.map_state((2, 3))
    goal  = map.map_state((8, 3))

    search.initialize(start, goal)
    result = { True  : "succeeded",
               False : "failed" }[search.search()]
    print "Completed search in %d steps : %s" % (search.steps, result)

    solution = search.get_solution()
    for (i, node) in enumerate(solution):
        print "%3d.  At %s" % (i+1, node.state.rep())

