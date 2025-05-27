import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize app
app = dash.Dash(__name__)
server = app.server

# Prepare dropdown options
launch_sites = [{'label': 'All Sites', 'value': 'All Sites'}] + [
    {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
]

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={
        'textAlign': 'center', 'color': '#503D36', 'fontSize': 40
    }),

    dcc.Dropdown(
        id='site_dropdown',
        options=launch_sites,
        value='All Sites',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload_slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: f'{i} kg' for i in range(0, 10001, 1000)}
    ),
    html.Br(),

    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site_dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Total Successful Launches by All Sites',
            hole=0.3
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Launch Outcomes for Site: {selected_site}',
            hole=0.3
        )
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'),
     Input('payload_slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] > low) &
        (spacex_df['Payload Mass (kg)'] < high)
    ]
    if selected_site != 'All Sites':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        size='Payload Mass (kg)',
        hover_data=['Payload Mass (kg)']
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
