# To handle data
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas

# To make visualizations
import hvplot.pandas
import panel as pn; pn.extension()
from panel.template import DarkTheme
import matplotlib.pyplot as plt
from panel.interact import interact



# data source https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420 (License CC BY-SA 4.0)
data = pd.read_csv('master.csv')

pn.extension()
pd.options.plotting.backend = 'holoviews'

countries = list(data['country'].unique())
years = np.array(data['year'].unique())
print(years)
data.interactive()

import hvplot.pandas  # Enable interactive
import param
import panel as pn
pn.extension()

year_selection = pn.widgets.IntRangeSlider(name='Period to visualize', start=int(years.min()), end=int(years.max()), value=(int(years.min()), int(years.max())), step=1)
countries_selection = pn.widgets.CheckBoxGroup(name='Countries', value=countries, options=countries)


def filterTable(data, selection):
    data.loc[data['country'].isin(selection)]
    return data.loc[data['country'].isin(selection)]

def scatter(data, country_selection, year_selection, x_selection, y_selection):
    filtered_data = filterTable(data, country_selection)
    filtered_data = filtered_data[(filtered_data['year'] >= year_selection[0]) & (filtered_data['year'] <= year_selection[1])]
    return filtered_data.hvplot(
                    x=x_selection, y=y_selection, 
                    by='country', 
                    kind='scatter', 
                    hover_cols=['country', 'suicide_no', 'gdp_per_capita ($)', 'year'], 
                    title='Relationship between Weight (kg) and Height (m), by Type',
                    width=700, height=500,
                    grid=True,
                    )

# w = a(data, countries)
x_scatter = pn.widgets.Select(name="X", options=list(data.columns))
y_scatter = pn.widgets.Select(name="Y", options=list(data.columns))
scatter_data = pn.bind(scatter, data, countries_selection, year_selection, x_scatter, y_scatter)  


sidebar=[
    pn.pane.Markdown('# About the project'),
    pn.pane.Markdown('#### This project uses data available on [Kaggle](https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420) and on [Wikipedia](https://en.wikipedia.org/wiki/Pok%C3%A9mon_(video_game_series)#Reception) about Pokémons to explore different types of visualizations using HoloViz tools: [Panel](https://panel.holoviz.org/) [hvPlot](https://hvplot.holoviz.org/)'),
    pn.pane.JPG('thimo-pedersen-dip9IIwUK6w-unsplash.jpg', sizing_mode='scale_both'),
    pn.pane.Markdown('[Photo by Thimo Pedersen on Unsplash](https://unsplash.com/photos/dip9IIwUK6w)'),
    pn.pane.Markdown('## Filter by Country'),
    countries_selection,
    year_selection
]

main = [
    pn.Row(scatter_data, pn.Column(x_scatter, y_scatter))
]
template = pn.template.FastListTemplate(theme=DarkTheme,
    sidebar=sidebar,
    main=main,
    title = 'Pokémon Interactive Dashboard',
    accent_base_color='#d78929',
    header_background='#d78929',
    sidebar_footer='<br><br><a href="https://github.com/pcmaldonado/PokemonDashboard">GitHub Repository</a>',       
    main_max_width='100%'                                        
)

template.servable()
template.show()