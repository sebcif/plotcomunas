import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import json
import numpy
import os

def clean_string_series(s):
    return s.str.normalize('NFKD').str.encode('ascii', errors='ignore').\
           str.decode('utf-8').str.lower().replace(r'\(.*?\)', '', regex=True).str.strip()

def main():
    # Carga de mapa de comunas
    filepath = "comunas.json"
    geojson = json.load(open(filepath, 'r'))
    comunas_map_df = gpd.read_file(filepath)
    comunas_map_df['Comuna'] = clean_string_series(comunas_map_df['Comuna'])
    # Carga de archivo de comunas
    filename = 'Comunas.csv'
    comunas_df = pd.read_csv(filename)
    comunas_df['Comuna'] = clean_string_series(comunas_df['Comuna'])
    comunas_count_df = comunas_df.groupby('Comuna', as_index=False).size().rename(columns={'size':'Cantidad'})
    # Combinamos ambos dataset
    full_map = comunas_map_df.merge(comunas_count_df, left_on=['Comuna'], right_on=['Comuna'], how='left')
    full_map['Cantidad'].fillna(0, inplace=True)
    map_fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=full_map.objectid,
        featureidkey="properties.objectid",
        z=full_map.Cantidad,
        colorscale="Viridis",
        text=full_map['Comuna'],
        hovertemplate='<b>%{text}</b><br>Cantidad: %{z}',
        marker_opacity=0.5, marker_line_width=0),
    )
    map_fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": -33.6048, "lon": -70.6287})
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    map_fig.show()
    return

if __name__=='__main__':
    main()