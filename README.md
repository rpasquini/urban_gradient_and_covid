# Gradiente urbano en valores de alquiler y Covid 
En este proyecto exploramos cambios en el gradiente urbano de precios atribuíbles a la pandemia del COVID-19 en un conjunto de ciudades de América Latina.

Las ciudades y los aglomerados urbanos en general, se caracterizan por mostrar un gradiente de precios, esto es, un incremento en los valores de las propiedades (precios del suelo, alquileres, etc.) a medida que las mismas se encuentran más cerca del centro de negocios de la ciudad. 

La pandemia del COVID-19 estimuló una serie de cambios en los patrones de localización y en las actividades económicas, que habrían resultado en un decrecimiento del valor de las areas centrales  y un incremento en las áreas más alejadas.

Examinamos una muestra de ciudades seleccionadas de América Latina, incluyendo: el Área Metropolitana de Buenos Aires (AMBA), Córdoba (Argentina),  Rosario (Argentina), Bogotá (Colombia), Medellín (Colombia), Cali (Colombia), Quito (Ecuador), Lima (Peru), y Montevideo (Uruguay).



## Métodos 

En una primera etapa analizamos el gradiente urbano de alquileres . Para cada ciudad recolectamos las ofertas de alquiler disponibles en el sitio Properati (https://www.properati.com.ar/data/). 

Una modelización simplificada que proponemos inicialmente para identificar el gradiente urbano consiste en identificar el principal Centro de Negocios de las respectivas ciudades y medir la distancia de las propiedades a dichos centros. Luego definimos el gradiente como la mejor relación lineal entre las distancias y los valores de alquiler. 

Para identificar el efecto de la pandemia, utilizamos una especificación de Diferencias en Diferencias, donde examinamos cómo el gradiente se transformó en el período posterior a marzo de 2020.

Más específicamente, para cada ciudad, estimamos el siguiente modelo:

![equation](https://latex.codecogs.com/png.latex?alquiler_i%3D%5Cbeta_0&plus;%5Cbeta_1distanciaC_i&plus;%5Cbeta_2Post&plus;%5Cbeta_3%28distanciaC_i%20*%20Post_t%29&plus;%5Cepsilon_i)


donde <img src="https://latex.codecogs.com/gif.latex?alquiler_i " /> es el valor de alquiler de la iesima oferta en la ciudad respectiva, <img src="https://latex.codecogs.com/gif.latex?distanciaC_i " /> es la distancia al centro de negocios en metros, y  <img src="https://latex.codecogs.com/gif.latex?Post_t " /> es una variable dummy que identifica si la oferta fue realizada posterior a marzo 2020 y 0 de otro modo.  En este modelo, el coeficiente <img src="https://latex.codecogs.com/gif.latex?\beta_1 " /> capturará la pendiente del gradiente lineal (i.e., el descuento por metro de distancia al centro de negocios),  <img src="https://latex.codecogs.com/gif.latex?\beta_2 " /> en la ecuacion identifica el cambio en el valor promedio ocurrido en el período de la pandemia. Por último, el coeficiente <img src="https://latex.codecogs.com/gif.latex?\beta_3 " /> busca identificar el efecto de interés, esto es, el cambio del gradiente ocurrido en el período de la pandemia.

## Resultados Preliminares

### Resultados modelo

Las siguientes tablas resumen los resultados del modelo estimado. Para cada ciudad se presentan dos especificaciones. Una incluyendo el modelo básico, y una segunda especificación incluyendo controles adicionales. 

**Tabla I. Resultados econométricos. Ciudades de Argentina**

| Dependent: Adjusted rent | (1)            | (2)            | (3)            | (4)            | (5)            | (6)            |
| ------------------------ | -------------- | -------------- | -------------- | -------------- | -------------- | -------------- |
| Ciudad                   | AMBA           | AMBA           | Cordoba        | Cordoba        | Rosario        | Rosario        |
| Intercept                | 18155.39755*** | 8479.812307*** | 9813.725129*** | 7701.686325*** | 9281.725578*** | 6346.840421*** |
|                          | (59.104649)    | (78.899392)    | (104.236414)   | (131.001237)   | (79.605141)    | (97.099084)    |
| Post-covid               | -502.077196*** | 54.482161      | -348.291042**  | -300.762948**  | -15.706429     | -51.196576     |
|                          | (86.139792)    | (75.095024)    | (152.115917)   | (147.640683)   | (114.633572)   | (106.984893)   |
| Distance to CBD          | -0.098418***   | -0.104176***   | -0.215937***   | -0.279124***   | -0.071673***   | -0.132031***   |
|                          | (0.003427)     | (0.003016)     | (0.037966)     | (0.037431)     | (0.024335)     | (0.023024)     |
| Post*Distance            | 0.004969       | 0.002647       | 0.145899**     | 0.182903***    | -0.108946***   | -0.066393**    |
|                          | (0.005399)     | (0.004722)     | (0.059449)     | (0.05895)      | (0.036308)     | (0.033546)     |
| Controls                 | No             | Yes            | No             | Yes            | No             | Yes            |
| Number of obs.           | 71026.0        | 66655.0        | 3897.0         | 3442.0         | 8256.0         | 7026.0         |
| Adj-R2                   | 0.019          | 0.301          | 0.008          | 0.165          | 0.009          | 0.28           |
| F-statistic:             | 448.122        | 4781.979       | 11.574         | 114.056        | 24.856         | 456.246        |
| Prob (F-statistic)       | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            |

**Tabla II.  Resultados econométricos. Ciudades de Colombia**

| Dependent: Adjusted rent | (1)               | (2)               | (3)               | (4)              | (5)               | (6)              |
| ------------------------ | ----------------- | ----------------- | ----------------- | ---------------- | ----------------- | ---------------- |
| Ciudad                   | Bogota            | Bogota            | Cali              | Cali             | Medellin          | Medellin         |
| Intercept                | 4176386.454067*** | 1673884.041312*** | 1133363.102718*** | 657175.356651*** | 1603611.575982*** | 952158.219363*** |
|                          | (86698.163782)    | (71291.132053)    | (20761.957757)    | (25480.865642)   | (24778.159684)    | (32455.906133)   |
| Post-covid               | -136906.392554    | 93833.356647      | 84586.546489***   | 55723.954168*    | 72686.004275      | 20203.344722     |
|                          | (139138.793706)   | (97367.929152)    | (30816.886466)    | (28857.316721)   | (50914.653734)    | (46423.308543)   |
| Distance to CBD          | -108.551616***    | -87.062835***     | 3.445754          | -4.333077        | 5.750947          | -3.876808        |
|                          | (7.573059)        | (5.437556)        | (3.225149)        | (3.034017)       | (3.856938)        | (3.565829)       |
| Post*Distance            | 9.317349          | 2.68469           | -9.285003*        | -5.098681        | -12.963138*       | -9.778944        |
|                          | (12.468645)       | (8.717723)        | (4.856286)        | (4.540421)       | (7.407363)        | (6.748964)       |
| Controls                 | No                | Yes               | No                | Yes              | No                | Yes              |
| Number of obs.           | 8326.0            | 8253.0            | 6249.0            | 6184.0           | 5796.0            | 5683.0           |
| Adj-R2                   | 0.035             | 0.532             | 0.001             | 0.136            | 0.0               | 0.18             |
| F-statistic:             | 101.945           | 1564.445          | 2.925             | 163.254          | 1.202             | 209.27           |
| Prob (F-statistic)       | 0.0               | 0.0               | 0.033             | 0.0              | 0.308             | 0.0              |

**Tabla III.  Resultados econométricos. Ciudades de Ecuador y Uruguay**

| Dependent: Adjusted rent | (1)            | (2)           | (3)            | (4)            | (5)             | (6)             |
| ------------------------ | -------------- | ------------- | -------------- | -------------- | --------------- | --------------- |
| Ciudad                   | Quito          | Quito         | Lima           | Lima           | Montevideo      | Montevideo      |
| Intercept                | 811.983411***  | 567.663776*** | 2410.620143*** | 1702.582907*** | 20784.537828*** | 14741.382624*** |
|                          | (81.883949)    | (80.184945)   | (31.365546)    | (52.167731)    | (240.570951)    | (314.036575)    |
| Post-covid               | -246.731111*** | -200.958746** | -150.042679*** | -264.29267**   | -463.532126     | -638.653579**   |
|                          | (92.881515)    | (82.906055)   | (46.222472)    | (133.763594)   | (320.565185)    | (317.717696)    |
| Distance to CBD          | -0.034493**    | -0.02634**    | -0.051846***   | -0.053872***   | -0.035444       | -0.147189***    |
|                          | (0.01436)      | (0.012855)    | (0.003292)     | (0.0035)       | (0.049055)      | (0.04876)       |
| Post*Distance            | 0.02614        | 0.014314      | 0.013088***    | 0.0162         | 0.129139**      | 0.196208***     |
|                          | (0.015797)     | (0.014046)    | (0.005075)     | (0.014851)     | (0.065163)      | (0.062118)      |
| Controls                 | No             | Yes           | No             | Yes            | No              | Yes             |
| Number of obs.           | 155.0          | 155.0         | 3726.0         | 1672.0         | 3455.0          | 2411.0          |
| Adj-R2                   | 0.082          | 0.299         | 0.085          | 0.239          | 0.001           | 0.299           |
| F-statistic:             | 5.57           | 11.928        | 116.352        | 88.504         | 1.825           | 172.413         |
| Prob (F-statistic)       | 0.001          | 0.0           | 0.0            | 0.0            | 0.14            | 0.0             |

### Gráficos gradiente

Los siguientes gráficos presentan los gradientes estimados por la específicación del modelo propuesta para cada una de las ciudades.
![AMBA](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_amba.png?raw=true)
![Cordoba](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_cordoba.png?raw=true)
![Rosario](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_rosario.png?raw=true)
![Bogota](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_bogota.png?raw=true)
![Medellin](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_medellin.png?raw=true)
![Cali](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_cali.png?raw=true)
![Quito](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_quito.png?raw=true)
![Lima](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_lima.png?raw=true)
![Montevideo](https://github.com/rpasquini/urban_gradient_and_covid/blob/main/graphs/gradient_montevideo.png?raw=true)



