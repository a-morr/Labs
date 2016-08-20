# To run the solutions, you must have bokeh 0.12.0 and pyproj installed.
# To install these packages, in a terminal/commandline run
#
#       conda install bokeh==0.12.0
#       conda install pyproj
#
# This lab also includes data sets you will need to download. To download
# the needed data, in ipython run
#
#       import bokeh
#       bokeh.sampledata.download()
#
# Then to view the Bokeh application, in a termrinal/commandline, run
#
#       bokeh serve bokeh_solutions.py
#
# Then navigate to localhost:5006/bokeh_solutions in your web browser.


from __future__ import division
import numpy as np
import pandas as pd
import pickle
from bokeh.io import curdoc
from bokeh.plotting import Figure, output_file, show
from bokeh.layouts import column, row, layout, widgetbox
from bokeh.palettes import Reds9 as COLORS
#from bokeh.tile_providers import STAMEN_TONER, STAMEN_TERRAIN, STAMEN_TONER_BACKGROUND
from bokeh.sampledata import us_states
from bokeh.core.properties import Either, Auto, Instance
from bokeh.models import (Range1d, ColumnDataSource, Slider,
                        CustomJS, HoverTool, WheelZoomTool,
                        DataRange1d, TextInput, Toggle, Div,
                        WMTSTileSource)
from bokeh.models.widgets import CheckboxButtonGroup, Select

from pyproj import Proj, transform

# Prep data
accidents = pd.read_pickle("fars_accidents.pickle")
drivers = pd.read_pickle("final_drivers.pickle")

#us_states = us_states.data.copy()
with open("us_states.pickle", "rb") as file:
    us_states = pickle.load(file)

state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]

state_names = us_states.keys()

id_to_st = {1:"AL", 2:"AK", 4:"AZ", 5:"AR", 6:"CA", 8:"CO", 9:"CT", 10:"DE",
            11:"DC", 12:"FL", 13:"GA", 15:"HI", 16:"ID", 17:"IL", 18:"IN",
            19:"IA", 20:"KS", 21:"KY", 22:"LA", 23:"ME", 24:"MD", 25:"MA",
            26:"MI", 27:"MN", 28:"MS", 29:"MO", 30:"MT", 31:"NE", 32:"NV",
            33:"NH", 34:"NJ", 35:"NM", 36:"NY", 37:"NC", 38:"ND", 39:"OH",
            40:"OK", 41:"OR", 42:"PA", 44:"RI", 45:"SC", 46:"SD", 47:"TN",
            48:"TX", 49:"UT", 50:"VT", 51:"VA", 53:"WA", 54:"WV", 55:"WI",
            56:"WY"}

with open("id_to_state.pickle", "wb") as f:
    pickle.dump(id_to_st, f)

st_to_id = {v: k for k, v in id_to_st.items()}

id_list = []
for s in state_names:
    id_list.append(st_to_id[s])

state_totals = [accidents[accidents["STATE"]==s].shape[0] for s in id_list]
state_drunk = [accidents[(accidents["STATE"]==s) & (accidents["DRUNK_DR"]>0)].shape[0] for s in id_list]
state_percent = (np.array(state_drunk) / np.array(state_totals, dtype=float)) * 100
state_speed = [accidents[(accidents["STATE"]==s) & (accidents["SP"]==1)].shape[0] for s in id_list]
state_percent_sp = (np.array(state_speed) / np.array(state_totals, dtype=float)) * 100

# Convert data to appropriate format for map
"""
from_proj = Proj(init="epsg:4326")
to_proj = Proj(init="epsg:3857")

def convert(longitudes, latitudes):
    x_vals = []
    y_vals = []
    for lon, lat in zip(longitudes, latitudes):
        x, y = transform(from_proj, to_proj, lon, lat)
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals

accidents["x"], accidents["y"] = convert(accidents.LONGITUD, accidents.LATITUDE)
accidents["r"] = 10000

accidents.to_pickle("fars_accidents.pickle")


borders_x = []
borders_y = []
for i in xrange(len(state_xs)):
    cx, cy = convert(state_xs[i], state_ys[i])
    borders_x.append(cx)
    borders_y.append(cy)

borders = dict(x=borders_x, y=borders_y)
with open("borders.pickle", "wb") as f:
    pickle.dump(borders, f)
"""

# set up map
mercator_extent = dict(start=-1400000, end=2000000, bounds="auto", )
x_range = Range1d(start=-14000000, end=-7000000, bounds="auto")
y_range = Range1d(start=2500000, end=6500000, bounds="auto")

fig = Figure(plot_width=1100, plot_height=650, tools=["wheel_zoom", "pan"],
            x_range=(-13000000, -7000000), y_range=(2750000, 6250000), webgl=True,
            active_scroll="wheel_zoom")
fig.axis.visible = False

STAMEN_TONER_BACKGROUND = WMTSTileSource(
    url='http://tile.stamen.com/toner-background/{Z}/{X}/{Y}.png',
    attribution=(
        'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
        'under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>.'
        'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, '
        'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>'
    )
)

fig.add_tile(STAMEN_TONER_BACKGROUND)

accidents.loc[accidents.DRUNK_DR != 0, "DRUNK_DR"] = "YES"
accidents.loc[accidents.DRUNK_DR == 0, "DRUNK_DR"] = "NO"
accidents.loc[accidents.SP != 0, "SP"] = "YES"
accidents.loc[accidents.SP == 0, "SP"] = "NO"
accidents.loc[accidents.WEATHER.isin([0,1,8,10,98,99]), "WEATHER"] = "Clear"
accidents.loc[accidents.WEATHER == 2, "WEATHER"] = "Rain"
accidents.loc[accidents.WEATHER == 3, "WEATHER"] = "Sleet/Hail"
accidents.loc[accidents.WEATHER == 4, "WEATHER"] = "Snow"
accidents.loc[accidents.WEATHER == 5, "WEATHER"] = "Fog/Smog/Smoke"
accidents.loc[accidents.WEATHER == 6, "WEATHER"] = "Severe Crosswinds"
accidents.loc[accidents.WEATHER == 7, "WEATHER"] = "Blowing Sand, Soil, Dirt"
accidents.loc[accidents.WEATHER == 11, "WEATHER"] = "Blowing Snow"
accidents.loc[accidents.WEATHER == 12, "WEATHER"] = "Freezing Rain"

accidents["r"] = 10000

drunk = accidents[accidents.DRUNK_DR == "YES"].copy()
speed = accidents[(accidents.DRUNK_DR == "NO") & (accidents.SP == "YES")].copy()
other = accidents[(accidents.DRUNK_DR == "NO") & (accidents.SP == "NO")].copy()

del accidents

COLORS.reverse()
no_colors = ['#FFFFFF']*len(state_names)
drunk_colors = [COLORS[i] for i in pd.qcut(state_percent, len(COLORS)).codes]
speeding_colors = [COLORS[i] for i in pd.qcut(state_percent_sp, len(COLORS)).codes]
alpha=[0]*len(state_names)


with open("borders.pickle", "rb") as f:
    b = pickle.load(f)

patch_source = ColumnDataSource(
    data=dict(borders_x=b["x"],
        borders_y=b["y"],
        colors=no_colors,
        alpha=alpha,
        state_names=state_names,
        state_totals=state_totals,
        state_drunk=state_drunk,
        state_percent=state_percent,
        state_percent_sp=state_percent_sp
    )
)

patches = fig.patches(xs="borders_x", ys="borders_y", source=patch_source, fill_alpha="alpha",
                    fill_color="colors", line_alpha=0, hover_alpha=.3, line_width=5)

fig.add_tools(HoverTool(renderers=[patches], tooltips=[("State", "@state_names"),
                                      ("Total", "@state_totals"),
                                      ("Drunk%", "@state_percent{1.11}" + "%"),
                                      ("Speeding%", "@state_percent_sp{1.11}" + "%")]))
select = Select(title="Color States By:", value="None", options=["None", "Drunk%", "Speeding%"])

def update_color(attrname, old, new):
    if select.value == "Drunk%":
        patch_source.data["colors"] = drunk_colors
        patch_source.data["alpha"] = [.3]*len(state_names)
    elif select.value == "Speeding%":
        patch_source.data["colors"] = speeding_colors
        patch_source.data["alpha"] = [.3]*len(state_names)
    else:
        patch_source.data["colors"] = no_colors
        patch_source.data["alpha"] = [0]*len(state_names)

select.on_change('value', update_color)

# --------------------------------------

def gen_dict(df):
    return dict(
        x=df["x"],
        y=df["y"],
        r=df["r"],
        MONTH=df["MONTH"],
        DAY=df["DAY"],
        YEAR=df["YEAR"],
        FATALS=df["FATALS"],
        DRUNK_DR=df["DRUNK_DR"],
        SP=df["SP"],
        WEATHER=df["WEATHER"]
    )

other_source = ColumnDataSource(data=gen_dict(other))
speed_source = ColumnDataSource(data=gen_dict(speed))
drunk_source = ColumnDataSource(data=gen_dict(drunk))

other_circles = fig.circle(source=other_source, x="x", y="y", radius="r", fill_color="gray",
            fill_alpha=.3, line_alpha=0, hover_alpha=1, hover_color="yellow", legend="Other")
speed_circles = fig.circle(source=speed_source, x="x", y="y", radius="r", fill_color="blue",
            fill_alpha=.3, line_alpha=0, hover_alpha=1, hover_color="yellow", legend="Speeding")
drunk_circles = fig.circle(source=drunk_source, x="x", y="y", radius="r", fill_color="red",
            fill_alpha=.3, line_alpha=0, hover_alpha=1, hover_color="yellow", legend="Drunk")

dot_tooltips = [("Date", "@MONTH/@DAY/@YEAR"), ("Fatalities", "@FATALS"), ("Drunk", "@DRUNK_DR"),
                ("Speeding", "@SP"), ("Weather", "@WEATHER")]

fig.add_tools(HoverTool(renderers=[other_circles, speed_circles, drunk_circles], tooltips=dot_tooltips))

button_group = CheckboxButtonGroup(
        labels=["Other", "Speeding", "Drunk"], active=[0, 1, 2], width=200)

toggle = Toggle(label="Sort by Hour", button_type="default")

slider = Slider(title="Hour (Military Time)", start=0, end=23, value=0, step=1)

empty_dict = dict(
        x=np.array([]),
        y=np.array([]),
        r=np.array([]),
        MONTH=np.array([]),
        DAY=np.array([]),
        YEAR=np.array([]),
        FATALS=np.array([]),
        DRUNK_DR=np.array([]),
        SP=np.array([]),
        WEATHER=np.array([])
)

def update_hour(attrname, old, new):
    if toggle.active:
        if 0 in button_group.active:
            new_other = other[other.HOUR == slider.value]
            other_source.data = gen_dict(new_other)
        else:
            other_source.data = empty_dict

        if 1 in button_group.active:
            new_speed = speed[speed.HOUR == slider.value]
            speed_source.data = gen_dict(new_speed)
        else:
            speed_source.data = empty_dict

        if 2 in button_group.active:
            new_drunk = drunk[drunk.HOUR == slider.value]
            drunk_source.data = gen_dict(new_drunk)
        else:
            drunk_source.data = empty_dict
    else:
        if 0 in button_group.active:
            other_source.data = gen_dict(other)
        else:
            other_source.data = empty_dict

        if 1 in button_group.active:
            speed_source.data = gen_dict(speed)
        else:
            speed_source.data = empty_dict

        if 2 in button_group.active:
            drunk_source.data = gen_dict(drunk)
        else:
            drunk_source.data = empty_dict


slider.on_change('value', update_hour)
toggle.on_change('active', update_hour)
button_group.on_change('active', update_hour)

callback = CustomJS(args=dict(other=other_circles, speed=speed_circles, drunk=drunk_circles), code="""
        other.glyph.radius = { value: cb_obj.get('value')*125 }
        other.data_source.trigger('change')

        speed.glyph.radius = { value: cb_obj.get('value')*125 }
        speed.data_source.trigger('change')

        drunk.glyph.radius = { value: cb_obj.get('value')*125 }
        drunk.data_source.trigger('change')
""")

size_slider = Slider(title="Dot Size", start=1, end=100, orientation="horizontal",
                value=100, step=1, callback=callback, callback_policy="mouseup")

fig.legend.background_fill_alpha = 1
fig.legend.background_fill_color = "gainsboro"
fig.legend.border_line_width = 4
fig.legend.level="overlay"
fig.legend.label_text_font_size = "15pt"

wbox = widgetbox(select, Div(text="<br>"), Div(text="Type of Accidents to Show:"),
                button_group, Div(text="<br>"), toggle, slider, Div(text="<br>"),
                size_slider)

curdoc().add_root(row(fig, wbox))
