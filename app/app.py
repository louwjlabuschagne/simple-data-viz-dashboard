import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path

data_dir = Path('../notebooks/data')

df_philosopher = pd.read_csv(data_dir/'Harry Potter 1.csv', sep=';')
df_philosopher.columns = [c.lower().strip().replace(' ', '_')
                          for c in df_philosopher.columns]
df_philosopher['character'] = df_philosopher['character'].str.strip().str.lower()
df_philosopher['sentence'] = df_philosopher['sentence'].str.lower()

for character in df_philosopher['character'].unique():
    df_philosopher[f'{character}'] = df_philosopher['sentence'].str.count(
        character)

df_mentions = df_philosopher.groupby('character')\
    .sum().reset_index()\
    .melt(id_vars='character', var_name='mentions', value_name='count')

characters = list(df_mentions['character'].unique())

df_mentions['speaker'] = df_mentions['character'].apply(
    lambda ai: characters.index(ai))
df_mentions['mentioner'] = df_mentions['mentions'].apply(
    lambda ai: characters.index(ai)+len(character))

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=characters+characters,
    ),
    link=dict(
        source=df_mentions['speaker'].values,
        target=df_mentions['mentioner'].values,
        value=df_mentions['count'].values
    ))])\
    .update_layout(title_text="Who speaks about who",
                   height=1000)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(html.Div([
    dcc.Graph(figure=fig,
              id='output-figure')
]))

if __name__ == "__main__":
    app.run_server()
