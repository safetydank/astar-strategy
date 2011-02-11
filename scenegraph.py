import ntree

class StemSG(object):
    def __init__(self, name):
        self.name = name

    def predraw(self):
        # return True if node doesn't require drawing
        return True

    def draw(self):
        raise Exception("Stem draw() should never be called")

    def postdraw(self):
        pass

class Scenegraph(object):
    """A basic 2D scenegraph.  A scenegraph node supports the following interface:
    
    predraw()  - push transform(s) onto matrix stack and any other predraw operation
    draw()     - draw object in local space
    postdraw() - pop transform(s) from matrix stack
    
    """

    def __init__(self):
        self.tree = ntree.NTree()

    def stem(self, name):
        """Create a new named stem node in the scenegraph"""
        return self.tree.append(StemSG(name))

    def node(self, data):
        """Create a scenegraph node from an object"""
        node = ntree.NTreeNode(data)
        data.node = node
        return node

    def draw(self):
        for node in self.tree.pushpop_iter(pop_cb=lambda n: n.parent.data.postdraw()):
            if not node.data.predraw():
                node.data.draw()

            if not node.first_child:
                node.data.postdraw()

