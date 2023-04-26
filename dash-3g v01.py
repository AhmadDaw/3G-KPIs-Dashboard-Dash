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

#df_ta=extract_cel_nam(df_ta)
#df_rlf=extract_cel_nam(df_rlf)

df_zt=df.groupby('Cell')['CS Traffic (Erl)'].sum()
count_cells_zt = (df_zt == 0).sum()
print(df_zt.head(10))
# --------------------------------------------------------
# ----------------------------------
ta_mae=["S4400A:Number of MRs (TA = 0) (None)","S4401A:Number of MRs (TA = 1) (None)","S4402A:Number of MRs (TA = 2) (None)","S4403A:Number of MRs (TA = 3) (None)","S4404A:Number of MRs (TA = 4) (None)","S4405A:Number of MRs (TA = 5) (None)","S4406A:Number of MRs (TA = 6) (None)","S4407A:Number of MRs (TA = 7) (None)","S4408A:Number of MRs (TA = 8) (None)","S4409A:Number of MRs (TA = 9) (None)","S4410A:Number of MRs (TA = 10) (None)","S4411A:Number of MRs (TA = 11) (None)","S4412A:Number of MRs (TA = 12) (None)","S4413A:Number of MRs (TA = 13) (None)","S4414A:Number of MRs (TA = 14) (None)","S4415A:Number of MRs (TA = 15) (None)","S4416A:Number of MRs (TA = 16) (None)","S4417A:Number of MRs (TA = 17) (None)","S4418A:Number of MRs (TA = 18) (None)","S4419A:Number of MRs (TA = 19) (None)","S4420A:Number of MRs (TA = 20) (None)","S4421A:Number of MRs (TA = 21) (None)","S4422A:Number of MRs (TA = 22) (None)","S4423A:Number of MRs (TA = 23) (None)","S4424A:Number of MRs (TA = 24) (None)","S4425A:Number of MRs (TA = 25) (None)","S4426A:Number of MRs (TA = 26) (None)","S4427A:Number of MRs (TA = 27) (None)","S4428A:Number of MRs (TA = 28) (None)","S4429A:Number of MRs (TA = 29) (None)","S4430A:Number of MRs (TA = 30 or 31) (None)","S4432A:Number of MRs (TA = 32 or 33) (None)","S4434A:Number of MRs (TA = 34 or 35) (None)","S4436A:Number of MRs (TA = 36 or 37) (None)","S4438A:Number of MRs (TA = 38 or 39) (None)","S4440A:Number of MRs (TA = 40 to 44) (None)","S4445A:Number of MRs (TA = 45 to 49) (None)","S4450A:Number of MRs (TA = 50 to 54) (None)","S4455A:Number of MRs (TA = 55 to 63) (None)","S4463A:Number of MRs (TA greater than 63) (None)"]

ta_m=["0.55 Km","1.1 Km","1.650 Km","2.2 Km","2.75 Km","3.3 Km","3.85 Km","4.4 Km","4.950 Km","5.5 Km","6.050 Km","6.6 Km","7.150 Km","7.7 Km","8.250 Km","8.8 Km","9.350 Km","9.9 Km","10.450 Km","11 Km","11.55 Km","12.1 Km","12.65 Km","13.2 Km","13.75 Km","14.3 Km","14.85 Km","15.4 Km","15.95 Km","16.5 Km","17.6 Km","18.7 Km","19.8 Km","20.9 Km","22 Km","24.75 Km","27.5 Km","28.6 Km","30.25 Km", '35.2 Km']

res = dict(zip(ta_mae, ta_m))
#df_ta.rename(columns=res, inplace=True)

# ----------------------------------
# --------------------------------------------------------
cells_list=df['Cell'].unique()
cells_list.sort()
list_dic=list()
a=0
for c in cells_list:
    d={'label':c,'value':c}
    list_dic.append(d)

g_dic={'label':'2G','value':2,
        'label':'3G','value':3,
        'label':'4G','value':4}

# --------------------------------------------------------
'''col_name=df_ta.columns[3]
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

# *********************************************************

col_name=df_rlf.columns[3]
appended_rlf=list()
for c in cells_list:
    dft=df_rlf[df_rlf[str(col_name)]==c]
    s1 = pd.Series([c],index=['Cell Name'])
    df_sum=dft.iloc[:,4:].sum()
    s1=s1.append(df_sum)
    appended_rlf.append(s1)
    
app_rlf = pd.concat(appended_rlf,axis=1)
app_rlf = app_rlf.transpose()
# -----------------------------------------------
app_rlf=app_rlf.set_index('Cell Name')
app_rlf = app_rlf.transpose()
app_rlf=app_rlf.reset_index()
app_rlf.rename(columns={'index': 'RLF'}, inplace=True)
# --------------------------------------------------------
'''
# ----------------------------------------
card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

card_zt = [
    dbc.CardHeader("Zero traffic"),
    dbc.CardBody(
        [
            html.H5(str(count_cells_zt), className="card-title"),
            dbc.CardLink("Number of cells with zero traffic.", href="#",style="text-decoration: none"),
            dbc.Button("Number of cells with zero traffic.", color="danger", className="mt-auto", href="#")
        ]
    ),
]

card_ht = [
    dbc.CardHeader("Highest CS/PS traffic"),
    dbc.CardBody(
        [
            html.H5(' ', className="card-title"),
            html.P(
                "Highest traffic cells.",
                className="card-text",
            ),
        ]
    ),
]
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
    #dfta=app_df.loc[:,str(column_chosen)]
    # ---------------------------------------------
    dff=df.copy()
    dff=dff[dff['Cell']==column_chosen]
    dff.sort_values(by=['Start Time'],inplace=True)
    #dff_ta=df_ta[df_ta['Cell']==column_chosen]
    #dff_ta.sort_values(by=['Start Time'],inplace=True)
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

