import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from grid import Grid
from finite_state_machine import FiniteStateMachine

# uncomment this is for pycharm
# import matplotlib; matplotlib.use("TkAgg")

FRAMES = 50
INTERVAL = 100


def read_from_file(file_name):
    """
    Read all needed coefficients and statisatical
    data from file and return grid based on this data
    and statistical data (percent of every age group
    on the grid and percent of smokers from them)
    for start fillng the grid.
    Needed format of file is descibed in data\example.txt.
    Examples of files for reading are in the folder 'data'.
    """
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

        fertile_percent_non_smokers, fertile_percent_smokers = [
            float(i) for i in data.pop(0).split()]

        smokers_location = [bool(int(i)) for i in data.pop(0).split()]

    grid = Grid(size, start_fill, people_influence, weight_of_smoking_parents,
                weight_of_smoking_year_stop, chances_to_die, weight_of_smoking_year_die,
                fertile_percent_non_smokers, fertile_percent_smokers, smokers_location)
    return grid, percent_people, percent_smokers


def init():
    return


def animate(i):
    """
    Build a new state of smokers
    """
    data = arrays_lst[i + 1]
    ax = sns.heatmap(data, square=True, cbar=False, cmap=[
        "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
    ax.set(xticklabels=[], yticklabels=[])
    ax.tick_params(bottom=False, left=False)
    ax.set_title(f"Smokers around the world. Year {i + 1}.")
    # ax.text(-5.1, 1.5, f'{count_states_list[i][5]}')
    x = 5
    ax.text(-40, 2 * x, f'Non-smokers_low: {count_states_list[i][4]}',
            bbox={'facecolor': "#86ff6b", 'alpha': 1, 'pad': 10})
    ax.text(-40, 3 * x + 5, f'Non-smokers_high: {count_states_list[i][3]}',
            bbox={'facecolor': "#ffd24d", 'alpha': 1, 'pad': 10})
    ax.text(-40, 4 * x + 10, f'Junior smokers: {count_states_list[i][2]}',
            bbox={'facecolor': "#ffa46b", 'alpha': 1, 'pad': 10})
    ax.text(-40, 5 * x + 15, f'Senior smokers: {count_states_list[i][1]}',
            bbox={'facecolor': "#ff6b6b", 'alpha': 1, 'pad': 10})
    ax.text(-40, 6 * x + 20, f'Quit smoking: {count_states_list[i][0]}',
            bbox={'facecolor': "#b8b8b8", 'alpha': 1, 'pad': 10})


class SmokingAnimation:
    """
    Class to represent animation during simulation.
    """
    year_count = 0

    def __init__(self):
        fig = plt.figure("Smokers world")
        data = arrays_lst[0]
        ax = sns.heatmap(data, square=True, cmap=[
            "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
        ax.set(xticklabels=[], yticklabels=[])
        ax.tick_params(bottom=False, left=False)
        c_bar = ax.collections[0].colorbar
        c_bar.set_ticks([0.3 + 0.85 * i for i in range(6)])
        c_bar.set_ticklabels(
            ['None', 'Quit smoking', 'Senior smokers', 'Junior smokers', 'Non-smokers (high)', 'Non-smokers (low)'])
        plt.title("Smokers around the world.")

        self.animation = animation.FuncAnimation(fig, animate, init_func=init, frames=FRAMES, repeat=False,
                                                 interval=INTERVAL)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        """
        A helper function for pausing the animation.
        """
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused


def statistic_window(teen, young, adult, elderly):
    """
    Open new window with 4 different plots representing
    statistics gathered during simulation
    """
    y = list(range(51))

    def category_data(category, k, h):
        """
        A helper function to draw subplots in animation.
        """
        quit_smoking = []
        senior_smokers = []
        junior_smokers = []
        non_smoker_high = []
        non_smokers_low = []
        for year in category:
            quit_smoking.append(year[0])
            senior_smokers.append(year[1])
            junior_smokers.append(year[2])
            non_smoker_high.append(year[3])
            non_smokers_low.append(year[4])
        axes[k, h].plot(y, quit_smoking, label="Quit smoking", color='#b8b8b8')
        axes[k, h].plot(y, junior_smokers, label="Junior smokers", color='#ffa46b')
        axes[k, h].plot(y, senior_smokers, label="Senior smokers", color='#ff6b6b')
        axes[k, h].plot(y, non_smoker_high, label="Non-smokers (high)", color='#ffd24d')
        axes[k, h].plot(y, non_smokers_low, label="Non-smokers (low)", color='#86ff6b')

    figure, axes = plt.subplots(nrows=2, ncols=2)

    plt.suptitle('Results of simulation', fontsize=30)

    axes[0, 0].set_title("Teen", fontsize=20)
    axes[0, 1].set_title("Young", fontsize=20)
    axes[1, 0].set_title("Adult", fontsize=20)
    axes[1, 1].set_title("Elderly", fontsize=20)
    category_data(teen, 0, 0)
    plt.figlegend(loc="lower center", ncol=5)

    category_data(young, 0, 1)
    category_data(adult, 1, 0)
    category_data(elderly, 1, 1)

    plt.setp(axes[1, :], xlabel='years of simulation')
    plt.setp(axes[1, :], ylabel='number of people')
    plt.setp(axes[0, :], ylabel='number of people')


if __name__ == '__main__':
    # read needed data from file and fill the grid with people
    file_name = 'data/centregrid70x70.txt'
    grid, percent_people, percent_smokers = read_from_file(file_name)
    grid.random_start(percent_people, percent_smokers)

    # create a finite state machine for updating human states
    fsm = FiniteStateMachine(grid)

    # create lists for giving data to visualisation
    arrays_lst = [grid.to_matrix()]
    count_states_list = [grid.count_states()]

    count_teen = [grid.count_states('teen')]
    count_young = [grid.count_states('young')]
    count_adult = [grid.count_states('adult')]
    count_elderly = [grid.count_states('elderly')]

    # add info about 100 years on the grid to lists
    for i in range(50):
        grid.next_iteration(fsm)
        arrays_lst.append(grid.to_matrix())
        count_states_list.append(grid.count_states())
        count_teen.append(grid.count_states('teen'))
        count_young.append(grid.count_states('young'))
        count_adult.append(grid.count_states('adult'))
        count_elderly.append(grid.count_states('elderly'))

    for i in count_states_list:
        for j in range(len(i)):
            if i[j] < 1000:
                i[j] = str(i[j]).zfill(4)

    pa = SmokingAnimation()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.show()

    statistic_window(count_teen, count_young, count_adult, count_elderly)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.show()
