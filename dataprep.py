__author__ = 'Ricardo Pasquini'
#rpasquini@gmail.com
# Codigo para descarga y preparacion de datos abiertos de Properati
# https://www.properati.com.ar/data/

import os, inspect
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
from shapely.geometry import Point

bboxes={'lima':[-77.218231,-12.255511,-76.781525,-11.847983],
'bogota':[-74.288315,4.506675,-73.970398,4.817979],
'medellin':[-75.657074,6.163262,-75.523865,6.347843],
'cali':[-76.577866,3.360677,-76.455643,3.519305],
'guayaquil':[-79.995712,-2.287224,-79.841904,-2.051253],
'quito': [-78.633957,-0.348386,-78.414230,-0.067628],
'rosario':[-60.790581,-33.029626,-60.579094,-32.861703],
'cordoba':[-64.296455,-31.480901,-64.069862,-31.332379],
'amba':[-59,-35.07811648211815,-58.1,-34.25],
'montevideo':[-56.285843,-34.927305,-55.949387,-34.788737],
}

CBDS={'lima':[-12.0456438313481, -77.03049783580703], #plaza de armas lima
      'bogota':[4.598387954239012, -74.07604350327951], #plaza de bolivar de bogota
      'medellin':[6.252698355831157, -75.56864150327084], #plaza botero
      'cali':[3.459149664698113, -76.52891084561297], # torre de cali
'guayaquil':[-2.194352258082037, -79.88386895910979], #Catedral Católica Metropolitana de Guayaquil
  'quito': [ -0.21493662992634846, -78.50715141123723 ],#Basílica del Voto Nacional
     'rosario':[ -32.94753311498522, -60.63020831072553], # Monumento Histórico Nacional a la Bandera
      'cordoba':[-31.416694441845316, -64.18360210282326],#plaza san martín cordoba
            'amba':[-34.603359,  -58.381613],#obelisco
     'montevideo':[ -34.90674092718181, -56.19977624504621],
   }



def queryproperaty(credentials, ciudad):
    """
    Querys Properati for a city and returns geodataframe
    :param credentials: Big query credentials
    :param ciudad: City name
    :return: gdf
    """""
    project_id = 'dataproperati2019'
    client = bigquery.Client(credentials= credentials,project=project_id)

    lonmin=str(bboxes[ciudad][0])
    lonmax=str(bboxes[ciudad][2])
    latmin=str(bboxes[ciudad][1])
    latmax=str(bboxes[ciudad][3])


    # Aqui se define el pedido en formato SQL.
    QUERY = (
    'SELECT * FROM `properati-dw.public.ads` WHERE start_date >= "2019-05-01" AND start_date <= "2022-05-15" AND type = "Propiedad" '
    #'AND place.l1 = "Argentina" '
    'AND property.type = "Departamento" '
    'AND property.operation = "Alquiler" '
    'AND property.surface_total > 0 '
    'AND property.surface_covered > 0 '
    'AND property.price > 0 '
    #'AND (place.l2="Capital Federal" or place.l2="Buenos Aires Interior" or place.l2="Bs.As. G.B.A. Zona Sur" or place.l2="Bs.As. G.B.A. Zona Norte" or place.l2="Bs.As. G.B.A. Zona Oeste") '
    'AND place.lat <'+latmax+' '
    'AND place.lat >'+latmin+' '
    'AND place.lon < '+lonmax+' '
    'AND place.lon > '+lonmin

    )

    #query_job = client.query(QUERY)  # API request
    #rows = query_job.result()  # Waits for query to finish

    df=client.query(QUERY).to_dataframe()



    df=pd.concat([df[['type', 'type_i18n', 'country', 'id', 'start_date', 'end_date',
       'created_on', 'place', 'development']], json_normalize(df.property), json_normalize(df.place)], axis=1)


    crs = {'init' :'epsg:4326'}
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)


    return gdf



def add_distances_to_CBD(gdf, ciudad):
    """
    Add distances to city CBD
    """

    # define specific projection
    crs_city={'proj': 'tmerc',
     'lat_0': CBDS[ciudad][0],
     'lon_0': CBDS[ciudad][1],
     'k': 0.999998,
     'x_0': 100000,
     'y_0': 100000,
     'ellps': 'intl',
     'units': 'm',
     'no_defs': True}

    gdf=gdf.to_crs(crs_city)

    cbdpoint=Point(CBDS[ciudad][1], CBDS[ciudad][0])
    cbdpointgdf = gpd.GeoDataFrame({'col1': ['name1'], 'geometry': [cbdpoint]}, crs={'init' :'epsg:4326'})
    cbdpointgdf=cbdpointgdf.to_crs(crs_city)

    def distancia(row):
        return cbdpointgdf.geometry[0].distance(row['geometry'])

    gdf['distanciaCBD']=gdf.apply(distancia,axis=1)

    return gdf


def export_to_shapefile(gdf2, ciudad):
    """
    Drop some data. Exports to shapefile
    """

    if 'start_month' not in gdf2.columns:
            gdf2['start_month']=gdf2.start_date.apply(lambda x: x.month)
            gdf2['start_year']=gdf2.start_date.apply(lambda x: x.year)
            gdf2['start_day']=gdf2.start_date.apply(lambda x: x.day)
            gdf2['end_month']=gdf2.end_date.apply(lambda x: x.month)
            gdf2['end_year']=gdf2.end_date.apply(lambda x: x.year)
            gdf2['end_day']=gdf2.end_date.apply(lambda x: x.day)

    gdf2=gdf2.drop(columns=['start_date','end_date','created_on','description','place'])
    gdf2=gdf2.drop(columns=['id'])

    gdf2.to_file("data//2022//"+ciudad+".shp")


def inflationadjustment(gdf2):
    """
    Adds inflation adjusted price

    Cuidado hay que pasarle solo un dataframe con un solo tipo de moneda
    """
    if 'start_month' not in gdf2.columns:
            gdf2['start_month']=gdf2.start_date.apply(lambda x: x.month)
            gdf2['start_year']=gdf2.start_date.apply(lambda x: x.year)

    averageprice=gdf2.groupby(['start_year','start_month',]).median().price.reset_index()
    precio0=averageprice.loc[(averageprice.start_year==2019) & (averageprice.start_month==5)].price[0]
    averageprice['infla']=averageprice.price/precio0
    averageprice=averageprice.drop(columns='price')
    gdf2=gdf2.merge(averageprice, on=['start_year','start_month'])
    gdf2['adjprice']=gdf2.price/gdf2.infla

    return gdf2