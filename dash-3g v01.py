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
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#load_figure_template("darkly")

# ---------------------------------------------------------------

df=pd.read_excel('3g-kpis.xlsx')
df_ta=pd.read_excel('3g-ta.xlsx')

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

df_ta=extract_cel_nam(df_ta)

# --------------------------------------------------------

ta_mae=['VS.TP.UE.0 (None)','VS.TP.UE.1 (None)','VS.TP.UE.2 (None)','VS.TP.UE.3 (None)', 'VS.TP.UE.4 (None)','VS.TP.UE.5 (None)','VS.TP.UE.6.9 (None)','VS.TP.UE.10.15 (None)','VS.TP.UE.16.25 (None)','VS.TP.UE.26.35 (None)','VS.TP.UE.36.55 (None)','VS.TP.UE.More55 (None)']

ta_m=["234 m","468 m","702 m","936 m","1170 m","1404 m","2340 m","3744 m","6084 m","8424 m","13104 m","17784 m"]
#ta_dist=[234,468,702,936,1170,1404,2340,3744,6084,8424,13104,17784]
res = dict(zip(ta_mae, ta_m))
df_ta.rename(columns=res, inplace=True)

# --------------------------------------------------------
cells_list=df['Cell'].unique()
cells_list.sort()
list_dic=list()
a=0
for c in cells_list:
    d={'label':c,'value':c}
    list_dic.append(d)

# --------------------------------------------------------
col_name=df_ta.columns[3]
appended_data=list()
for c in cells_list:
    dft=df_ta[df_ta[str(col_name)]==c]
    s1 = pd.Series([c],index=['Cell Name'])
    df_sum=dft.iloc[:,4:].sum()
    s1=s1.append(df_sum)
    appended_data.append(s1)
    
app_df = pd.concat(appended_data,axis=1)
app_df = app_df.transpose()
# -----------------------------------------------
app_df=app_df.set_index('Cell Name')
app_df = app_df.transpose()
app_df=app_df.reset_index()
app_df.rename(columns={'index': 'TA'}, inplace=True)

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
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph11')
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
    Output(component_id='graph10', component_property='figure'),
    Output(component_id='graph11', component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    #dfta=app_df.loc[:,str(column_chosen)]
    # ---------------------------------------------
    dff=df.copy()
    dff=dff[dff['Cell']==column_chosen]
    dff.sort_values(by=['Start Time'],inplace=True)
    dff_ta=df_ta[df_ta['Cell']==column_chosen]
    dff_ta.sort_values(by=['Start Time'],inplace=True)
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
    fig11=px.bar(data_frame=app_df, x='TA',y=column_chosen)
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7 ,fig8, fig9 ,fig10, fig11
# -------------------------------------------------

if __name__ == '__main__':
    app.run_server()

