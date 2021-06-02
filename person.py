from random import random, choice


class Person:
    '''
    Represents people who can be in one of six states:
    'Quit smoking' - smoked earlier but now does not (Romanus since 15.06.2021)
    'Senior smoker' - smokes more than 10 years
    'Junior smoker' - smokes less than 10 years
    'Non-smoker_high' - does not smoke but has many chances to start
    'Non-smoker_low' - does not smoke and has little chance to start
    '''

    def __init__(self, age: int, smoker: bool, smoking_parents: bool, smoking_period: int = 0, position: tuple = None):
        self.position = position
        self.age = age
        self.smoking_parents = smoking_parents
        self.smoker = smoker
        self.smoking_period = smoking_period
        self.state = None

    def influence_weight(self, people_influence):
        '''
        Return a coefficient how much surrounding
        influence on person depending on his age.
        '''
        if self.age < 16:
            return people_influence[0]
        if 15 < self.age < 26:
            return people_influence[1]
        if self.age < 46:
            return people_influence[2]
        if self.age < 66:
            return people_influence[3]
        return people_influence[4]

    def get_person_age_type(self):
        '''
        Return the name of age group
        depending on the person age.
        '''
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
        '''
        Return tuple where the first element is
        the number of smokers around the person,
        the second one - the number of nonsmokers
        around the person in the square 3x3, where
        the person is in the centre.
        '''
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

    def chances_to_die(self, grid):
        '''
        Return the constant value if the person
        is not a smoker and the higher one if he is.
        Chances depends on how many years the person
        smokes. If the person smokes more than 10 years,
        every new year has more influence than first 10
        years.
        '''
        chances = grid.chances_to_die

        weight_of_smoking_period = grid.weight_of_smoking_year_die[0]
        weight_of_smoking_period_pro = grid.weight_of_smoking_year_die[1]
        if self.smoking_period:
            if self.state != 'smoker_pro':
                chances = self.smoking_period * weight_of_smoking_period
            else:
                chances = 10 * weight_of_smoking_period + \
                    (self.smoking_period - 10) * weight_of_smoking_period_pro
        return chances

    def chances_to_start_smoking(self, grid):
        '''
        Return float between 0 and 1 that means
        chances of person to start smoking depending on
        the surrounding and the fact if his parents were
        smokers.
        '''
        if self.smoking_parents:
            weight_of_smoking_parents = grid.weight_of_smoking_parents
        else:
            weight_of_smoking_parents = 1

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_smokers = smokers / (smokers+nonsmokers)
        chances = percent_of_smokers * \
            self.influence_weight(grid.people_influence) * \
            weight_of_smoking_parents
        return min(chances, 1)

    def chances_to_stop_smoking(self, grid):
        '''
        Return float between 0 and 1 that means
        chances of person to stop smoking depending on
        the surrounding and the period how long he smokes.
        '''
        weight_of_smoking_period = grid.weight_of_smoking_year_stop

        smokers, nonsmokers = self.check_neighbors(grid)
        percent_of_nonsmokers = nonsmokers / (smokers+nonsmokers)
        chances = percent_of_nonsmokers * \
            (1 - self.smoking_period * weight_of_smoking_period)
        return max(chances, 0)

    def check_death(self, grid):
        '''
        Return True if the person has dead.
        '''
        random_death = random()
        if random_death <= self.chances_to_die(grid):
            x, y = self.position
            grid.filled_cells.pop((x, y))
            return True
        return False

    def __str__(self):
        '''
        Return info about the person.
        '''
        return f'Position: {self.position}, age: {self.age}, \
smoker: {self.smoker}, smoking_period: {self.smoking_period}, \
smoking_parents: {self.smoking_parents}, state: {self.state}'

    def move(self, grid):
        '''
        Move the person to the new cell from the square 3x3, where
        he is in the centre for now.
        '''
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
