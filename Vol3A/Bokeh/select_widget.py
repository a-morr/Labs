import pandas as pd
import numpy as np
from bokeh.io import curdoc 
from bokeh.plotting import Figure, output_file, show
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column

COUNT = 10
df = pd.DataFrame({"x":np.random.rand(COUNT), "y":np.random.rand(COUNT), "color":"white"})
source = ColumnDataSource(df)

fig = Figure()
fig.circle(source=source, x="x", y="y", fill_color="color", line_color="black", size=40)

select = Select(title="Option:", value="white", options=["white", "red", "blue", "yellow"])

def update_color(attrname, old, new):
    source.data["color"] = [select.value]*COUNT
    
select.on_change('value', update_color)

curdoc().add_root(column(fig, select))
