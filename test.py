import numpy as np
import plotly.graph_objs as go
arrays = [np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10]), np.empty([10, 10, 10])]
for a in range(len(arrays)):
    arrays[a].fill(a)
for i in range(10):
    N = 10
    # M = np.random.random((N, 10, 10))
    M = arrays[i]
    fig = go.Figure(
        data=[go.Heatmap(z=M[0])],
        layout=go.Layout(
            title="Smokers in the world",
            title_x=0.5,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                            method="animate",
                            args=[None]),
                        dict(label="Pause",
                            method="animate",
                            args=[None,
                                {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                            )])]
        ),
        frames=[go.Frame(data=[go.Heatmap(z=M[i])],
                        layout=go.Layout(title_text=f"Year {i}")) 
                for i in range(1, N)]
    )
fig.show()