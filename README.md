# Urban gradient in rental values and Covid
In this project we explore changes to the urban prices gradient due to the effects of COVID-19 pandemic, across a number of selected cities in LATAM. 

Cities exhibit urban gradients, defined as increases in land prices as 

Data: https://www.properati.com.ar/data/





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
$$
alquiler_i=\beta_0+\beta_1distanciaC_i+\beta_2Post+\beta_3(distanciaC_i * Post_t)+\epsilon_i
$$
donde $alquiler_i$ es el valor de alquiler de la iesima oferta en la ciudad respectiva, $distanciaC_i$ es la distancia al centro de negocios en metros, y  $Post_t$ es una variable dummy que identifica si la oferta fue realizada posterior a marzo 2020 y 0 de otro modo.  En este modelo, el coeficiente $\beta_1$ capturará la pendiente del gradiente lineal (i.e., el descuento por metro de distancia al centro de negocios),  $\beta_2$ en la ecuacion identifica el cambio en el valor promedio ocurrido en el período de la pandemia. Por último, el coeficiente  $\beta_3$ busca identificar el efecto de interés, esto es, el cambio del gradiente ocurrido en el período de la pandemia.

## Resultados Preliminares
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