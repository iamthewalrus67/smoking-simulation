from random import random

# from person import Person, Grid


class FiniteStateMachine:

    def __init__(self, grid):
        self.handlers = {'nonsmoker_low_prob': from_nonsmoker,
                         'nonsmoker_high_prob': from_nonsmoker,
                         'smoker_beginner': from_smoker_beginner,
                         'smoker_pro': from_smoker_pro,
                         'smoker_in_the_past': from_smoker_in_the_past}
        # self.startState = None
        self.endStates = ['dead']
        self.grid = grid

    def add_state(self, name, handler=None, end_state=False):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    # def set_start(self, name):
    #     self.startState = name

    def next(self, person):
        smoke_earlier = person.smoker
        age_group_earlier = person.get_person_age_type()

        person.age += 1

        handler = self.handlers[person.state]
        new_state = handler(person, self.grid)
        person.state = new_state

        smoke_now = person.smoker
        age_group_now = person.get_person_age_type()
        
        if new_state == 'dead':
            self.grid.population_count[age_group_earlier][0] -= 1
            if smoke_earlier:
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
    if person.check_death(grid):
        return 'dead'
    if person.chances_to_start_smoking(grid) < 0.5:
        new_state = 'nonsmoker_low_prob'
    else:
        new_state = 'nonsmoker_high_prob'
    random_float = random()
    if random_float <= person.chances_to_start_smoking(grid):
        new_state = 'smoker_beginner'
    return new_state


def from_smoker_beginner(person, grid):
    new_state = 'smoker_beginner'
    if person.check_death(grid):
        return 'dead'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        new_state = 'smoker_in_the_past'
    elif person.smoking_period >= 5:
        new_state = 'smoker_pro'
    return new_state


def from_smoker_pro(person, grid):
    new_state = 'smoker_pro'
    if person.check_death(grid):
        return 'dead'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        new_state = 'smoker_in_the_past'
    return new_state


def from_smoker_in_the_past(person, grid):
    new_state = 'smoker_in_the_past'
    if person.check_death(grid):
        return 'dead'

    random_float = random()
    if random_float <= person.chances_to_start_smoking(grid):
        if person.smoking_period < 5:
            new_state = 'smoker_beginner'
        else:
            new_state = 'smoker_pro'
    return new_state

# state_nonsmoker_low_prob = 'nonsmoker_low_prob'
# state_nonsmoker_high_prob = 'nonsmoker_high_prob'
# state_smoker_beginner = 'smoker_beginner'
# state_smoker_pro = 'smoker_pro'
# state_smoker_in_the_past = 'smoker_in_the_past'
# state_dead = 'dead'

# fsm = FiniteStateMachine()
# fsm.add_state(state_nonsmoker_low_prob, from_nonsmoker)
# fsm.add_state(state_nonsmoker_high_prob, from_nonsmoker)
# fsm.add_state(state_smoker_beginner, from_smoker_beginner)
# fsm.add_state(state_smoker_pro, from_smoker_pro)
# fsm.add_state(state_smoker_in_the_past, from_smoker_in_the_past)
# fsm.add_state(state_dead, end_state=True)
