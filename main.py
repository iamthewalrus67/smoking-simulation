from person import Grid, Person
from finite_state_machine import FiniteStateMachine
from time import sleep


grid = Grid((10, 10), 1)
grid.random_start()

fsm = FiniteStateMachine(grid)


for i in range(100):
    grid.next_iteration(fsm)
    sleep(1)