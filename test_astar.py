import astar

class MapState(object):
    def __init__(self):
        pass

GOAL = 22

class TrivialState(object):
    def __init__(self, at):
        self.at = at

    def estimate_cost(self, goal):
        return abs(goal.at - self.at)

    def __eq__(self, other):
        return (self.at == other.at)

    def successors(self):
        succ = [ TrivialState(self.at - 1), TrivialState(self.at + 1) ]
        return [ (s, 1) for s in succ ]

if __name__ == '__main__':
    search = astar.AStar()
    
    start = TrivialState(7)
    goal  = TrivialState(GOAL)
    search.initialize(start, goal)
    result = { True  : "succeeded",
               False : "failed" }[search.search()]
    print "Completed search in %d steps : %s" % (search.steps, result)

    solution = search.get_solution()
    for (i, node) in enumerate(solution):
        print "%3d.  At %d" % (i+1, node.state.at)

