from __future__ import annotations

import layer_store
from data_structures import referential_array


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style: str, x: int, y: int) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        # initialised an array of length x and assigned to grid
        self.grid = referential_array.ArrayR(self.x)

        # for length of x, creating arrays of length y to create grid, can be accessed using grid[x][y]
        for i in range(self.x):
            self.grid[i] = referential_array.ArrayR(self.y)

        # looping through all of the grid and creating LayerStore() instances
        for i in range(self.x):
            for j in range(self.y):
                if self.draw_style == Grid.DRAW_STYLE_OPTIONS[0]:
                    self.grid[i][j] = layer_store.SetLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_OPTIONS[1]:
                    self.grid[i][j] = layer_store.AdditiveLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_OPTIONS[2]:
                    self.grid[i][j] = layer_store.SequenceLayerStore()

    def __getitem__(self, index: int) -> referential_array.ArrayR:
        return self.grid[index]

    def __setitem__(self, index: int, value: referential_array.ArrayR) -> None:
        self.grid[index] = value

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size == Grid.MAX_BRUSH:
            pass
        else:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size == Grid.MIN_BRUSH:
            pass
        else:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()



