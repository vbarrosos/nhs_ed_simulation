from dash import dcc, html
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from views.table_view import create_selected_parameters_table, create_selected_parameters_acuity_table, create_simulation_results_table
import pandas as pd

def create_simulation_view(add_clicks, simulation_id, simulation_dict, rows, columns, rows_acuity, columns_acuity):
    return html.Div([
                html.Div([
                    html.Div([
                        html.H2(f'Simulation {simulation_id}',  style={'margin-bottom': '0%'}, className="text-primary", id={'type': 'simulation-label', 'index': add_clicks}),
                        html.Button('Remove', id={'type': 'remove-button', 'index': add_clicks}, style={'margin-left': '5px'}, className="btn btn-danger")
                     ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between', 'margin-bottom': '2%'}),
                    dbc.Accordion([
                        dbc.AccordionItem([
                                create_selected_parameters_table(rows),
                                create_selected_parameters_acuity_table(rows_acuity, columns_acuity)
                            ], title=html.H4(f'Selected Parameters', style={'margin':'0px','white-space': 'nowrap'}),
                        ),
                        dbc.AccordionItem(
                            create_simulation_results_table(simulation_dict)
                            +[html.Div(id={'type': 'simulation-graph', 'index': add_clicks})],
                            title=html.H4('Results', style={'margin':'0px','white-space': 'nowrap'}),
                        )
                    ], start_collapsed=False, style={"accordion-button":{'padding':'0px'}}, flush=True, always_open=True,
                    )
                ], style={'display': 'flex', 'flexDirection': 'column', 'width': '100%'}),
                # html.H4(f'Simulation results',  style={'margin-top': '1%', 'margin-bottom': '0%'}),
                # html.Div(id={'type': 'simulation-graph', 'index': add_clicks}),
            ], style={'display': 'inline-block', 'width': '32.5%', 'margin': '0.5%', 'padding': '1%'}, 
            id=f'simulation-div-{add_clicks}', className='bg-body-tertiary'
            )
    
def create_simulation_graph(simulation_data):
    plot_keys = ['Bed Usage', 'Queue Lengths', 'Total Occupancy', 'Average Wait Time']
    figs = []
    for sd in simulation_data:
        fig = make_subplots(rows=4, cols=1, 
                            shared_xaxes=True,
                            vertical_spacing=0.01
                            )
        fig.update_layout(
            legend_title_text="Acuity",
            legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1,
            ),
            margin=dict(
                t=60,
                b=1,
                r=1,
                l=1
            ),
            # paper_bgcolor='#f8f9fa',
            )
        df = pd.DataFrame(sd)
        for ii,key in enumerate(plot_keys): 
            lines = px.line(df,x="Time",y=key,color="Acuity")
            for trace in range(len(lines["data"])):
                lines["data"][trace]["showlegend"] = False if ii>0 else True
                fig.append_trace(lines["data"][trace],row=ii+1,col=1)
            fig.update_yaxes(title_text=key, row=ii+1, col=1)
        fig.update_xaxes(title_text="Time", row=ii+1, col=1)
        figs.append(dcc.Graph(figure=fig, style={'height': '800px', 'margin': '0px'}, config={'displayModeBar': True}))
    return figs
