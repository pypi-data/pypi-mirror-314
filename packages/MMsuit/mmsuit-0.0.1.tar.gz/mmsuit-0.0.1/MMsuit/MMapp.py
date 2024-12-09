import MMsuit.MMcalc as mm
from dash import dash, dcc, html, Output, Input, State
import pandas as pd
import numpy as np
import base64
import io
import plotly.graph_objects as go

#Intialize data storage variable
uploaded = None

#Initialize Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

#Dash Layout
app.layout = html.Div([html.H1(children='MMsuit: Michaelis-Menten Suit', style={"textAlign": "center", "marginBottom": "20px"}),
                       html.Div([dcc.Tabs(id="tabs", value='tab-1', children=[dcc.Tab(label='ExperimentExecuter', value='tab-1'),
                                                                               dcc.Tab(label='Simulator', value='tab-2'),])]),
                       html.Div(id='tabs-content')],
                      style={"border": "5px solid purple",  # Purple border
                             "padding": "20px",
                             "backgroundColor": "#4B2E83",  # UW Huskies Purple background
                             "color": "#D4AF37",  # Gold text color
                             "fontFamily": "Arial, sans-serif"})
# Callback function to switch content based on the selected tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([html.H3(children='Upload your data as Substrate in one column and Velocity in the other column\nMMsuit fits your data to Michaelis-Menten and LineWeaver-Burk equations'),
                       dcc.Upload(id = 'upload-input',
                                  children= html.Button('Upload'), multiple=False),
                       html.Div(id='upload-output', style={"marginTop": "10px", "color": "#D4AF37"}),
                       html.Div([
                           ## Michaelis-Menten plot
                           html.Div([dcc.Markdown('''
                           ***Michaelis-Menten equation***\n
                           $V = Vmax*[S]/(Km + [S])$\n
                           $V$: velocity, $Vmax$: Maximum velocity, $S$: substrate concentration, $Km$: Michaelis-Menten constant
                           ''',mathjax=True, style={"color": "#D4AF37"}),
                                     dcc.Graph(id='MM-plot')],style={"width": "48%", "display": "inline-block"}),
                           ## Linweaver-Burk plot
                           html.Div([dcc.Markdown('''
                                                      ***Lineweaver-Burk equation***\n
                                                      $1/V = (Km/Vmax)*(1/S)+(1/Vmax)$\n
                                                      $V$: velocity, $Vmax$: Maximum velocity, $S$: substrate concentration, $Km$: Michaelis-Menten constant
                                                      ''',mathjax=True ,style={"color": "#D4AF37"}),
                                     dcc.Graph(id='LB-plot')],style={"width": "48%", "display": "inline-block"})],
                                  style={"display": "flex", "justify-content": "space-between"}),

                       ## Display Km and Vmax
                       html.Div([html.Div([html.Label("Vmax:"),
                                       dcc.Input(id="vmax-box",type="text",value="N/A",readOnly=True,
                                           style={"width": "100px", "backgroundColor": "white", "color": "black"})],
                                   style={"display": "inline-block", "marginRight": "20px"}),
                                        html.Div([html.Label("Km:"),
                                       dcc.Input(id="km-box",type="text",value="N/A",readOnly=True,
                                           style={"width": "100px", "backgroundColor": "white", "color": "black"})],
                                   style={"display": "inline-block"}),
                                        ],
                           style={"marginBottom": "20px", "color": "#D4AF37", "textAlign": "center"},
                       ),

                       ## (Optional) Display Kcat
                       html.Div([
                           html.Label("Enter Enzyme Concentration (µM):", style={'font-weight': 'bold'}),
                           dcc.Input(id='enzyme-conc', type='number', min=0, step=0.1, placeholder="Enter value"),
                           html.Button('Compute kcat', id='compute-kcat', n_clicks=0, style={'margin-left': '10px'}),
                           html.Div(id='kcat-output', style={'margin-top': '10px', 'font-weight': 'bold'}),
                       ])])
    ## Michaelis-Menten Simulator
    elif tab == 'tab-2':
        return html.Div([html.Div([html.H3(children='Simulate Michaelis-Menten plot by inserting Km and Vmax'),
                           ## Km
                               html.Label("Enter Km:"),
                               dcc.Input(id="input-km", type="number", placeholder="Enter a positive number", min=0, step=0.01),
                           ## Vmax
                               html.Label("Enter Vmax:", style={"marginLeft": "12px"}),
                               dcc.Input(id="input-vmax", type="number", placeholder="Enter a positive number", min=0, step=0.01),
                               html.Button("Michaelis-Menten Simulator", id="button-michaelis-menten",n_clicks=0,
                                   style={"marginLeft": "12px"}
                                   ),
                         html.Div([
                           ## Michaelis-Menten simulated plot
                               html.Div(dcc.Graph(id="simulatedMM-plot"),style={"width": "48%","display": "inline-block"}),
                               html.Div(dcc.Graph(id="simulatedLB-plot"),style={"width": "48%", "display": "inline-block"})],
                             style={"display": "flex", "justify-content": "space-between"}
                         )
                         ],style={"color": "#D4AF37", "marginTop": "20px"})])

#Dash Callbacks
@app.callback([Output('upload-output', 'children'),
              Output('MM-plot', 'figure'),
                Output('LB-plot', 'figure'),
               Output('vmax-box','value'),
               Output('km-box','value'),
               Output('kcat-output', 'children')],
              [Input('upload-input', 'contents'),
              Input('compute-kcat', 'n_clicks')],
              [State('upload-input', 'filename'),
               State('enzyme-conc', 'value')])
def update_output(contents,n_clicks,filename,enzyme_conc):
    global uploaded
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            uploaded = np.transpose(df.to_numpy())
            uploaded = (uploaded[0],uploaded[1])
            if df.shape[1] >= 2:
                MMfig = mm.MMplot(uploaded)
                LBfig = mm.LBplot(uploaded)
                fittedMMparams = mm.MMfitter(uploaded)
                Vmax = fittedMMparams[1][1]
                Km = fittedMMparams[1][0]
            else:
                fig = go.Figure()
                fig.add_annotation(text="Insufficient Data for Plotting",
                                   xref="paper", yref="paper",
                                   showarrow=False,
                                   font=dict(size=16, color="red"))
            kcat_output = "Enter enzyme concentration to compute kcat."
            if n_clicks > 0 and enzyme_conc is not None and enzyme_conc > 0:
                kcat = Vmax / (enzyme_conc * 1e-6)  # Convert enzyme concentration to M
                kcat_output = f"kcat: {kcat:.2f} s⁻¹"
            return f'Yay! {filename} uploaded successfully!', MMfig, LBfig, f'{Vmax:.2f}', f'{Km:.2f}',kcat_output
        except:
            return 'Error reading file',go.Figure(),go.Figure(),'N/A','N/A','Upload data to compute Kcat'
    return 'Please upload a file', go.Figure(),go.Figure(),'N/A','N/A','Upload data to compute Kcat'

@app.callback(
    [Output("simulatedMM-plot", "figure"),Output("simulatedLB-plot", "figure")],
    Input("button-michaelis-menten", "n_clicks"),
    [State("input-km", "value"), State("input-vmax", "value")]
)
def update_simulated(n_clicks, km, vmax):
    if n_clicks > 0 and km is not None and vmax is not None:
        simulatedfig = mm.MMsimulator(km, vmax)
        return [simulatedfig[0],simulatedfig[1]]
    return [go.Figure(),go.Figure()]


#Run Dash
def MMgui(debug=True, host="127.0.0.1", port=8050):
    app.run_server(debug=debug, host=host, port=port)
    if __name__ == "__main__":
        MMgui()
#MMsuit()

