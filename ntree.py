class NTreeNode(object):
    def __init__(self, data=None):
        self.reset()
        self.data = data

    def reset(self):
        """Reset this node's connections to None"""
        self.parent = None
        self.next = None
        self.prev = None
        self.first_child = None
        self.last_child = None

    @property
    def has_children(self):
        return self.first_child is not None

    @property
    def children(self):
        c = []
        node = self.first_child
        while node:
            c.append(node)
            node = node.next
        return c

    def append_child(self, node):
        """Add a node as a child of this one"""
        node.parent = self

        if self.last_child:
            node.prev = self.last_child
            node.prev.next = node
            self.last_child = node

        if not self.first_child:
            self.first_child = node
            self.last_child = node

        return self

    def append(self, node):
        """Add a node after this one"""

        node.parent = self.parent;
        if node.parent and node.parent.last_child is self:
            node.parent.last_child = node

        node.prev = self
        if self.next:
            node.next = self.next
            node.next.prev = node

        self.next = node

    def excise(self):
        """Cleanly remove a node from its connected nodes"""

        parent = self.parent

        if self.prev:
            self.prev.next = self.next
            if self.next:
                self.next.prev = self.prev
        elif self.next:
            self.next.prev = None
        
        if self.parent and self.parent.last_child is self:
            self.parent.last_child = self.prev

        if self.parent and self.parent.first_child is self:
            self.parent.first_child = self.next

        self.reset()

    def __iter__(self):
        if not self.next:
            raise Exception("Node must be connected to other nodes to iterate")

        return NTreeIterator(self, self.next)

def node_forward(node, push_cb=None, pop_cb=None):
    """Return the next node after the given one, traversing tree depth-first"""

    next = None
    if node.first_child:
        if push_cb:
            push_cb(node)
        next = node.first_child
    elif node.next:
        next = node.next
    else:
        #  Move back up to parent
        while node.parent:
            if pop_cb:
                pop_cb(node)
            node = node.parent
            if node.next:
                next = node.next
                break
    return next

def node_back(node):
    """Return the previous node before the given one, traversing tree 
    depth-first"""

    next = None
    if node.prev:
        next = node.prev
        while node.last_child:
            next = node.last_child
    elif node.parent:
        next = node.parent;
    return next

class NTreeIterator(object):
    def __init__(self, begin, end, push_cb=None, pop_cb=None):
        self.node = None
        self.begin = begin
        self.end = end
        self.push_cb = push_cb
        self.pop_cb = pop_cb

    def __iter__(self):
        return self

    def next(self):
        if self.node:
            self.node = node_forward(self.node, 
                                     self.push_cb, self.pop_cb)
            if self.node is self.end:
                raise StopIteration
        else:
            self.node = self.begin

        return self.node

class NTree(object):
    def __init__(self):
        self._head = NTreeNode()
        self._tail = NTreeNode()
        self._head.append(self._tail)

    def begin(self):
        return self._head.next

    def end(self):
        return self._tail

    def append(self, data):
        """Add a node to the end of the tree at the root level"""
        node = NTreeNode(data)
        self._tail.prev.append(node)
        return node

    def append_child(self, parent_node, child_data):
        child_node = NTreeNode(data)
        parent_node.append(child_data)
        return child_node

    def find_one(self, data):
        for n in self:
            if n.data == data:
                return n
        else:
            return None

    def find(self, data):
        return [ n for n in self if n.data == data ]

    def __iter__(self):
        """Return a depth-first iterator covering the entire tree"""
        return NTreeIterator(self.begin(), self.end())

    def pushpop_iter(self, push_cb=None, pop_cb=None):
        """Return a depth-first iterator initialized with a push and pop 
           callback.  These are called when the iterator's tree depth
           changes."""
        return NTreeIterator(self.begin(), self.end(), push_cb, pop_cb)

