import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from person import Grid, Person
from finite_state_machine import FiniteStateMachine

# this is for pycharm
# import matplotlib; matplotlib.use("TkAgg")

FRAMES = 100
INTERVAL = 100

def read_from_file(file_name):
    with open(file_name) as f:
        data = f.readlines()

        size = [int(i) for i in data.pop(0).split()]
        start_fill = float(data.pop(0))

        percent_people = [float(i) for i in data.pop(0).split()]
        percent_smokers = [float(i) for i in data.pop(0).split()]
        people_influence = [float(i) for i in data.pop(0).split()]
        #
        chances_to_die = float(data.pop(0))
        weight_of_smoking_year_die = [float(i) for i in data.pop(0).split()]

        weight_of_smoking_parents = float(data.pop(0))

        weight_of_smoking_year_stop = float(data.pop(0))


    grid = Grid(size, start_fill, people_influence, weight_of_smoking_parents, \
        weight_of_smoking_year_stop, chances_to_die, weight_of_smoking_year_die)
    return grid, percent_people, percent_smokers


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
    ax.text(-5.1, 1.5, f'{count_states_list[i][5]}')
    # ax.text(-12, 1.5, f'Non-smokers_low: {count_states_list[i][5]}',
    #         bbox={'facecolor': "#86ff6b", 'alpha': 1, 'pad': 10})
    # ax.text(-12, 4.5, f'Non-smokers_high: {count_states_list[i][4]}',
    #         bbox={'facecolor': "#ffd24d", 'alpha': 1, 'pad': 10})
    # ax.text(-12, 7.5, f'Junior smokers: {count_states_list[i][3]}',
    #         bbox={'facecolor': "#ffa46b", 'alpha': 1, 'pad': 10})
    # ax.text(-12, 10.5, f'Senior smokers: {count_states_list[i][2]}',
    #         bbox={'facecolor': "#ff6b6b", 'alpha': 1, 'pad': 10})
    # ax.text(-12, 13.5, f'Quit smoking: {count_states_list[i][1]}',
    #         bbox={'facecolor': "#b8b8b8", 'alpha': 1, 'pad': 10})


class SmokingAnimation:
    year_count = 0

    def __init__(self):
        plt.rcParams.update({'font.family': 'Helvetica'})
        fig = plt.figure("Smokers world")
        data = arrays_lst[0]
        ax = sns.heatmap(data, square=True, cmap=[
            "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
        ax.text(-5.1, 1.5, '')
        ax.text(-12, 1.5, f'Non-smokers_low:         ',
                bbox={'facecolor': "#86ff6b", 'alpha': 1, 'pad': 10})
        ax.text(-12, 4.5, f'Non-smokers_high:         ',
                bbox={'facecolor': "#ffd24d", 'alpha': 1, 'pad': 10})
        ax.text(-12, 7.5, f'Junior smokers:         ',
                bbox={'facecolor': "#ffa46b", 'alpha': 1, 'pad': 10})
        ax.text(-12, 10.5, f'Senior smokers:          ',
                bbox={'facecolor': "#ff6b6b", 'alpha': 1, 'pad': 10})
        ax.text(-12, 13.5, f'Quit smoking:         ',
                bbox={'facecolor': "#b8b8b8", 'alpha': 1, 'pad': 10})
        ax.set(xticklabels=[], yticklabels=[])
        ax.tick_params(bottom=False, left=False)
        c_bar = ax.collections[0].colorbar
        c_bar.set_ticks([0.3 + 0.85 * i for i in range(6)])
        c_bar.set_ticklabels(
            ['None', 'Quit smoking', 'Senior smokers', 'Junior smokers', 'Non-smokers_high', 'Non-smokers_low'])
        plt.title("Smokers around the world.")

        self.animation = animation.FuncAnimation(fig, animate, init_func=init, frames=FRAMES, repeat=False,
                                                 interval=INTERVAL)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused


if __name__ == '__main__':
    file_name = '1.txt'
    grid, percent_people, percent_smokers = read_from_file(file_name)
    grid.random_start(percent_people, percent_smokers)
    fsm = FiniteStateMachine(grid)

    arrays_lst = [grid.to_matrix()]
    count_states_list = [grid.count_states()]
    count_teen = [grid.count_states('teen')]
    count_young = [grid.count_states('young')]
    count_adult = [grid.count_states('adult')]
    count_elderly = [grid.count_states('elderly')]

    for i in range(100):
        grid.next_iteration(fsm)
        arrays_lst.append(grid.to_matrix())
        count_states_list.append(grid.count_states())

    pa = PauseAnimation()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()
