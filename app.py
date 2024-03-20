# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   Graph DOES NOT need to interact with dropdown or slider
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# import dependencies
import dash
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

# %%
# load the dataset
df = pd.read_csv("gdp_pcap.csv")

# %%
# reshape dataframe 
melted_df = df.melt(id_vars=['country'], var_name = 'year', value_name = 'gdpPercap')
melted_df['year'] = pd.to_numeric(melted_df['year']) #year to numeric
 # makes this so that there is a year and gdp calculated column

# %%
# initialize the dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# %%
# Define the layout of the app
app.layout = html.Div([
    html.H1(children="Gapminder GDP Per Capita Explorer"), #title
    html.P("Explore GDP per capita data from the Gapminder dataset. Use the slider to select the years. Use the drop down menu to select the countries you want to look at"), #description
    html.Div([
        # Dropdown menu for selecting countries
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in melted_df['country'].unique()],# make sure countries are not repeated 
            multi=True,
            value=['Afghanistan']  # Default selected countries, otherwise presents an error
        ),
        html.Label("slide for year"), #label 
        # Slider for selecting years
        dcc.RangeSlider(
            id='year-slider',
            min=melted_df['year'].min(), # minimum year value
            max=melted_df['year'].max(), # maximum year value 
            step = 1,
            value=[melted_df['year'].min(), melted_df['year'].max()], # default
            marks={year: str(year) for year in range(melted_df['year'].min(), melted_df['year'].max() + 1, 100)},
            tooltip = {"placement":"bottom", "always_visible":True},
        )
    ]),
    
    # Graph for displaying GDP per capita, line 
    dcc.Graph(id='gdp-per-capita-graph')
]) 

# Define callback to update graph based on user inputs
@app.callback(
    Output('gdp-per-capita-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_years):
    # Filter data based on selected countries and years
    filtered_df = melted_df[(melted_df['country'].isin(selected_countries)) & 
                            (melted_df['year'].astype(int).between(selected_years[0], selected_years[1]))]
    sorted_df = filtered_df.sort_values(by=['year', 'gdpPercap'])
    # Create traces for each selected country
    traces = []
    for country in selected_countries:
        country_data =filtered_df[filtered_df['country'] == country]
        traces.append(dict(
            x=country_data['year'],
            y=country_data['gdpPercap'],
            mode='lines',
            name=country
        ))

    # Define layout for the graph
    layout = dict(
        title='GDP Per Capita Over Time',
        xaxis={'title': 'Year'},
        yaxis={'title': 'GDP Per Capita'}
    )

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)



