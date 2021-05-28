from person import Person, Grid

class FiniteStateMachine:
    
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler = None, end_state = False):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
    
        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break 
            else:
                handler = self.handlers[newState.upper()]

state_nonsmoker_low_prob = 'nonsmoker_low_prob'
state_nonsmoker_high_prob = 'nonsmoker_high_prob'
state_smoker_beginner = 'smoker_beginner'
state_smoker_pro = 'smoker_pro'
state_smoker_in_the_past = 'smoker_in_the_past'
state_died = 'died'



def from_nonsmoker_low_prob(person: Person):
    pass

def from_nonsmoker_high_prob(person: Person):
    pass

def from_smoker_beginner(person: Person):
    pass

def from_smoker_pro(person: Person):
    pass

def from_smoker_in_the_past(person: Person):
    pass

fsm = FiniteStateMachine()
fsm.add_state(state_nonsmoker_low_prob, from_nonsmoker_low_prob)
fsm.add_state(state_nonsmoker_high_prob, from_nonsmoker_high_prob)
fsm.add_state(state_smoker_beginner, from_smoker_beginner)
fsm.add_state(state_smoker_pro, from_smoker_pro)
fsm.add_state(state_smoker_in_the_past, from_smoker_in_the_past)
fsm.add_state(state_died, end_state=True)

#set start



# positive_adjectives = ["great","super", "fun", "entertaining", "easy"]
# negative_adjectives = ["boring", "difficult", "ugly", "bad"]

# def start_transitions(txt):
#     splitted_txt = txt.split(None,1)
#     word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
#     if word == "Python":
#         newState = "Python_state"
#     else:
#         newState = "error_state"
#     return (newState, txt)

# def python_state_transitions(txt):
#     splitted_txt = txt.split(None,1)
#     word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
#     if word == "is":
#         newState = "is_state"
#     else:
#         newState = "error_state"
#     return (newState, txt)

# def is_state_transitions(txt):
#     splitted_txt = txt.split(None,1)
#     word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
#     if word == "not":
#         newState = "not_state"
#     elif word in positive_adjectives:
#         newState = "pos_state"
#     elif word in negative_adjectives:
#         newState = "neg_state"
#     else:
#         newState = "error_state"
#     return (newState, txt)

# def not_state_transitions(txt):
#     splitted_txt = txt.split(None,1)
#     word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
#     if word in positive_adjectives:
#         newState = "neg_state"
#     elif word in negative_adjectives:
#         newState = "pos_state"
#     else:
#         newState = "error_state"
#     return (newState, txt)

# def neg_state(txt):
#     print("Hallo")
#     return ("neg_state", "")


# m = StateMachine()
# m.add_state("Start", start_transitions)
# m.add_state("Python_state", python_state_transitions)
# m.add_state("is_state", is_state_transitions)
# m.add_state("not_state", not_state_transitions)
# m.add_state("neg_state", None, end_state=1)
# m.add_state("pos_state", None, end_state=1)
# m.add_state("error_state", None, end_state=1)
# m.set_start("Start")
# m.run("Python is great")
# m.run("Python is difficult")
# m.run("Perl is ugly")