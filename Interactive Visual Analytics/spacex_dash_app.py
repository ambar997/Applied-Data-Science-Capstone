# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
x= spacex_df['Launch Site'].unique()
x=np.insert(x,0,'All Sites')
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                       dcc.Dropdown(id='site-dropdown', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[{'label': i, 'value': i} for i in x],
                                                     placeholder="Select a Launch Site here",
                                                     searchable= True,
                                                     style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                            ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                        dcc.RangeSlider(
                                                        id='payload-slider',
                                                        min=0,
                                                        max=10000,
                                                        step=1000,
                                                        marks={
                                                                0: '0',
                                                                2500: '2500',
                                                                5000: '5000',
                                                                7500: '7500',
                                                                10000: '10000'
                                                                },
                                                        value=[min_payload, max_payload]
                                                        ),]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value')],
               )
# Add computation to callback function and return graph
def get_pie(i1):
    
    if i1 == 'All Sites':
        pie_fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    elif i1 == 'CCAFS LC-40':
        spacex_df1= spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        pie_fig = px.pie(spacex_df1, names='class', title='Total Success Launches for site CCAFS LC-40')
    elif i1 == 'CCAFS SLC-40':
        spacex_df2= spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        pie_fig = px.pie(spacex_df2, names='class', title='Total Success Launches by site CCAFS SLC-40')
    elif i1 == 'KSC LC-39A':
        spacex_df3= spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        pie_fig = px.pie(spacex_df3, names='class', title='Total Success Launches by site KSC LC-39A')
    elif i1 == 'VAFB SLC-4E':
        spacex_df4= spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        pie_fig = px.pie(spacex_df4, names='class', title='Total Success Launches by site VAFB SLC-4E')
    
    return pie_fig
    



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")],
               )
# Add computation to callback function and return graph
def get_slid(i1,i2):
    low, high = i2
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)

    if i1 == 'All Sites':
        slid_fig = px.scatter(
        spacex_df[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category", title='Correlation between payload and launch success for All Sites')

    elif i1 == 'CCAFS LC-40':
        spacex_df1= spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        slid_fig = px.scatter(
        spacex_df1[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category", title='Correlation between payload and launch success for CCAFS LC-40')

    elif i1 == 'CCAFS SLC-40':
        spacex_df2= spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        slid_fig = px.scatter(
        spacex_df2[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category", title='Correlation between payload and launch success for CCAFS SLC-40')

    elif i1 == 'KSC LC-39A':
        spacex_df3= spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        slid_fig = px.scatter(
        spacex_df3[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category", title='Correlation between payload and launch success for KSC LC-39A')

    elif i1 == 'VAFB SLC-4E':
        spacex_df4= spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        slid_fig = px.scatter(
        spacex_df4[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category", title='Correlation between payload and launch success for VAFB SLC-4E')
    
    return slid_fig


# Run the app
if __name__ == '__main__':
    app.run_server(host="localhost", port=8060, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
