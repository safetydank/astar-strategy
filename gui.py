import scenegraph

from pyglet.gl import *
import ntree

# A basic overlay GUI module

class Rectangle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y):
        return self.x <= x < (self.x + self.width) and self.y <= y < (self.y + self.height)

    def intersect(self, rect):
        corners = ( (rect.x, rect.y), 
                    (rect.x, rect.y + rect.height),
                    (rect.x + rect.width, rect.y + rect.height),
                    (rect.x + rect.width, rect.y) )
        return any(self.contains(*c) for c in corners)

class GuiEventHandlers(object):
    def __init__(self, manager):
        self.manager = manager

    def on_mouse_press(self, x, y, button, modifiers):
        for element in (n.data for n in self.manager.stem if n is not self.manager.stem):
            if element.bounding_rect().contains(x, y):
                element.on_mouse_press(x, y, button, modifiers)
                return True

class GuiManager(object):
    """Handles creating GUI elements and handling input"""
    def __init__(self, window, graph):
        self.window = window
        self.graph = graph
        self.stem = graph.stem('GUI')
        self.handlers = GuiEventHandlers(self)

    # self.graph.node will set a data member "node"
    def push_textbox(self, x, y, w, h):
        textbox = self.graph.node(TextBox(Rectangle(x, y, w, h)))
        self.stem.append_child(textbox)

def draw_box(width, height, color=None):
    """Draw a filled box with an optional (r,g,b,a) color"""

    if color:
        glColor4f(*color)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    glVertex2f(0, height)
    glVertex2f(width, height)
    glVertex2f(width, 0)
    glEnd()

class TextBox(object):
    def __init__(self, rect, color=(0,0,1,1)):
        self.rect = rect
        self.color = color

    def bounding_rect(self):
        return self.rect

    def predraw(self):
        glPushMatrix()
        glTranslatef(self.rect.x, self.rect.y, 0)

    def draw(self):
        draw_box(self.rect.width, self.rect.height, (1,1,0,1))

    def postdraw(self):
        glPopMatrix()

    def on_mouse_press(self, x, y, button, modifiers):
        self.node.excise()

class Button(object):
    pass

