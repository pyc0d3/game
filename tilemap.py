import pygame as pg
import dungeon_generator
from settings import *
from sprites import *
from collections import deque
import heapq


class SquareGrid:
    def __init__(self, game, size):
        self.game = game
        self.width, self.height = size
        self.walls = [wall.gridpos for wall in self.game.walls]
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # comment/uncomment this for diagonals:
        # self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors


class WeightedGrid(SquareGrid):
    def __init__(self, game, size):
        super().__init__(game, size)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def heuristic(self, a, b):
        # return abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2
        return (abs(a.x - b.x) + abs(a.y - b.y)) * 10

    def find_shortest_path(self, start, end):
        if start in self.walls:
            return deque()
        frontier = PriorityQueue()
        frontier.put(vec2int(start), 0)
        path = {}
        cost = {}
        path[vec2int(start)] = None
        cost[vec2int(start)] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == end:
                break
            for next in self.find_neighbors(vec(current)):
                next = vec2int(next)
                next_cost = cost[current] + self.cost(current, next)
                if next not in cost or next_cost < cost[next]:
                    cost[next] = next_cost
                    priority = next_cost + self.heuristic(end, vec(next))
                    frontier.put(next, priority)
                    path[next] = vec(current) - vec(next)

        current = end
        shortest_path = []
        while current != start:
            current = current + path[vec2int(current)]
            shortest_path.append(current)
        return deque(shortest_path)


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


class Map:
    def __init__(self, game):
        self.game = game
        gen = dungeon_generator.Generator()
        gen.gen_level()
        self.level = gen.level
        self.reachable_objects = ['floor', 'start_door', 'end_door', 'player']
        self.unreachable_objects = ['wall', 'stone']
        self.gridwidth = gen.width
        self.gridheight = gen.height
        self.width = self.gridwidth * TILESIZE
        self.height = self.gridheight * TILESIZE

    def load(self):
        for row in range(self.gridheight):
            for col in range(self.gridwidth):
                Floor(self.game, (col, row))

        for row in range(self.gridheight):
            for col in range(self.gridwidth):

                if self.level[row][col] == 'stone':
                    Wall(self.game, (col, row), 'mid')

                if self.level[row][col] == 'start_door':
                    Trapdoor(self.game, (col, row), False)
                    self.game.player = Player(self.game, (col, row))

                if self.level[row][col] == 'exit_door':
                    Trapdoor(self.game, (col, row), True)

        # set up all walls and rotate them
        for row in range(1, self.gridheight - 1):
            for col in range(1, self.gridwidth - 1):
                if self.level[row][col] == 'wall':

                    """if top == 'smth' and bottom == 'smth' and\
                            left == 'smth' and right == 'smth':
                    """
                    if self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'mid')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.unreachable_objects:
                        Wall(self.game, (col, row), 'up')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.unreachable_objects:
                        Wall(self.game, (col, row), 'down')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'left')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'right')
                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'up-left')
                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'up-right')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'down-left')
                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'down-right')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'solo_up')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'solo_down')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'solo_left')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'solo_right')

                    elif self.level[row - 1][col] in self.unreachable_objects and self.level[row + 1][col] in self.unreachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'solo_mid_ver')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.unreachable_objects and self.level[row][col + 1] in self.unreachable_objects:

                        Wall(self.game, (col, row), 'solo_mid_hor')

                    elif self.level[row - 1][col] in self.reachable_objects and self.level[row + 1][col] in self.reachable_objects and\
                            self.level[row][col - 1] in self.reachable_objects and self.level[row][col + 1] in self.reachable_objects:

                        Wall(self.game, (col, row), 'solo')


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.gridoffset = vec(0, 0)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH // 2)
        y = -target.rect.y + int(HEIGHT // 2)

        # ограничиваем прокрутку карты
        x = min(0, x)  # левая грань
        y = min(0, y)  # верхняя грань
        x = max(-(self.width - WIDTH), x)  # правая грань
        y = max(-(self.height - HEIGHT), y)  # нижняя грань

        self.camera = pg.Rect(x, y, self.width, self.height)

        self.gridoffset = get_gridpos(vec(self.camera.x, self.camera.y))
