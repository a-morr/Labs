import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import Figure, output_file, show
from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import column

COUNT = 10
df = pd.DataFrame({"x":np.random.rand(COUNT), "y":np.random.rand(COUNT), "radius":0.05})
source = ColumnDataSource(df)

fig = Figure()
fig.circle(source=source, x="x", y="y", fill_color="red", line_color="black", radius="radius")

slider = Slider(start=1, end=10, step=0.1, value=5)

def update_size(attrname, old, new):
    source.data["radius"] = [slider.value / 100.]*COUNT

slider.on_change('value', update_size)

curdoc().add_root(column(fig,slider))
