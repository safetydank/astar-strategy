# Define a grid map
#
# A map is a square grid of faces.  
#
# See http://www-cs-students.stanford.edu/~amitp/game-programming/grids/ for
# addressing scheme

class Face(object):
    def __init__(self, (u, v)):
        self.u = u
        self.v = v

# edge orientation can be WEST or SOUTH from a vertex
W = 0
S = 1

class Edge(object):
    def __init__(self, (u, v, o)):
        """An edge is defined by u,v co-ordinates and o orientation (S|w)"""
        self.u = u
        self.v = v
        self.o = o

class Vertex(object):
    def __init__(self, (u, v)):
        """A vertex is defined by u,v co-ordinates"""
        self.u = u
        self.v = v

def neighbours((u,v)):
    """Return neighbouring face co-ordinates of a given face"""
    return ((u,v+1), (u+1,v), (u,v-1), (u-1,v))

def neighbours2((u,v)):
    """Return neighbouring face co-ordinates of a given face, including 
    diagonals"""

    return ((u-1, v+1), (u,v+1), (u+1,v+1), 
            (u-1,v), (u+1,v),
            (u-1,v-1), (u,v-1), (u+1,v-1))

def borders((u,v)):
    """Return border edge co-ords of a face"""
    return ((u,v+1,S), (u+1,v,W), (u,v,S), (u,v,W))

def corners((u,v)):
    """Return corner vertex coords of a face"""
    return ((u+1,v+1), (u+1,v), (u,v), (u,v+1))

def joins((u,v,o)):
    """Return adjoining faces of an edge"""
    return { W : ((u,v), (u-1,v)),
             S : ((u,v), (u,v-1)) }[o]

def continues((u,v,o)):
    """Return continuing edges of an edge"""
    return { W : ((u,v+1,W), (u,v-1,W)),
             S : ((u+1,v,S), (u-1,v,S)) }[o]

def endpoints((u,v,o)):
    """Return endpoint vertices of an edge"""
    return { W : ((u,v+1), (u,v)),
             S : ((u+1,v), (u,v)) }[o]

def touches((u,v)):
    """Return faces touching a given vertex"""
    return ((u,v), (u,v-1), (u-1,v-1), (u-1,v))

def protrudes((u,v)):
    """Return edges protruding (like a +) about a given vertex"""
    return ((u,v,W), (u,v,S), (u,v-1,W), (u-1,v,S))

def adjacent((u,v)):
    """Return adjacent vertices to a given vertex"""
    return ((u,v+1), (u+1,v), (u,v-1), (u-1,v))

class Grid(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.faces = {}
        for i in range(cols):
            for j in range(rows):
                self.faces[(i,j)] = Face(i,j)
    
    #  Items are accessed as Map[(u,v)]
    def __getitem__(self, key):
        return self.faces[key]

