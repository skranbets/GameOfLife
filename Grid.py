class Grid:
    def __init__(self, grid_length):
        self.grid_size = grid_length
        col_list = [0 for i in range(self.grid_size)]
        self.grid_list = [col_list.copy() for j in range(self.grid_size)]
        self.box = int(900 / self.grid_size)

    def new_grid(self, grid):
        self.grid_size = len(grid)
        self.box = int(900 / self.grid_size)
        self.grid_list = grid



