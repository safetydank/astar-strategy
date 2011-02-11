import pyglet
import traceback

from pyglet import window, clock
from pyglet.gl import *

import gamemap
import scenegraph
import gui
import player

class StrategyWindow(window.Window):
    def __init__(self, **kwargs):
        kwargs.update(dict(caption = 'Strategy prototype',
                        width = 1024,
                        height = 768))
        super(StrategyWindow, self).__init__(**kwargs)

        self.game = Game(self)

    def draw(self):
        glLoadIdentity()
        glClearColor(0.22, 0.03, 0.03, 1.0)
        self.clear()

        #  Draw scenegraph
        self.game.graph.draw()

    def loop(self):
        try:
            clock.tick()

            while not self.has_exit:
                self.dispatch_events()
                dt = clock.tick()
                self.game.update(dt)
                self.draw()
                self.flip()

        except Exception, e:
            print "Error", e
            traceback.print_exc()
            self.close()

class Game(object):
    def __init__(self, window):
        self.map = gamemap.Map(width=20, height=15)
        self.start = None
        self.end = None

        self.graph = scenegraph.Scenegraph()

        # Map stem
        self.stem = self.graph.stem('map')
        self.stem.append(self.graph.node(self.map.sgdata))

        player1 = player.Player('Player 1', self.map)
        player2 = player.Player('Player 2', self.map)

        self.players = []
        self.players.append(player1)
        self.players.append(player2)

        self.handlers = GameEventHandlers(self)
        window.push_handlers(self.handlers)

        self.gui = gui.GuiManager(self, self.graph)
        self.gui.push_textbox(20, 20, 30, 40)
        window.push_handlers(self.gui.handlers)

    def update(self, dt):
        pass

class GameEventHandlers(object):
    def __init__(self, game):
        self.game = game

    def on_mouse_press(self, x, y, button, modifiers):
        game = self.game

        tile = game.map.hit_test(x, y)

        if tile and not game.start:
            game.start = tile
            game.map.colored_faces.append(tile)
        elif tile and not game.end:
            game.end = tile
            game.map.colored_faces.append(tile)
            solution = game.map.find_path(game.start, game.end)

            for node in solution:
                game.map.colored_faces.append(node.state.face)

            # highlight searched nodes
            for node in game.map.pathfinder._closed:
                game.map.closed_faces.append(node.state.face)
        elif game.start and game.end:
            game.start = None
            game.end = None
            game.map.colored_faces = []
            game.map.closed_faces = []

if __name__ == '__main__':
    w = StrategyWindow()
    w.loop()

