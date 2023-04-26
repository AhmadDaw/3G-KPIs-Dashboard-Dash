import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import pandas as pd
from extract_cell_name import extract_cel_nam

app = dash.Dash()

# ---------------------------------------------------------------

df=pd.read_excel('3g-kpis.xlsx')
graph1='CS Traffic (Erl)'
graph2='Mean HSDPA UE in Cell'
graph3='RRC Setup Success Ratio (Service) (%)'
graph4='RRC Setup Success Ratio (Other) (%)'
graph5='HSDPA MAC-d MegaByte (MB)'
graph6='HSDPA RLC Throughput (kbit/s)'
graph7='CS Call Drop Rate (%)'
graph8='PS Call Drop Rate (%)'
graph9='CS RAB Assignment Success Rate (%)'
graph10='PS RAB Assignment Success Rate (%)'

df=extract_cel_nam(df)
df.rename(columns={'VS.RAB.AMR.Erlang.cell (Erl)': 'CS Traffic (Erl)',
                    'Radio_CS Inter-Rat Handover Success Rate (%)': 'CS Inter-Rat Handover SR (%)',
                    '{Upgrade}RRC Setup Success Ratio (Service) (%)': 'RRC Setup Success Ratio (Service) (%)',
                    '{Upgrade}RRC Setup Success Ratio (Other) (%)':'RRC Setup Success Ratio (Other) (%)',
                    'VS.HSDPA.UE.Mean.Cell (None)':'Mean HSDPA UE in Cell',
                    'Radio_PS Call Drop Rate (%)':'PS Call Drop Rate (%)',
                    'Radio_CS Call Drop Rate (%)':'CS Call Drop Rate (%)',
                    'Radio_CS RAB Assignment Success Rate (%)':'CS RAB Assignment Success Rate (%)',
                    'Radio_PS RAB Assignment Success Rate (%)':'PS RAB Assignment Success Rate (%)'}
                    , inplace=True)


# --------------------------------------------------------

# --------------------------------------------------------
cells_list=df['Cell'].unique()
cells_list.sort()
list_dic=list()
a=0
for c in cells_list:
    d={'label':c,'value':c}
    list_dic.append(d)


# -----------------------------------------
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([html.Br()])
        ]),    
    dbc.Row([
        dbc.Col([html.H1("3G KPIs Dashboard", style={'textAlign': 'center'})
        ], width=12)
        ]),
    dbc.Row([
        dbc.Col([html.Br()])
        ]),
    dbc.Row(
            [
                dbc.Col(dbc.Card(card_zt, color="danger", inverse=True)),
                dbc.Col(dbc.Card(card_ht, color="success", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="primary", inverse=True)),
            ],
            className="mb-4",
        ),
    dbc.Row([
        dbc.Col([html.Br()])
        ]),
    dbc.Row([
            dcc.Dropdown(id='my_dropdown',
            options=list_dic,
            optionHeight=35,                    #height/space between dropdown options
            value='Borough',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph1')
        ]),
        dbc.Col([
            dcc.Graph(id='graph2')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph3')
        ]),
        dbc.Col([
            dcc.Graph(id='graph4')
        ])     
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph5')
        ]),
        dbc.Col([
            dcc.Graph(id='graph6')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph7')
        ]),
        dbc.Col([
            dcc.Graph(id='graph8')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph9')
        ]),
        dbc.Col([
            dcc.Graph(id='graph10')
        ])
    ])            
])


#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    [Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='graph3', component_property='figure'),
    Output(component_id='graph4', component_property='figure'),
    Output(component_id='graph5', component_property='figure'),
    Output(component_id='graph6', component_property='figure'),
    Output(component_id='graph7', component_property='figure'),
    Output(component_id='graph8', component_property='figure'),
    Output(component_id='graph9', component_property='figure'),
    Output(component_id='graph10', component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):

    dff=df.copy()
    dff=dff[dff['Cell']==column_chosen]
    dff.sort_values(by=['Start Time'],inplace=True)

    fig1 = px.line(data_frame=dff,x='Start Time',y=graph1, title=str(column_chosen))
    fig2 = px.line(data_frame=dff,x='Start Time',y=graph2, title=str(column_chosen))
    fig3 = px.line(data_frame=dff,x='Start Time',y=graph3, title=str(column_chosen),range_y=[0,110])
    fig4 = px.line(data_frame=dff,x='Start Time',y=graph4, title=str(column_chosen),range_y=[0,110])
    fig5 = px.line(data_frame=dff,x='Start Time',y=graph5, title=str(column_chosen))
    fig6 = px.line(data_frame=dff,x='Start Time',y=graph6, title=str(column_chosen))
    fig7 = px.line(data_frame=dff,x='Start Time',y=graph7, title=str(column_chosen),range_y=[0,110])
    fig8 = px.line(data_frame=dff,x='Start Time',y=graph8, title=str(column_chosen),range_y=[0,110])
    fig9 = px.line(data_frame=dff,x='Start Time',y=graph9, title=str(column_chosen),range_y=[0,110])
    fig10 = px.line(data_frame=dff,x='Start Time',y=graph10, title=str(column_chosen),range_y=[0,110])
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7 ,fig8, fig9 ,fig10
# -------------------------------------------------

if __name__ == '__main__':
    app.run_server()

