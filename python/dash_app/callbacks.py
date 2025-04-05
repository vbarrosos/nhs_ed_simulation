from dash import Input, Output, State, callback, dcc, html, callback_context, ClientsideFunction
from dash.dependencies import ALL
import dash_bootstrap_components as dbc
from models.simulation import run_simulation
from views.simulation_view import create_simulation_view, create_simulation_graph
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time

def register_callbacks(app):

    @app.callback(
        Output('simulation-container', 'children'),
        Output('alert-container', 'children'),
        Output('simulation-data-store', 'data'),
        Input('add-simulation-button', 'n_clicks'),
        Input({'type': 'remove-button', 'index': ALL}, 'n_clicks'),
        Input('simulation-parameters-table', 'data'),
        Input('simulation-parameters-table', 'columns'),
        Input('simulation-parameters-acuity-table', 'data'),
        Input('simulation-parameters-acuity-table', 'columns'),
        Input('simulation-start-date', 'date'),
        State('simulation-container', 'children'),
        State('simulation-data-store', 'data')
    )
    def manage_simulations(add_clicks, remove_clicks, rows, columns, rows_acuity, columns_acuity, start_date, children, simulation_data):
        ctx = callback_context
        if children is None:
            children = []
        if simulation_data is None:
            simulation_data = []
        alert = None
        if not ctx.triggered:
            return children, alert, simulation_data
        rows.append({'property':'START DATE', 'value':start_date})
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'add-simulation-button':
            if len(children) >= 3:
                alert = dbc.Alert("You can only add up to 3 simulations. Remove one of the simulations to continue.", color="warning")
                return children, alert, simulation_data
            simulation_dict = run_simulation(rows + rows_acuity)
            simulation_data.append(simulation_dict)
            simulation_id = len(simulation_data)
            new_simulation = create_simulation_view(add_clicks, simulation_id, simulation_dict, rows, columns, rows_acuity, columns_acuity)
            children.append(new_simulation)
            return children, alert, simulation_data
        elif 'remove-button' in button_id:
            button_id = eval(button_id)
            index_to_remove = button_id['index']
            children = [child for child in children if child['props']['id'] != f'simulation-div-{index_to_remove}']
            simulation_data = [sd for sd, child in zip(simulation_data,children) if child['props']['id'] != f'simulation-div-{index_to_remove}']
        return children, alert, simulation_data

    @app.callback(
        Output({'type': 'simulation-graph', 'index': ALL}, 'children'),
        Input('simulation-data-store', 'data'),
    )
    def update_graph(simulation_data):
        if simulation_data is not None:
            return create_simulation_graph(simulation_data)
        else:
            return []
        
    @app.callback(
        Output({'type': 'simulation-label', 'index': ALL}, 'children'),
        Input({'type': 'remove-button', 'index': ALL}, 'n_clicks'),
        State('simulation-container', 'children')   
    )
    def update_simulation_label(n_clicks, children):
        return [f"Simulation {ch+1}" for ch in range(len(children))]
    
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='generate_pdf_function'
        ),
        Input('download-btn', 'n_clicks'),
        prevent_initial_call=True)