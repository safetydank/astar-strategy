import astar
import grid
import math
import ntree

from pyglet.gl import *

class MapState(object):
    def __init__(self, map, face):
        self.map = map
        self.face = face

    def estimate_cost(self, goal):
        (u,v), (gu,gv) = self.face, goal.face
        return max(abs(u - gu), abs(v - gv))

    def __eq__(self, other):
        return self.face == other.face

    def successors(self):
        (fu, fv) = self.face
        dist = lambda (u,v): math.sqrt((fu-u)*(fu-u) + (fv-v)*(fv-v))
        succ = [ self.map.map_state(n) 
                 for n in grid.neighbours2(self.face)
                 if self.map.valid_face(n) ]
        return [ (s, self.map.cost(s.face) * dist(s.face)) for s in succ ]

    def __repr__(self):
        (u,v) = self.face
        return "(%d,%d)" % (u, v)

TILE_SIZE = 40
class MapSG(object):
    """Map scenegraph node"""

    def __init__(self, map):
        self.map = map
        self.zoom = 1
        self.origin = (80, 60)

    def predraw(self):
        glPushMatrix()

    def draw(self):
        (ox, oy) = self.origin
        map = self.map

        # Draw grid
        glPushAttrib(GL_CURRENT_BIT)
        glColor3f(1, 1, 1)

        for tile in self.map.tiles.values():
            self.draw_tile(tile)

        glPopAttrib()

        for i in range(0, self.map.width):
            for j in range(0, self.map.height):
                if self.map.cost((i,j)) != 1:
                    self.color_face((0,0,0,1), (i,j))

        for face in map.closed_faces:
            self.color_face((1,1,0,0.6), face)

        for face in map.colored_faces:
            self.color_face((0,0.75,0,1), face)

    def postdraw(self):
        glPopMatrix()

    def draw_tile(self, tile):
        (ox, oy) = self.origin
        x, y = tile.x, tile.y

        glBegin(GL_LINE_LOOP)
        glVertex2f(ox + x * TILE_SIZE, oy + y * TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE, oy + y * TILE_SIZE + TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE + TILE_SIZE, oy + y * TILE_SIZE + TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE + TILE_SIZE, oy + y * TILE_SIZE)
        glEnd()
        
    def color_face(self, color, (x, y)):
        (ox, oy) = self.origin
        (r, g, b, a) = color

        glColor4f(r, g, b, a)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(ox + x * TILE_SIZE, oy + y * TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE, oy + y * TILE_SIZE + TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE + TILE_SIZE, oy + y * TILE_SIZE + TILE_SIZE)
        glVertex2f(ox + x * TILE_SIZE + TILE_SIZE, oy + y * TILE_SIZE)
        glEnd()

    def hit_test(self, x, y):
        (ox, oy) = self.origin
        gx, gy = (x - ox) // TILE_SIZE, (y - oy) // TILE_SIZE
        if 0 <= gx < self.map.width and 0 <= gy < self.map.height:
            return (gx, gy)

        return None

class MapTile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pathfinder = astar.AStar()

        # Reference to the map's scene graph node
        self.sgdata = MapSG(self)

        self.tiles = {}
        for x in range(0, width):
            for y in range(0, height):
                self.tiles[(x,y)] = MapTile(x,y)

        # XXX temporary
        self.colored_faces = []
        self.closed_faces = []

    def __getitem__(self, key):
        return self.tiles[key]
        
    def map_state(self, face):
        return MapState(self, face)

    def find_path(self, start, goal):
        """Given start and goal co-ords return a solved node path or None"""
        self.pathfinder.initialize(self.map_state(start), self.map_state(goal))
        result = self.pathfinder.search()
        return self.pathfinder.get_solution() if result else None

    def valid_face(self, (u, v)):
        return 0 <= u < self.width and 0 <= v < self.height

    def cost(self, face):
        (u, v) = face
        
        # Mark an expensive block of the map
        if 5 <= u <= 10 and 5 <= v <= 10:
            return 5

        return 1

    def hit_test(self, x, y):
        return self.sgdata.hit_test(x,y)

if __name__ == '__main__':
    search = astar.AStar()

    map = Map(10, 10)
    
    start = map.map_state((2, 3))
    goal  = map.map_state((8, 3))

    search.initialize(start, goal)
    result = { True  : 'succeeded',
               False : 'failed' }[search.search()]
    print 'Completed search in %d steps : %s' % (search.steps, result)

    solution = search.get_solution()
    for (i, node) in enumerate(solution):
        print '%3d.  At %s' % (i+1, node.state)

