from random import random, randrange, randint, choice
import numpy as np
from person import Person

np.set_printoptions(threshold=np.inf)


class Grid:
    """
    Represents the place where
    people live and contact with each other.

    Attributes:
        size - tuple with the length and width of the grid
        filled_cells - dict (keys are positions in format (x, y),
            values are objects of class Person)
        start_fill - float between 0 and 1 that means what part
            of the grid should be filled in the method
            random_start()
        population_count - dict (keys are strings with names of
            age groups, values are list with number of people
            in this age group and number of smokers from them)
        weight_of_smoking_parents - coefficient that represents in
            how many times the human chances to start smoking grow
            if his parents are smokers (2 if parents are smokers, 1
            in another case)
        weight_of_smoking_year_stop - coefficient that represents how
            harder for humans is to stop smoking with every
            new year of smoking
        chances_to_die - float between 0 and 1 that represents chances
            of every human to die
        weight_of_smoking_year_die - coefficient that represents how
            much every smoking year influences on cahnces to die
        fertile_percent_non_smokers - float between 0 and 1 that represents
            the percent of rates of birth from nonsmokers
        fertile_percent_smokers - float between 0 and 1 that represents
            the percent of rates of birth from smokers
        smokers_concentration - list where the first bool value is True if most
            of smokers are in the centre, the second one is True if most of
            smokers are on the side of the grid after calling method random_start().
            Both of values are False if start positions of smokers are absolutely random.

    """

    def __init__(self, size, start_fill, people_influence, weight_of_smoking_parents,
                 weight_of_smoking_year_stop, chances_to_die, weight_of_smoking_year_die,
                 fertile_percent_non_smokers, fertile_percent_smokers, smokers_concentration):
        self.size = size
        self.filled_cells: dict = {}
        self.start_fill = start_fill
        self.population_count = {'children': [0, 0],
                                 'teen': [0, 0],
                                 'young': [0, 0],
                                 'adult': [0, 0],
                                 'elderly': [0, 0]}
        self.people_influence = people_influence
        self.weight_of_smoking_parents = weight_of_smoking_parents
        self.weight_of_smoking_year_stop = weight_of_smoking_year_stop
        self.chances_to_die = chances_to_die
        self.weight_of_smoking_year_die = weight_of_smoking_year_die
        self.fertile_percent_non_smokers = fertile_percent_non_smokers
        self.fertile_percent_smokers = fertile_percent_smokers
        self.smokers_concentration = {'smokers_in_centre': smokers_concentration[0], \
                                      'smokers_on_side': smokers_concentration[1]}

    def is_occupied(self, position):
        """
        Return True if the cell with given position
        is occupied.
        """
        try:
            return isinstance(self.filled_cells[position], Person)
        except KeyError:
            return False

    def next_iteration(self, fsm):
        """
        Update the grid like after 1 year of life.
        """
        for position in list(self.filled_cells.keys()):
            person = self.filled_cells[position]
            fsm.next(person)
        for position in list(self.filled_cells.keys()):
            self.filled_cells[position].move(self)

        self.create_children()

    def create_children(self):
        """
        Create and add children to the grid depending on
        coefficients fertile_percent_non_smokers, fertile_percent_smokers
        and the number of people on the grid.
        """
        fertile_people = self.population_count['teen'][0] + \
                         self.population_count['young'][0]
        fertile_smokers = self.population_count['teen'][1] + \
                          self.population_count['young'][1]

        fertile_non_smokers = fertile_people - fertile_smokers
        # when the grid is small max(1, x) does not want correctly
        # so I deleted it
        if fertile_non_smokers > 0:
            children_born_from_non_smokers = max(randint(0, 1), \
                                                 round(fertile_non_smokers * self.fertile_percent_non_smokers))
        else:
            children_born_from_non_smokers = 0

        if fertile_smokers > 0:
            children_born_from_smokers = max(randint(0, 1), \
                                             round(fertile_smokers * self.fertile_percent_smokers))
        else:
            children_born_from_smokers = 0

        for i in range(children_born_from_non_smokers):
            person = Person(age=0, smoker=False, smoking_parents=False)
            while self.get_free_cells_count():
                position = (
                    randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))
                if position not in self.filled_cells:
                    self.filled_cells[position] = person
                    person.position = position
                    person.state = 'nonsmoker_low_prob'
                    self.population_count['children'][0] += 1
                    break

        for i in range(children_born_from_smokers):
            person = Person(age=0, smoker=False, smoking_parents=True)
            while self.get_free_cells_count():
                position = (
                    randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))
                if position not in self.filled_cells:
                    self.filled_cells[position] = person
                    person.position = position
                    person.state = 'nonsmoker_low_prob'
                    self.population_count['children'][0] += 1
                    break

    def get_total_population(self):
        """
        Return current number of people on
        the grid.
        """
        total_population = 0
        for i in self.population_count:
            total_population += self.population_count[i][0]

        return total_population

    def get_free_cells_count(self):
        """
        Return how many cells are free at
        the current moment.
        """
        free_cells = self.size[0] * self.size[1] - self.get_total_population()
        return free_cells

    def random_start(self, percent_people=[0.16, 0.1, 0.3, 0.27, 0.17],
                     percent_smokers=[0, 0.187, 0.324, 0.229, 0.06]):
        """
        Depending on some coefficients, statistical data and little part of random
        fills the grid with people.
            percent_people - list with percent of every age group in population
                that will be generated (in order: children, teen, young, adult, elderly)
            percent_smokers - list with percent of smokers in every age group
                (in the same order as the previous list)
        """
        smokers_in_centre = self.smokers_concentration['smokers_in_centre']
        smokers_on_side = self.smokers_concentration['smokers_on_side']

        people_count = int(self.size[0] * self.size[1] * self.start_fill)

        children_count = int(people_count * percent_people[0])
        teen_count = int(people_count * percent_people[1])
        young_count = int(people_count * percent_people[2])
        adult_count = int(people_count * percent_people[3])
        elderly_count = int(people_count * percent_people[4])

        people = {'children': (children_count, [0, 15], percent_smokers[0]),
                  'teen': (teen_count, [16, 25], percent_smokers[1]),
                  'young': (young_count, [26, 45], percent_smokers[2]),
                  'adult': (adult_count, [46, 65], percent_smokers[3]),
                  'elderly': (elderly_count, [66, 85], percent_smokers[4])}

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
                    smoking_period = randrange(age - 10)
                else:
                    smoking_period = 0

                smoking_parents = choice([True, False])

                new_person = Person(
                    age=age, smoker=smoker, smoking_parents=smoking_parents, smoking_period=smoking_period)
                if smoker:
                    self.population_count[person_type][1] += 1

                centre_positions = {'x': (int(0.16 * self.size[0]), int(0.75 * self.size[0])),
                                    'y': (int(0.16 * self.size[1]), int(0.75 * self.size[1]))}

                while True:
                    if not smokers_in_centre and not smokers_on_side:
                        position = (
                            randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))
                    else:
                        if (smokers_in_centre and smoker) or (smokers_on_side and not smoker):
                            position = (randint(centre_positions['x'][0], centre_positions['x'][1]),
                                        randint(centre_positions['y'][0], centre_positions['y'][1]))
                        else:
                            position = (
                                randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))
                    if position not in self.filled_cells:
                        self.filled_cells[position] = new_person
                        new_person.position = position
                        break
            self.population_count[person_type][0] = people[person_type][0]

        for position in self.filled_cells:
            person = self.filled_cells[position]
            if person.smoker == True:
                if person.smoking_period >= 10:
                    person.state = 'smoker_pro'
                else:
                    person.state = 'smoker_beginner'
            else:
                if person.chances_to_start_smoking(self) > 0.5:
                    person.state = 'nonsmoker_high_prob'
                else:
                    person.state = 'nonsmoker_low_prob'

    def to_matrix(self):
        """
        Return numpy.array that is filled with
        numbers from 0 to 5 depending on
        the person of what age group is
        on this position.
        """
        states = {'dead': 0,
                  'smoker_in_the_past': 1,
                  'smoker_pro': 2,
                  'smoker_beginner': 3,
                  'nonsmoker_high_prob': 4,
                  'nonsmoker_low_prob': 5
                  }
        matrix = np.zeros(shape=(self.size[0], self.size[1]))

        for position in self.filled_cells:
            x, y = position
            person = self.filled_cells[position]
            matrix[x, y] = states[person.state]

        return matrix

    def count_states(self, age_group=None):
        """
        Return list with the number of people
        of every state that occupies the grid
        at the current moment.

        If the age_group is None, return the total
        values of the whole population.

        If the age_group is the name of the age group,
        return the list of values only for this group of
        people.
        """
        states_dict = {'smoker_in_the_past': 0,
                       'smoker_pro': 0,
                       'smoker_beginner': 0,
                       'nonsmoker_high_prob': 0,
                       'nonsmoker_low_prob': 0}
        if age_group is None:
            for person in self.filled_cells.values():
                states_dict[person.state] += 1
        else:
            for person in self.filled_cells.values():
                if person.get_person_age_type() == age_group:
                    states_dict[person.state] += 1
        return list(states_dict.values())
