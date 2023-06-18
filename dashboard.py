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

pn.extension()


# Preprocessing data
data = pd.read_csv('master.csv', thousands=',')
data['suicides_no'] = pd.to_numeric(data['suicides_no'])
data[' gdp_for_year ($) '] = pd.to_numeric(data[' gdp_for_year ($) '])

data['age'] = data['age'].map(lambda x: x.replace("years", ""))
data['age'] = data['age'].map(lambda x: x.replace("5-14", "05-14"))
print(data.columns)
pn.extension()
pd.options.plotting.backend = 'holoviews'

countries = list(data['country'].unique())
ages = list(data['age'].unique())
ages.sort()

years = np.array(data['year'].unique())


year_selection = pn.widgets.IntRangeSlider(name='Period to visualize', start=int(years.min()), end=int(years.max()), value=(int(years.min()), int(years.max())), step=1)
countries_selection = pn.widgets.CheckBoxGroup(name='Countries', value=countries, options=countries)
group_selection = pn.widgets.CheckBoxGroup(name='Group', value=['age', 'sex'], options=['age', 'sex'])
age_selection = pn.widgets.CheckBoxGroup(name='Group', value=ages, options=ages)

order_selection = pn.widgets.Select(name='Sort By', value='suicides/100k pop', options=['suicides_no', 'suicides/100k pop', 'population', 'HDI for year', ' gdp_for_year ($) ', 'gdp_per_capita ($)'])

def filterTable(data, selection):
    return data.loc[data['country'].isin(selection)]

def scatter(data, country_selection, year_selection, x_selection, y_selection):
    filtered_data = filterTable(data, country_selection)
    filtered_data = filtered_data[(filtered_data['year'] >= year_selection[0]) & (filtered_data['year'] <= year_selection[1])]
    return filtered_data.sort_values(by=[x_selection], ascending=True).hvplot(
                    x=x_selection, y=y_selection, 
                    by='country', 
                    kind='scatter', 
                    hover_cols=['country', 'suicide_no', 'gdp_per_capita ($)', 'year'], 
                    title='Relationship between Weight (kg) and Height (m), by Type',
                    width=700, height=500,
                    grid=True,
                    )

def sex_plot(data, country_selection, year_selection, group_by, age_selection):
    gp = group_by + ["year"]
    filtered_data = filterTable(data, country_selection)
    filtered_data = filtered_data[(filtered_data['year'] >= year_selection[0]) & (filtered_data['year'] <= year_selection[1])]
    filtered_data = filtered_data.loc[data['age'].isin(age_selection)]
    filtered_data = filtered_data.groupby(gp, as_index = False)["suicides_no"].mean()
    return filtered_data.hvplot(
                    x='year', 
                    y=['suicides_no'],
                    by=group_by, 
                    kind='line', 
                    # hover_cols=['suicide_no', 'gdp_per_capita ($)', 'year'], 
                    title='Relationship between Weight (kg) and Height (m), by Type',
                    width=700, height=500,
                    grid=True,
                    )

def ranking_plot(data, country_selection, year_selection, order_selection):
    filtered_data = filterTable(data, country_selection)
    filtered_data = filtered_data[(filtered_data['year'] >= year_selection[0]) & (filtered_data['year'] <= year_selection[1])]
    filtered_data = filtered_data.groupby(['country'], as_index = False).mean(numeric_only=True).sort_values(by=order_selection, ascending=True)
    return filtered_data.hvplot(
                    'country', 
                    'suicides/100k pop',
                    kind='barh', 
                    title='Relationship between Weight (kg) and Height (m), by Type',
                    width=700, height=500, color="suicides/100k pop", colorbar=True, clabel="Weight", cmap="bmy"
                    )

# w = a(data, countries)
x_scatter = pn.widgets.Select(name="X", options=list(data.columns))
y_scatter = pn.widgets.Select(name="Y", options=list(data.columns))

scatter_data = pn.bind(scatter, data, countries_selection, year_selection, x_scatter, y_scatter)  
line_data = pn.bind(sex_plot, data, countries_selection, year_selection, group_selection, age_selection)  
ranking_data = pn.bind(ranking_plot, data, countries_selection, year_selection, order_selection)  

sidebar=[
    pn.pane.Markdown('# About the project'),
    pn.pane.Markdown('#### This project uses data available on [Kaggle](https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420) and on [Wikipedia](https://en.wikipedia.org/wiki/Pok%C3%A9mon_(video_game_series)#Reception) about Pokémons to explore different types of visualizations using HoloViz tools: [Panel](https://panel.holoviz.org/) [hvPlot](https://hvplot.holoviz.org/)'),
    pn.pane.JPG('thimo-pedersen-dip9IIwUK6w-unsplash.jpg', sizing_mode='scale_both'),
    pn.pane.Markdown('[Photo by Thimo Pedersen on Unsplash](https://unsplash.com/photos/dip9IIwUK6w)'),
    pn.pane.Markdown('## Filter by Country'),
    year_selection,
    countries_selection
]

main = [
    pn.Row(
            scatter_data, 
            pn.Column(
                    x_scatter,
                    y_scatter
                    )
            ),
    pn.Row(
            line_data, 
            pn.Column(
                    pn.pane.Markdown('Groups'),
                    group_selection,
                    pn.pane.Markdown('Age interval'),
                    age_selection
                    )
            ),
    pn.Row(
            ranking_data, 
            pn.Column(
                    pn.pane.Markdown('Sort By'),
                    order_selection,
                    )
            )
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