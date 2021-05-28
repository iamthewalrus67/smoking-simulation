import random
from random import random

EMPTY_CELL = None


class Person:
    def __init__(self, position: tuple, age: int, smoker: bool, chances_to_start: float, chances_to_stop: float,
                 chances_to_die: float, smoking_period: int, smoking_parents: int):
        self.position = position
        self.age = age
        self.smoking_parents = smoking_parents
        self.smoker = smoker
        self.chances_to_start_smoking = chances_to_start
        self.chances_to_stop_smoking = chances_to_stop
        self.chances_to_die = chances_to_die
        self.smoking_period = smoking_period

        self.state = None

    def influence_weight(self):
        if self.age < 15:
            return 2
        if 15 < self.age < 25:
            return 1.75
        if self.age < 55:
            return 1.5
        if self.age < 65:
            return 1.25
        return 1

    def check_neighbors(self, grid):
        x, y = self.position
        smokers = 0
        nonsmokers = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if grid[i, j].smoker == True:
                    smokers += 1
                else:
                    nonsmokers += 1
        return smokers, nonsmokers

    def chances_to_die(self):
        weight_of_age = None
        weight_of_smoking_period = 0.05

        chances = self.smoking_period * weight_of_smoking_period
        return chances

    def chances_to_start(self, grid):
        weight_of_smoking_parents = 0.1

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_smokers = smokers / (smokers+nonsmokers)
        chances = percent_of_smokers * self.influence_weight() + self.smoking_parents * \
            weight_of_smoking_parents
        return min(chances, 1)

    def chances_to_stop(self, grid):
        weight_of_smoking_period = 0.05

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_nonsmokers = nonsmokers / (smokers+nonsmokers)
        chances = percent_of_nonsmokers - self.smoking_period * weight_of_smoking_period
        return max(chances, 0)

    def check_death(self, grid):
        random_death = random()
        if random_death <= self.chances_to_die:
            x, y = self.position
            grid[x, y] = EMPTY_CELL

    def move(self, grid):
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                      (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        while True:
            random_direction = random.choice(directions)
            new_x = self.position[0] + random_direction[0]
            new_y = self.position[1] + random_direction[1]
            new_position = (new_x, new_y)
            if grid.is_occupied(new_position) or new_x not in range(grid.size[0]) or new_y not in range(grid.size[1]):
                continue

            grid.filled_cells.pop(self.position)
            self.position = new_position
            grid.filled_cells[self.position] = self


class Grid:
    def __init__(self, size: tuple):
        self.size = size
        self.filled_cells: dict = {}

    def fill_grid(self, position, value):
        if position in self.filled_cells.keys():
            raise IndexError
        self.filled_cells[position] = value

    def is_occupied(self, position):
        return self.filled_cells[position] is not None

    def next_iteration(self):
        for position in self.filled_cells.keys():
            self.filled_cells[position].move(self)


def random_start(grid=None, percent_of_people=0.01, children=0.15, teen=0.1, young=0.44, adult=0.14, elderly=0.17):
    if not grid:
        grid = Grid((50, 50))
    size = grid.size
    people_count = size[0]*size[1]*percent_of_people

    children = round(people_count*children)
    teen = round(people_count*teen)
    young = round(people_count*young)
    adult = round(people_count*adult)
    elderly = round(people_count*elderly)
