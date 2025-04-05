# from dash import dcc, html, dash_table
from dash_extensions.enrich import DashProxy, html, Output, Input, dcc
import dash_bootstrap_components as dbc
from datetime import date, datetime
from views.table_view import create_parameters_table, create_parameters_acuity_table

def create_layout():
    return html.Div([
        html.Div([
        html.H2('Simulation Parameters',  style={'margin': '1%'}, className="text-primary"),
        html.H5(id='container-output-text', 
                children='Enter values in the table below and press "Add Simulation" to run a simulation.',
                style={'margin': '1%', 'margin-bottom': '0%'}
                ),
        html.Div([
            html.Div([
                create_parameters_table(),
                create_parameters_acuity_table(),
            ], style={'margin': '1%', 'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between', 'align-items': 'center'}
                     ),
            html.Div([
                html.H5("Choose a start date for the simulation: "),
                dcc.DatePickerSingle(
                    id='simulation-start-date',
                    min_date_allowed=date(1995, 1, 1),
                    initial_visible_month=datetime.today(),
                    date=date(2024,1,1),
                    display_format='DD-MM-YYYY',
                    clearable=True
                )
            ], style={'margin': '1%'}),
        ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between'}),
        html.Button('Add Simulation', id='add-simulation-button', 
                    n_clicks=0, style={'margin': '1%', 'margin-top': '0%'},
                    className="btn btn-primary btn-lg"),
        html.Button("Download PDF", id='download-btn', 
                    n_clicks=0, style={'margin': '1%', 'margin-top': '0%'},
                    className="btn btn-primary btn-lg"),
        ], className="bg-light", style={'width': 'window','margin': '2%'}),
        html.Div(id='alert-container', style={'margin': '2%', 'width': '40%'}),
        html.Div(id='simulation-container', style={'width': 'window', 'margin': '1.5%', 'display': 'flex', 'flexDirection': 'row'}),
        dcc.Store(id='simulation-data-store'),
    ])
