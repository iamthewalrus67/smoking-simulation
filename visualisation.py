import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

uniform_data = np.random.rand(100, 100)
plt.figure("Smokers world")
ax = sns.heatmap(uniform_data, linewidth=0.5, cmap=[
                 "#2b2b2b", "#b8b8b8", "#ff6b6b", "#ffa46b", "#ffd24d", "#86ff6b", ])
plt.show()
