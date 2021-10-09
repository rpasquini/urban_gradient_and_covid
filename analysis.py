__author__ = 'Ricardo Pasquini'
#rpasquini@gmail.com
import contextily as cx
import geopandas as gpd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import econometrics as econ
import pickle
import pandas as pd


ciudades=['lima', 'bogota', 'medellin', 'cali', 'guayaquil', 'quito', 'rosario', 'cordoba', 'amba', 'montevideo']

def regress(lista, df):

  gdf=df[lista]
  gdf=gdf.dropna()
  # lista[0] refiere al primer elemento de la lista, esto es, el nombre de la variable a explicar
  # del dataframe datos tomaremos solo la columna con el nombre de la variable a explicar para la variable Y
  Y=gdf[lista[0]]
  # lista[1:] refiere al resto de los nombres incluidos en la  lista, esto es, a la lista de nombre de la variables que serán explicativas
  X=gdf[lista[1:]]
  X=sm.add_constant(X)
  modelo=sm.OLS(Y,X)
  resultados=modelo.fit()
  # imprimimos en pantalla el resumen de resultados
  print(resultados.summary())
  # la funcion devolverá el objeto de resultados

  return {'resultados':resultados, 'gdf':gdf}


def completeanalysis(ciudad, dependent):

    gdf=gpd.GeoDataFrame.from_file("data/"+ciudad+".zip")

    gdf=gdf.loc[gdf[dependent]<gdf[dependent].quantile(.95)]
    map_prices(gdf,ciudad,dependent)

    gdf['post'] = 0
    gdf.loc[(gdf['start_year'] == 2021)| (gdf['start_year'] == 2020) & (gdf['start_mont']>=4), 'post'] =1
    gdf['postdistancia'] = gdf['post']*gdf['distanciaC']

    output1=regress([dependent,'distanciaC','post',  'postdistancia'],gdf)
    gdf2=output1['gdf']
    ypred=output1['resultados'].predict()
    gdf2['ypred']=ypred

    graph_gradiente(gdf2,ciudad, dependent)

    residuals=gdf2[dependent]-gdf2.ypred
    graph_residuals(residuals,ciudad)

    output2=regress([dependent,'distanciaC','post',  'postdistancia','surface_co', 'surface_to', 'rooms'],gdf)

    # Saving
    resultados1=output1['resultados']
    save_data(resultados1,ciudad,'modelo1')
    resultados2=output2['resultados']
    save_data(resultados2,ciudad,'modelo2')


def graph_gradiente(gdf2,ciudad,dependent):

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(gdf2['distanciaC'], gdf2[dependent], 'o', label="Data", color='gray')
    ax.plot(gdf2.loc[gdf2.post==0]['distanciaC'], gdf2.loc[gdf2.post==0].ypred, 'b-', label="Pre", color='red')
    ax.plot(gdf2.loc[gdf2.post==1]['distanciaC'],gdf2.loc[gdf2.post==1].ypred, 'b-', label="Post", color='green')
    plt.title(ciudad)
    ax.legend(loc="best");

    if ciudad=='amba':
        plt.title('Linear gradient. '+ciudad.upper())
    else:
        plt.title('Linear gradient. '+ciudad.capitalize())

    plt.savefig('graphs/gradient_'+ciudad+'.png')

def graph_residuals(residuals,ciudad):

    fig, ax = plt.subplots(figsize=(6, 6))
    residuals.hist()
    if ciudad=='amba':
        plt.title('Residuals. '+ciudad.upper())
    else:
        plt.title('Residuals. '+ciudad.capitalize())
    plt.savefig('graphs/residuals_'+ciudad+'.png')

def map_prices(gdf,ciudad,dependent):
    fig, ax = plt.subplots(figsize=(12, 12))
    gdf.to_crs("EPSG:4326").plot(ax=ax,column=dependent, legend=True)
    #ax.set_xlim(-59.2, -58)
    #ax.set_ylim(-35, -34.1)
    cx.add_basemap(ax, crs=gdf.to_crs(epsg=4326).crs.to_string(), source=cx.providers.Stamen.TonerLite)
    ax.axis('off')
    plt.title(ciudad)

    if ciudad=='amba':
        plt.title('Rental prices. '+ciudad.upper())
    else:
        plt.title('Rental prices. '+ciudad.capitalize())
    plt.savefig('graphs/map_'+ciudad+'.png')



def save_data(data,ciudad,name):
    with open('results/'+ciudad+"/"+name+".dat", "wb") as f:
        pickle.dump(data, f)


def load_data(ciudad,name):
    with open('results/'+ciudad+"/"+name+".dat",'rb') as f:
        x = pickle.load(f)
        return x


def print_table(resultsreadylist):
    """
    Prints a table of econometric results using the to_summary_table function
    input: list of regression results object

    :return:
    """""
    descriptions={'dependent':'Adjusted rent', }
    #Defines the variables to be included in the table. Each should exist in the regression results object
    varnames_to_print=['const', 'post', 'distanciaC', 'postdistancia']

    #Set printable names of variables
    labels_dict={ 'post':'Post-covid','distanciaC':'Distance to CBD', 'postdistancia': 'Post*Distance', 'const':'Intercept'}

    # Adds special rows to the table. Warning: length should exactly match the columns in the table.
    # Each row is defined as dict
    specialrows=[{'varname':'Controls', 'values':['No','Yes','No','Yes','No','Yes']}]

    #            {'varname':'Data window', 'values':['Complete','2 days','1 day','Complete','2 days','1 day']}]

    # run the to_summary_table function
    tabledata2=econ.to_summary_table(varnames_to_print, resultsreadylist,labels_dict, specialrows)
    tabledata2=tabledata2.rename(columns={0:'Dependent: '+descriptions['dependent'], 1:'(1)', 2:'(2)', 3:'(3)', 4:'(4)',5:'(5)', 6:'(6)'})
    return tabledata2

def buildtables():
    """
    Compiles the results into 3 tables, and saves them in the tables folder
    Uses the printtable function

    :return:
    """""
    ciudades=['amba','cordoba','rosario', 'bogota','cali', 'medellin', 'quito', 'lima','montevideo']
    tablenumber=1
    tablesasdfs=[]
    for listacorta in [ciudades[0:3], ciudades[3:6], ciudades[6:9]]:
        listaresultados=[]
        headerscolumnasciudades=['Ciudad']
        for ciudad in listacorta:

            listaresultados.append(load_data(ciudad,'modelo1'))
            listaresultados.append(load_data(ciudad,'modelo2'))

            if ciudad=='amba':
                headerscolumnasciudades.append(ciudad.upper())
                headerscolumnasciudades.append(ciudad.upper())
            else:
                headerscolumnasciudades.append(ciudad.capitalize())
                headerscolumnasciudades.append(ciudad.capitalize())


        printabletable=print_table(listaresultados)
        #agrego header ciudades
        header=pd.DataFrame(headerscolumnasciudades,printabletable.columns).T
        tabletoprint=header.append(printabletable).reset_index(drop=True)
        tabletoprint.to_csv("tables/regressions"+str(tablenumber)+".csv", index=False)
        tablesasdfs.append(tabletoprint)
        tablenumber=tablenumber+1