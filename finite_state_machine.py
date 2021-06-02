from random import random


class FiniteStateMachine:
    '''
    Represents finite state machine with states:
        'nonsmoker_low_prob'
        'nonsmoker_high_prob'
        'smoker_beginner'
        'smoker_pro'
        'smoker_in_the_past'
        'dead'
    'dead' is the end state
    '''

    def __init__(self, grid):
        self.handlers = {'nonsmoker_low_prob': from_nonsmoker,
                         'nonsmoker_high_prob': from_nonsmoker,
                         'smoker_beginner': from_smoker_beginner,
                         'smoker_pro': from_smoker_pro,
                         'smoker_in_the_past': from_smoker_in_the_past}
        self.endStates = ['dead']
        self.grid = grid

    def next(self, person):
        '''
        Change the person's parameters after 1 year of life.
        '''
        smoke_earlier = person.smoker
        age_group_earlier = person.get_person_age_type()

        person.age += 1

        handler = self.handlers[person.state]

        new_state = handler(person, self.grid)
        person.state = new_state

        smoke_now = person.smoker
        age_group_now = person.get_person_age_type()

        if new_state in self.endStates:
            self.grid.population_count[age_group_earlier][0] -= 1
            if smoke_earlier == True:
                self.grid.population_count[age_group_earlier][1] -= 1

        elif age_group_earlier == age_group_now:
            if smoke_earlier == False and smoke_now == True:
                self.grid.population_count[age_group_now][1] += 1
            elif smoke_earlier == True and smoke_now == False:
                self.grid.population_count[age_group_now][1] -= 1
        else:
            self.grid.population_count[age_group_earlier][0] -= 1
            self.grid.population_count[age_group_now][0] += 1

            if smoke_earlier == smoke_now == True:
                self.grid.population_count[age_group_earlier][1] -= 1
                self.grid.population_count[age_group_now][1] += 1

            elif smoke_earlier == True and smoke_now == False:
                self.grid.population_count[age_group_earlier][1] -= 1

            elif smoke_earlier == False and smoke_now == True:
                self.grid.population_count[age_group_now][1] += 1


def from_nonsmoker(person, grid):
    '''
    Return the new state of nonsmoker
    after 1 year of life.
    '''
    new_state = person.state
    if person.check_death(grid):
        return 'dead'
    if person.chances_to_start_smoking(grid) < 0.5:
        new_state = 'nonsmoker_low_prob'
    else:
        new_state = 'nonsmoker_high_prob'
    random_float = random()
    if random_float <= person.chances_to_start_smoking(grid) and person.get_person_age_type() != 'children':
        person.smoker = True
        new_state = 'smoker_beginner'
    return new_state


def from_smoker_beginner(person, grid):
    '''
    Return the new state of smoker_beginner
    after 1 year of life.
    '''
    new_state = 'smoker_beginner'
    person.smoking_period += 1
    if person.check_death(grid):
        return 'dead'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        person.smoker = False
        new_state = 'smoker_in_the_past'
    elif person.smoking_period >= 10:
        new_state = 'smoker_pro'
    return new_state


def from_smoker_pro(person, grid):
    '''
    Return the new state of smoker_pro
    after 1 year of life.
    '''
    new_state = 'smoker_pro'
    person.smoking_period += 1
    if person.check_death(grid):
        return 'dead'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        person.smoker = False
        new_state = 'smoker_in_the_past'
    return new_state


def from_smoker_in_the_past(person, grid):
    '''
    Return the new state of smoker_in_the_past
    after 1 year of life.
    '''
    new_state = 'smoker_in_the_past'
    if person.check_death(grid):
        return 'dead'

    random_float = random()
    if random_float <= person.chances_to_start_smoking(grid):
        if person.smoking_period < 10:
            person.smoker = True
            new_state = 'smoker_beginner'
        else:
            new_state = 'smoker_pro'
            person.smoker = True
    return new_state
