# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
# from dash import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# prepare dropdown options
unique_launch_sites = list(spacex_df['Launch Site'].unique())
dropdown = {}
dropdown['All Sites'] = 'ALL'
for site in unique_launch_sites:
    dropdown[site] = site

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown,
                                    value='ALL',
                                    placeholder='Select Launch Site',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0:'0', 1000:'1000',
                                     2000:'2000',3000:'3000',4000:'4000',
                                     5000:'5000',6000:'6000',
                                     7000:'7000',8000:'8000',9000:'9000',10000:'10000'},
                                    value=[min_payload,max_payload]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def make_pie_chart(launch_site):
    print(f'given launch site is: {launch_site}')
    if launch_site != 'All Sites':
        df_launch = spacex_df[spacex_df['Launch Site']==launch_site]
        df = pd.pivot_table(values='Flight Number',index='class',aggfunc='count',data=df_launch)
        names_ = 'class'        
    else:
        df_launches_total = spacex_df[spacex_df['class']==1]
        df = pd.pivot_table(values='Flight Number', index='Launch Site', aggfunc='count',data=df_launches_total)
        names_ = 'Launch Site'
    df.reset_index(inplace=True)
    df.rename(columns={'Flight Number': 'Number of Flights'},inplace=True)
    print(df.head())
    # x = np.array(df['Flight Number'])
    fig = px.pie(df,
        values='Number of Flights',
        names=names_,
        title=f'Successes for Launch Site:  {launch_site}'
        )

    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property='value')]
)
def make_scatter(launch_site, payload_):
    if launch_site == 'All Sites':
        # no filter on sites
        df = spacex_df
    else:
        # one site
        df = spacex_df[spacex_df['Launch Site']==launch_site]
    plm = 'Payload Mass (kg)' # use short variable for readability.
    # filter for the payload range that is given.
    df = df[(df[plm]>=payload_[0]) & (df[plm]<=payload_[1])]
    fig = px.scatter(
        data_frame=df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
