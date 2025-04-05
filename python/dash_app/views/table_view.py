from dash import dcc, html, dash_table
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
from utils.ref_parameters import ACUITIES, SIMULATION_PARAMETERS, SIMULATION_PARAMETERS_ACUITY
import pandas as pd

def create_table_view(table_id, columns_list, data_list, editable=False, **kwargs):
    return dash_table.DataTable(
            id=table_id,
            columns=columns_list,
            data=data_list,
            editable=editable,
            style_header={'fontWeight': 'bold'},
            style_cell={'text-align': 'center',
                        'padding-right': '5px', 
                        'padding-left': '5px',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                        },
            **kwargs
        )
    
def create_parameters_table():
    id='simulation-parameters-table'
    columns=[{'name': 'Property', 'id': 'property', 'editable': False}, {'name': 'Value', 'id': 'value', 'type': 'numeric'}]
    data=[dict(property=key, **{'value': val}) 
            for key,val in SIMULATION_PARAMETERS.items()
        ]
    editable=True
    style_data_conditional=[{
                'if': {'column_editable': False},
                'fontWeight': 'bold'
            }]
    style_table={'margin-right': '5%',
                 'overflowX': 'auto'
                 }
    style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
                }
    return create_table_view(id, columns, data, editable=editable, style_data_conditional=style_data_conditional, style_table=style_table, style_data=style_data)

def create_parameters_acuity_table():
    id='simulation-parameters-acuity-table'
    columns=[{'name': 'ACUITY', 'id': 'acuity', 'editable': False}]+[{'name': key, 'id': key.lower().replace(' ', '_'), 'type': 'numeric'} for key in SIMULATION_PARAMETERS_ACUITY.keys()]
    data=[dict(acuity=acuity, 
            **{key.lower().replace(' ', '_'): value[acuity] for key, value in SIMULATION_PARAMETERS_ACUITY.items()}) 
        for acuity in ACUITIES
        ]
    editable=True
    style_data_conditional=[{
                'if': {'column_editable': False},
                'fontWeight': 'bold'
            }]
    style_table={'margin': '1%',
                 'overflowX': 'auto'
                 }
    style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
                }
    return create_table_view(id, columns, data, editable=editable, style_data_conditional=style_data_conditional, style_table=style_table, style_data=style_data)

def create_selected_parameters_table(rows):
    id='simulation-selected-parameters-table'
    columns = [{'name': 'Property', 'id': 'property'}]+[{'name': row['property'], 'id':row['property']} for row in rows]
    data= [{row['property']: row['value'] for row in [{'property':'property', 'value':'Value'}]+rows}]
    style_data_conditional=[{
                'if': {'column_id': 'property'},
                'fontWeight': 'bold'
            }]
    style_table={'margin': '0%',
                 'overflowX': 'scroll',
                 'height': '100%',
                 'font_size': '10pt',
                 }
    style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                }
    return create_table_view(id, columns, data, style_data_conditional=style_data_conditional, style_table=style_table, style_data=style_data)

def create_selected_parameters_acuity_table(rows, columns):
    id='simulation-selected-parameters-acuity-table'
    columns = [{'name': col['name'], 'id':col['id']} for col in columns]
    data = rows
    style_data_conditional=[{
                'if': {'column_id': 'ACUITY'},
                'fontWeight': 'bold'
            }]
    style_table={'margin-top': '1%',
                 'overflowX': 'scroll',
                 'height': '100%',
                 'font_size': '10pt',
                 }
    style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                }
    return create_table_view(id, columns, data, style_data_conditional=style_data_conditional, style_table=style_table, style_data=style_data)

def create_simulation_results_table(simulation_data):
    id='simulation-results-table'
    df = pd.DataFrame(simulation_data)
    desc_df = df.groupby(["Acuity"]).describe()
    properties = desc_df.columns.get_level_values(0).unique()
    out_tables = []
    for ii,property in enumerate(properties[:4]):
        id = id+f'-{ii+1}'
        columns = [{'name':[property,desc_df[property].index.name], 'id':desc_df[property].index.name}]
        for col in desc_df[property].columns:
            format=Format(precision=2, scheme=Scheme.decimal)
            columns += [{'name': [property,col], 'id': str(col), 'type':'numeric', 'format':format}]
        data = [{'Acuity':acuity, **{str(col):desc_df[property][col][acuity] for col in desc_df[property].columns}} for acuity in desc_df[property].index]
        style_data_conditional=[{
                    'if': {'column_id': 'ACUITY'},
                    'fontWeight': 'bold'
                }]
        style_table={'margin-top': '1%',
                    'overflowX': 'scroll',
                    'height': '100%',
                    'font_size': '10pt',
                    }
        style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    }
        out_tables.append(create_table_view(id, columns, data, style_data_conditional=style_data_conditional, style_table=style_table, style_data=style_data, merge_duplicate_headers=True,))
    return out_tables