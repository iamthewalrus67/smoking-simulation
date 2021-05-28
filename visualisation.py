import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


plt.rcParams.update({'font.family': 'Helvetica'})
uniform_data = np.random.rand(100, 100)
plt.figure("Smokers world")
ax = sns.heatmap(uniform_data, linewidth=0, cmap=[
                 "#ededed", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b"], cbar_kws={"drawedges": True}, square=True)
c_bar = ax.collections[0].colorbar
c_bar.set_ticks([0.07, 1/6+0.07, 2/6+0.07, 3/6+0.07, 4/6+0.07, 1-0.07])
c_bar.set_ticklabels(
    ['Dead', 'Quit smoking', 'Senior smokers', 'Middle smokers', 'Junior smokers', 'Non-smokers'])
plt.title("Smokers around the world")
plt.show()
