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
        self.endStates = ['died']
        self.grid = grid

    def add_state(self, name, handler = None, end_state = False):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    # def set_start(self, name):
    #     self.startState = name
    
    def next(self, person):
        handler = self.handlers[person.state]
        new_state = handler(person, self.grid)
        person.state = new_state

    # def run(self, cargo):
    #     try:
    #         handler = self.handlers[self.startState]
    #     except:
    #         raise InitializationError("must call .set_start() before .run()")
    #     if not self.endStates:
    #         raise  InitializationError("at least one state must be an end_state")
    
    #     while True:
    #         (newState, cargo) = handler(cargo)
    #         if newState.upper() in self.endStates:
    #             print("reached ", newState)
    #             break 
    #         else:
    #             handler = self.handlers[newState.upper()]



def from_nonsmoker(person, grid):
    if person.check_death(grid):
        return 'died'
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
        return 'died'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        new_state = 'smoker_in_the_past'
    elif person.smoking_period >= 5:
        new_state = 'smoker_pro'
    return new_state

def from_smoker_pro(person, grid):
    new_state = 'smoker_pro'
    if person.check_death(grid):
        return 'died'
    random_float = random()
    if random_float <= person.chances_to_stop_smoking(grid):
        new_state = 'smoker_in_the_past'
    return new_state

def from_smoker_in_the_past(person, grid):
    new_state = 'smoker_in_the_past'
    if person.check_death(grid):
        return 'died'

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
# state_died = 'died'

# fsm = FiniteStateMachine()
# fsm.add_state(state_nonsmoker_low_prob, from_nonsmoker)
# fsm.add_state(state_nonsmoker_high_prob, from_nonsmoker)
# fsm.add_state(state_smoker_beginner, from_smoker_beginner)
# fsm.add_state(state_smoker_pro, from_smoker_pro)
# fsm.add_state(state_smoker_in_the_past, from_smoker_in_the_past)
# fsm.add_state(state_died, end_state=True)

