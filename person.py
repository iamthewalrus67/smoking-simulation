from random import random, randrange, randint, choice

EMPTY_CELL = None


class Person:
    def __init__(self, age: int, smoker: bool, smoking_period: int, smoking_parents: float, position: tuple = None, 
    chances_to_start: float = None, chances_to_stop: float = None, chances_to_die: float = None,):
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

    def chances_to_start(self):
        weight_of_smoking_parents = 0.1

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_smokers = smokers / (smokers+nonsmokers)
        chances = percent_of_smokers * self.influence_weight() + self.smoking_parents * weight_of_smoking_parents
        return min(chances, 1)

    def chances_to_stop(self):
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
    
    def __str__(self):
        return f'Position: {self.position}, age: {self.age}, smoker: {self.smoker}, smoking_period: {self.smoking_period}, smoking_parents: {self.smoking_parents}'


class Grid:
    def __init__(self, size: tuple):
        self.size = size
        self.filled_cells: dict = {}

    def fill_grid(self, position, value):
        if position in self.filled_cells.keys:
            raise IndexError
        self.filled_cells[position] = value


    def random_start(self, percent_of_people = 0.01, children = 0.15, teen = 0.1, young = 0.44, adult = 0.14, elderly = 0.17):
        people_count = round(self.size[0]*self.size[1]*percent_of_people)

        children_count = round(people_count*children)
        teen_count = round(people_count*teen)
        young_count = round(people_count*young)
        adult_count = round(people_count*adult)
        elderly_count = round(people_count*elderly)
        
        people = {'children': (children_count, [0, 14], 0),
                    'teen': (teen_count, [15, 24], 0.187),
                    'young': (young_count, [25, 54], 0.324),
                    'adult': (adult_count, [55, 64], 0.229),
                    'elderly': (elderly_count, [65, 85], 0.06)}
        # people = [children, teen, young, adult, elderly]


        for person_type in people:
            for i in range(people[person_type][0]):
                min_age, max_age = people[person_type][1]
                age = randrange(min_age, max_age)

                check_smoking = random()
                if check_smoking <= people[person_type][2]:
                    smoker = True
                else:
                    smoker = False

                if smoker == True and age > 10:
                    smoking_period = randrange(age-10)
                else:
                    smoking_period = None
                
                smoking_parents = choice([True, False])

                new_person = Person(age=age, smoker=smoker, smoking_parents=smoking_parents, smoking_period=smoking_period)

                while True:
                    position = (randint(0, self.size[0]), randint(0, self.size[1]))
                    if position not in self.filled_cells:
                        self.filled_cells[position] = new_person
                        new_person.position = position
                        break
                    else:
                        position = (randint(0, self.size[0]), randint(0, self.size[1]))


grid = Grid((100, 100))
grid.random_start()
for i in grid.filled_cells:
    print(grid.filled_cells[i])