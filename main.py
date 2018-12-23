import numpy as np
import pygame as pygame
import copy as copy
# Conway game of life rules.
from collections import OrderedDict

info = {
    'window_size': (500, 500),
    'grid_size': 100,
    'background': (50, 50, 50),
    'live_colour': (255, 255, 255),
}



class grid:

    def __init__(self, x, y):
        nx, ny = (x, y)
        x = np.repeat(0, nx)
        y = np.repeat(0, ny)
        self.grid, yv = np.meshgrid(x, y)
        self._initial_state()

    def _initial_state(self):
        self.set_coords(2, 0, 1)
        self.set_coords(2, 1, 1)
        self.set_coords(2, 2, 1)
        self.set_coords(0, 1, 1)
        self.set_coords(1, 2, 1)
        # for x in range(0, self.grid.shape[0]):
        #     for y in range(0, self.grid.shape[1]):
        #         r = np.random.randint(0, 2, 10)
        #         val = 1 if sum(r) > 7 else 0
        #         self.set_coords(x, y, val)

    def __call__(self, *args, **kwargs):
        return copy.deepcopy(self)

    def __repr__(self):
        return str(self.grid)

    def __str__(self):
        return self.__repr__()

    def get_offset(self, x, y, x_o, y_o):
        return self.get_coords(x+x_o, y+y_o)

    def get_coords(self, x, y):
        # Out of bound cells are dead.
        # if x not in list(range(0, self.grid.shape[0]-1)):
        #     return 0
        # if y not in list(range(0, self.grid.shape[1]-1)):
        #     return 0
        return self.grid[abs(x-(self.grid.shape[0]-1))][abs(y-(self.grid.shape[1]-1))]

    def set_coords(self, x, y, value):
        if value not in (0, 1):
            raise AssertionError("A cell must be a 0 or 1 state")
        if (x < 0 or y < 0):
            raise ValueError("You can't set a cell out of gridspace")
        self.grid[x][y] = value


class ConwaysGameofLife:

    rules = OrderedDict(
        {1: {0: 0, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
         0: {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}})

    neighborhood = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1),
                    (1, -1), (-1, -1)]

    def __init__(self, grid):
        self.grid = grid

    def get_moore_neighborhood(self, board, x, y):
        return [board.get_offset(x, y, *m) for m in self.neighborhood]

    def _check_state(self, board, x, y):
        moore = self.get_moore_neighborhood(board, x, y)
        doa = board.get_coords(x, y)
        return self.rules[doa][sum(moore)]

    def update_state(self, board, x, y, state):
        """Update value of grid based on state of cell"""
        board.set_coords(x, y, state)

    def iterate(self):
        board = self.grid()
        self.grid = self.simulate(board)
        return self

    def simulate(self, board):
        new_board = board()
        for x in range(0, board.grid.shape[0]):
            for y in range(0, board.grid.shape[1]):
                state = self._check_state(board, x, y)
                self.update_state(new_board, x, y, state)
        return new_board

# Iterate:
cgl = ConwaysGameofLife(grid(120, 60))
pygame.init()
display = pygame.display.set_mode((480, 320))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    n = cgl.iterate()
    res = (480, 320)
    surfarray = pygame.surfarray.make_surface(n.grid.grid)
    disp = pygame.transform.scale(surfarray, res)
    display.blit(disp, (0, 0))
    pygame.display.update()
pygame.quit()



