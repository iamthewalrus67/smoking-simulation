import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from person import Grid, Person
from finite_state_machine import FiniteStateMachine
from time import sleep
from matplotlib.backend_bases import MouseButton

# this is for pycharm
import matplotlib; matplotlib.use("TkAgg")

FRAMES = 100
INTERVAL = 1
# arrays_lst = [np.random.rand(100, 100) for _ in range(FRAMES)]


grid = Grid((20, 20), 0.5)
grid.random_start()

fsm = FiniteStateMachine(grid)

arrays_lst = [grid.to_matrix()]
count_states_list = [grid.count_states()]
for i in range(100):
    grid.next_iteration(fsm)
    arrays_lst.append(grid.to_matrix())
    count_states_list.append(grid.count_states())
    # print(count_states_list[i])
    # sleep(1)

for i in count_states_list:
    for j in range(len(i)):
        if i[j] < 100:
            i[j] = str(i[j]).zfill(3)

def init():
    return


def animate(i):
    data = arrays_lst[i + 1]
    ax = sns.heatmap(data, square=True, cbar=False, cmap=[
        "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
    ax.set(xticklabels=[], yticklabels=[])
    ax.tick_params(bottom=False, left=False)
    ax.set_title(f"Smokers around the world. Year {i + 1}.")
    ax.text(-12, 1.5, f'Non-smokers_low: {count_states_list[i][5]}',
            bbox={'facecolor': "#86ff6b", 'alpha': 1, 'pad': 10})
    ax.text(-12, 4.5, f'Non-smokers_high: {count_states_list[i][4]}',
            bbox={'facecolor': "#ffd24d", 'alpha': 1, 'pad': 10})
    ax.text(-12, 7.5, f'Junior smokers: {count_states_list[i][3]}',
            bbox={'facecolor': "#ffa46b", 'alpha': 1, 'pad': 10})
    ax.text(-12, 10.5, f'Senior smokers: {count_states_list[i][2]}',
            bbox={'facecolor': "#ff6b6b", 'alpha': 1, 'pad': 10})
    ax.text(-12, 13.5, f'Quit smoking: {count_states_list[i][1]}',
            bbox={'facecolor': "#b8b8b8", 'alpha': 1, 'pad': 10})
    ax.text(-12, 16.5, f'Nobody: {count_states_list[i][0]}',
            bbox={'facecolor': "#ededed", 'alpha': 1, 'pad': 10})


class PauseAnimation:
    year_count = 0

    def __init__(self):
        plt.rcParams.update({'font.family': 'Helvetica'})
        fig = plt.figure("Smokers world")
        data = arrays_lst[0]
        ax = sns.heatmap(data, square=True, cmap=[
            "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
        ax.set(xticklabels=[], yticklabels=[])
        ax.tick_params(bottom=False, left=False)
        c_bar = ax.collections[0].colorbar
        c_bar.set_ticks([0.3 + 0.85 * i for i in range(6)])
        c_bar.set_ticklabels(
            ['Nobody', 'Quit smoking', 'Senior smokers', 'Junior smokers', 'Non-smokers_high', 'Non-smokers_low'])
        plt.title("Smokers around the world.")

        self.animation = animation.FuncAnimation(fig, animate, init_func=init, frames=FRAMES, repeat=True,
                                                 interval=INTERVAL)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)


pa = PauseAnimation()
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()
