from person import Grid, Person
from finite_state_machine import FiniteStateMachine
from time import sleep


grid = Grid((20, 20), 0.5)
grid.random_start()

fsm = FiniteStateMachine(grid)

arrays_lst = []
for i in range(100):
    arrays_lst.append(grid.to_matrix())
    grid.next_iteration(fsm)
    sleep(1)
