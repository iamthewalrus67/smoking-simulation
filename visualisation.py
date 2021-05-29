import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
# import matplotlib; matplotlib.use("TkAgg")


def init():
    return


def animate(i):
    data = np.random.rand(100, 100)
    ax = sns.heatmap(data, square=True, cbar=False, cmap=[
        "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
    ax.set(xticklabels=[], yticklabels=[])
    ax.tick_params(bottom=False, left=False)


class PauseAnimation:
    def __init__(self):
        plt.rcParams.update({'font.family': 'Helvetica'})
        fig = plt.figure("Smokers world")
        data = np.random.rand(100, 100)
        ax = sns.heatmap(data, square=True, cmap=[
            "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True})
        ax.set(xticklabels=[], yticklabels=[])
        ax.tick_params(bottom=False, left=False)
        c_bar = ax.collections[0].colorbar
        c_bar.set_ticks([0.07, 1 / 6 + 0.07, 2 / 6 + 0.07, 3 / 6 + 0.07, 4 / 6 + 0.07, 1 - 0.07])
        c_bar.set_ticklabels(
            ['Dead', 'Quit smoking', 'Senior smokers', 'Middle smokers', 'Junior smokers', 'Non-smokers'])
        plt.title("Smokers around the world")

        self.animation = animation.FuncAnimation(fig, animate, init_func=init, frames=20, repeat=True)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused


pa = PauseAnimation()
plt.show()
