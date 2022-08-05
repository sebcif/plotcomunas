import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy
import datetime
import os

def clean_string_series(s):
    return s.str.normalize('NFKD').str.encode('ascii', errors='ignore').\
           str.decode('utf-8').str.lower().replace(r'\(.*?\)', '', regex=True).str.strip()

def main():
    # Carga de mapa de comunas
    filepath = "Comunas/comunas.shx"
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
    regiones = full_map['Region'].unique()
    plot_path = 'plot'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    today = datetime.date.today()
    today_path = os.path.join(plot_path, str(today))
    if not os.path.exists(today_path):
        os.makedirs(today_path)
    for region in regiones:
        print(f"Plotting {region}")
        region_map = full_map[full_map['Region']==region]
        fig_region, ax_region = plt.subplots()
        region_map.plot(column='Cantidad', cmap='Blues', linewidth=1, ax=ax_region, edgecolor='0.9', legend = True)
        ax_region.axis('off')
        fig_region.savefig(os.path.join(today_path, f"{region}_{today}.png"))
    plt.close('all')
    fig_map, ax_map = plt.subplots()
    full_map.plot(column='Cantidad', cmap='Blues', linewidth=1, ax=ax_map, edgecolor='0.9', legend = True)
    ax_map.axis('off')
    fig_map.savefig(os.path.join(today_path, f"fullmapa_{datetime.date.today()}.png"))
    plt.show(block=True)

if __name__=='__main__':
    main()