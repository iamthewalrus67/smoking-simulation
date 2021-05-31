import matplotlib.pylab as plt
import seaborn as sns
from random import random, randrange, randint, choice
import numpy as np
np.set_printoptions(threshold=np.inf)
EMPTY_CELL = None


# from finite_state_machine import FiniteStateMachine


class Person:
    def __init__(self, age: int, smoker: bool, smoking_parents: float, smoking_period: int = 0, position: tuple = None):
        self.position = position
        self.age = age
        self.smoking_parents = smoking_parents
        self.smoker = smoker
        # self.chances_to_start_smoking = chances_to_start
        # self.chances_to_stop_smoking = chances_to_stop
        # self.chances_to_die = chances_to_die
        self.smoking_period = smoking_period

        self.state = None

    def influence_weight(self):
        if self.age < 16:
            return 1.5
        if 15 < self.age < 26:
            return 1.4
        if self.age < 46:
            return 1.3
        if self.age < 66:
            return 1.2
        return 1

    def get_person_age_type(self):
        if self.age < 16:
            return 'children'
        if self.age < 26:
            return 'teen'
        if self.age < 46:
            return 'young'
        if self.age < 66:
            return 'adult'
        return 'elderly'

    def check_neighbors(self, grid):
        x, y = self.position
        smokers = 0
        nonsmokers = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i, j) in grid.filled_cells:
                    if grid.filled_cells[(i, j)].smoker == True:
                        smokers += 1
                    else:
                        nonsmokers += 1
        return smokers, nonsmokers

    def chances_to_die(self):
        chances = 0.03

        weight_of_smoking_period = 0.01
        weight_of_smoking_period_pro = 0.02
        if self.smoking_period:
            if self.smoking_period <= 10:
                chances = self.smoking_period * weight_of_smoking_period
            else:
                chances = 10 * weight_of_smoking_period + \
                    (self.smoking_period - 10) * weight_of_smoking_period_pro
        return chances

    def chances_to_start_smoking(self, grid):
        if self.smoking_parents:
            weight_of_smoking_parents = 2
        else:
            weight_of_smoking_parents = 1

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_smokers = smokers / (smokers+nonsmokers)
        chances = percent_of_smokers * self.influence_weight() * weight_of_smoking_parents
        return min(chances, 1)

    def chances_to_stop_smoking(self, grid):
        weight_of_smoking_period = 0.05

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_nonsmokers = nonsmokers / (smokers+nonsmokers)
        chances = percent_of_nonsmokers * \
            (1 - self.smoking_period * weight_of_smoking_period)
        # chances = percent_of_nonsmokers - self.smoking_period * weight_of_smoking_period
        return max(chances, 0)

    def check_death(self, grid):
        random_death = random()
        if random_death <= self.chances_to_die() or self.age == 85:
            x, y = self.position
            grid.filled_cells.pop((x, y))
            return True
        return False

    def __str__(self):
        return f'Position: {self.position}, age: {self.age}, smoker: {self.smoker}, smoking_period: {self.smoking_period}, smoking_parents: {self.smoking_parents}, state: {self.state}'

    def move(self, grid):
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                      (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        while True:
            random_direction = choice(directions)
            new_x = self.position[0] + random_direction[0]
            new_y = self.position[1] + random_direction[1]
            new_position = (new_x, new_y)
            if new_position == self.position:
                break
            if grid.is_occupied(new_position) or new_x not in range(grid.size[0]) or new_y not in range(grid.size[1]):
                continue

            grid.filled_cells.pop(self.position)
            self.position = new_position
            grid.filled_cells[self.position] = self
            break


class Grid:
    def __init__(self, size: tuple, start_fill):
        self.size = size
        self.filled_cells: dict = {}
        self.start_fill = start_fill
        self.population_count = {'children': [0, 0],
                                 'teen': [0, 0],
                                 'young': [0, 0],
                                 'adult': [0, 0],
                                 'elderly': [0, 0]}

    def is_occupied(self, position):
        try:
            return isinstance(self.filled_cells[position], Person)
        except KeyError:
            return False

    def next_iteration(self, fsm):
        # print(self.to_matrix())

        for position in list(self.filled_cells.keys()):
            person = self.filled_cells[position]
            fsm.next(person)
        # print(self.population_count, self.get_total_population())
        # print(len(self.filled_cells))
        for position in list(self.filled_cells.keys()):
            self.filled_cells[position].move(self)

        self.create_children()

        #return self.to_matrix()


    def create_children(self):
        fertile_people = self.population_count['teen'][0] + self.population_count['young'][0]
        fertile_smokers = self.population_count['teen'][1] + self.population_count['young'][1]
        # print('adasdal sdasdk ahdslajh sdj a\n\n\n\n' + fertile_people)

        fertile_non_smokers = fertile_people - fertile_smokers
        if fertile_non_smokers > 0:
            children_born_from_non_smokers = max(
                1, round(fertile_non_smokers * 0.02))
        else:
            children_born_from_non_smokers = 0

        if fertile_smokers > 0:
            children_born_from_smokers = max(1, round(fertile_smokers * 0.01))
        else:
            children_born_from_smokers = 0

        for i in range(children_born_from_non_smokers):
            person = Person(age=0, smoker=False, smoking_parents=False)
            while self.get_free_cells_count():
                position = (
                    randint(0, self.size[0]-1), randint(0, self.size[1]-1))
                if position not in self.filled_cells:
                    # print('create child', position)
                    self.filled_cells[position] = person
                    # print('after creation', len(self.filled_cells))
                    person.position = position
                    person.state = 'nonsmoker_low_prob'
                    self.population_count['children'][0] += 1
                    break

        for i in range(children_born_from_smokers):
            person = Person(age=0, smoker=False, smoking_parents=True)
            while self.get_free_cells_count():
                position = (
                    randint(0, self.size[0]-1), randint(0, self.size[1]-1))
                if position not in self.filled_cells:
                    # print(position)
                    self.filled_cells[position] = person
                    # print(len(self.filled_cells))
                    person.position = position
                    person.state = 'nonsmoker_low_prob'
                    self.population_count['children'][0] += 1
                    break

    def get_total_population(self):
        total_population = 0
        for i in self.population_count:
            total_population += self.population_count[i][0]

        return total_population

    def get_free_cells_count(self):
        free_cells = self.size[0] * self.size[1] - self.get_total_population()
        return free_cells

    def random_start(self, children=0.16, teen=0.1, young=0.3, adult=0.27, elderly=0.17):
        people_count = int(self.size[0]*self.size[1]*self.start_fill)

        children_count = int(people_count*children)
        teen_count = int(people_count*teen)
        young_count = int(people_count*young)
        adult_count = int(people_count*adult)
        elderly_count = int(people_count*elderly)

        people = {'children': (children_count, [0, 15], 0),
                  'teen': (teen_count, [16, 25], 0.187),
                  'young': (young_count, [26, 45], 0.324),
                  'adult': (adult_count, [46, 65], 0.229),
                  'elderly': (elderly_count, [66, 85], 0.06)}
        # people = [children, teen, young, adult, elderly]

        for person_type in people:
            for i in range(people[person_type][0]):
                min_age, max_age = people[person_type][1]
                age = randrange(min_age, max_age)

                check_smoking = random()
                if check_smoking < people[person_type][2]:
                    smoker = True
                else:
                    smoker = False

                if smoker == True and age > 10:
                    smoking_period = randrange(age-10)
                else:
                    smoking_period = 0

                smoking_parents = choice([True, False])

                new_person = Person(
                    age=age, smoker=smoker, smoking_parents=smoking_parents, smoking_period=smoking_period)
                if smoker:
                    self.population_count[person_type][1] += 1

                while True:
                    position = (
                        randint(0, self.size[0]-1), randint(0, self.size[1]-1))
                    if position not in self.filled_cells:
                        self.filled_cells[position] = new_person
                        new_person.position = position
                        break
            self.population_count[person_type][0] = people[person_type][0]

        for position in self.filled_cells:
            person = self.filled_cells[position]
            if person.smoker == True:
                if person.smoking_period >= 5:
                    person.state = 'smoker_pro'
                else:
                    person.state = 'smoker_beginner'
            else:
                if person.chances_to_start_smoking(self) > 0.5:
                    person.state = 'nonsmoker_high_prob'
                else:
                    person.state = 'nonsmoker_low_prob'
        
        print(self.population_count, self.get_total_population())
        print(len(self.filled_cells))

    def to_matrix(self):
        states = {'dead': 0,
                    'smoker_in_the_past': 1,
                    'smoker_pro': 2,
                    'smoker_beginner': 3,
                    'nonsmoker_high_prob': 4,
                    'nonsmoker_low_prob': 5
                    }
        # states = {'dead': ' ',
        #           'nonsmoker_low_prob': '💛',
        #           'nonsmoker_high_prob': '🧡',
        #           'smoker_beginner': '❤️',
        #           'smoker_pro': '💜',
        #           'smoker_in_the_past': '💙'}
        matrix = np.zeros(shape=(self.size[0], self.size[1]))

        # matrix = [[' ' for _ in range(self.size[0])]
        #           for _ in range(self.size[1])]
        # for position in self.filled_cells:
        #     x, y = position
        #     person = self.filled_cells[position]
        #     matrix[x][y] = states[person.state]
        # for i in matrix:
        #     print(i)
        # print()
        for position in self.filled_cells:
            x, y = position
            person = self.filled_cells[position]
            matrix[x, y] = states[person.state]

        return matrix
    
    def count_states(self):
        states_dict = {'dead': 0,
                    'smoker_in_the_past': 0,
                    'smoker_pro': 0,
                    'smoker_beginner': 0,
                    'nonsmoker_high_prob': 0,
                    'nonsmoker_low_prob': 0}
        for person in self.filled_cells.values():
            states_dict[person.state] += 1
        return list(states_dict.values())

# grid = Grid((50, 50))
# grid.random_start()
# # for i in grid.filled_cells:
# #     print(grid.filled_cells[i])

# # print(grid.to_matrix())

# matrix = grid.to_matrix()


# uniform_data = np.random.rand(100, 100)
# plt.figure("Smokers world")
# ax = sns.heatmap(matrix, linewidth=0.5, cmap=[
#                  "#ffffff", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b", ])
# plt.show()
