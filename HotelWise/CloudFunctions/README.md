<p align="center">
    <img src="../../_src/logo/HotelWiseLogo.Horizontal.png">
</p>

# Despliegue del Proyecto de Machine Learning <!-- omit in toc -->

## Indice <!-- omit in toc -->

- [Despliegue](#despliegue)
  - [Implementacion en la Nube](#implementacion-en-la-nube)
    - [Proceso](#proceso)
  - [Codigos de Python](#codigos-de-python)
  - [Estructura y Resultados por Contenedores](#estructura-y-resultados-por-contenedores)
    - [Contenedor DB\_FIX para NLP](#contenedor-db_fix-para-nlp)
    - [Contenedor ML\_HTTP para Machine Learning](#contenedor-ml_http-para-machine-learning)
  - [Consideraciones](#consideraciones)
    - [Linea de Comandos](#linea-de-comandos)
    - [Por codigo Python](#por-codigo-python)
- [Contribuciones](#contribuciones)
- [Créditos](#créditos)
- [Licencias](#licencias)
- [Contacto](#contacto)
- [Enlaces adicionales](#enlaces-adicionales)

---

# Despliegue

Como se ha podido ver anteriormente, ya se eligieron los modelos de análisis de sentimiento y sistema de recomendacion. Estos fueron evaluados y desarrollados en los jupyter notebooks vistos en la seccion precedente. 
En esta etapa, se utiliza la información recopilada para generar códigos de procesamiento automatico y escalable, de forma que pueda ser deplegado en Cloud Functions.

## Implementacion en la Nube

Los modelos debieron implementarse en dos contenedores de Cloud Functions distintos, según sus triggers. 
Estos son los 2 activadores:
- Por modificación de archivos (Debido carga o modificacion de la base de datos).
  - Este activará el análisis y procesamiento de la base de datos principal para realizar NLP y luego recopilar datos de Amenidades, Estados y Ciudades, para finalmente almacenar una base de datos con los datos necesarios para realizar las recomendaciones.
- Por envío de mensaje HTTP (Debido a la selección de Estado y Ciudad en la Web).
  - Este activará el sistema de recomendaciones, que tomará como punto de partida la base de datos procesada en el contenedor de NLP, donde el modelo de machine learning enviará una respuesta con la eleccion de los 3 mejores hoteles en la zona, según rating promedio, análisis de sentimiento e índice de seguridad.

Gracias a la facilidad de uso de Cloud Functions, solo fue necesario utilizar los códigos de los notebooks para llevarlos a la nube. Luego se implementaron los cambios necesarios para interactúen con el entorno de GCP, como por ejemplo Cloud Storage, que es donde se alojan las bases de datos proporcionadas por Engineering.

Para mas informacion sobre el indice de seguridad dirigirse a [Crime_In_The_USA](https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise/Crime_In_The_USA).
### Proceso

Dado que el proyecto HotelWiseWeb ya se encontraba funcionando en GCP, solo debió configurarse Cloud Functions para comenzar a trabajar y puedan llevarse a cabo los trabajos de ML.

El proceso de implementción se puede separar en las siguientes partes:

- Depuracion del codigo de los notebooks, es decir que se transcriben y modifican los codigos python escritos anteriormente para que interactúen con Cloud Storage, Cloud Functions y por lo tanto funcionen de forma autonoma y escalable.
- Configuracion del entorno de Cloud Functions:
  - Eleccion de la version del entorno de trabajo (Memoria, CPU, etc.).
  - Eleccion del trigger o activador para iniciar la funcion.
  - Carga de librerías de trabajo (requirements.txt)
- Carga de los codigos.
- Prueba de Ejecucion.
- Despliegue.

## Codigos de Python

Es importante tener en cuenta que los scripts de python se separan en forma similar a los notebooks pero con algunas diferencias, ya que deben seguirse otros metodos de programacion para que dichos codigos sean funcionales. Uno de los elementos mas importantes es la separacion del codigo en funciones y la utilización de modulos de trabajo, separados en distintos archivos.

## Estructura y Resultados por Contenedores

### Contenedor DB_FIX para NLP

1. <u>Entorno GCP (**Cloud Storage** hotelwise_bucket)</u>
   - > Modificación o carga de ```hoteles_unificado.xlsx```-> Cloud Storage genera un **trigger** y llama a la Cloud Function **DB_FIX**.
2. <u>Entorno GCP (**Cloud Function** DB_FIX)</u>
- Carga DB_FILES.py y requirements.txt
- Activacion process_hotel_data() en main.py
  - -> Llama a process_amenities() en DB_FIX_Amenities.py
      - > Procesa los datos y los carga en el archivo HotelesUnificado.parquet en el bucket hotelwise_db.
  - -> Llama a process_crime() en DB_FIX_Crime.py
      - > Combina los datos de Hoteles (HotelesUnificado.parquet) con los de Seguridad (CrimeInTheUSA.parquet), por Estado y Ciudad. Luego los carga en el archivo HotelesUnificado_Final.parquet en el bucket hotelwise_db.
  - -> Llama a process_nlp() en DB_NLP_NLTK.py
      - > Realiza el análsis de sentimiento, reordena la tabla y la almacena en el archivo Hoteles_NLP_NLTK.parquet en el bucket hotelwise_db para que se encuentre disponible para cualquier pedido que realice el sistema de recomendaciones.
  - -> Llama a extract_amenities() en DB_Extract_Amenities.py
      - > Extrae y arma una lista de todas las amenidades de la base de datos y las guarda en el archivo amenities_data.parquet en el bucket hotelwise_db, para que estén disponibles en cualquier momento para los requerimientos de la WEB.
  - -> Llama a extract_location() en DB_Extract_Location.py
      - > Extrae y arma una lista de todos los Estados y sus correspondientes Ciudades, para luego almacenarla en los archivos state_city_data.parquet y state_city_data.csv, en el bucket hotelwise_db. Para finalmente terminar el proceso.

### Contenedor ML_HTTP para Machine Learning

1. <u>Entorno WEB:</u>
   - App Web Front-End ([HotelWise](https://hotelwiseweb.uk.r.appspot.com)) -> REVIEWS -> Eleccion de ```Estado``` y ```Ciudad``` -> La pagina genera un **trigger** de HTTP y llama a la Cloud Function **ML_HTTP**.
2. <u>Entorno GCP (**Cloud Function** ML_HTTP)</u>
- Carga requirements.txt
- Activacion de recomendacion_hotel() en main.py
     - > Carga la base de datos contenida en el archivo Hoteles_NLP_NLTK.parquet desde el bucket hotelwise_db, procesada anteriormente en DB_FIX
     - > Realiza el proceso de seleccion de hoteles basado en Estado y Ciudad (aportados junto con el trigger). Genera la recomendación según los datos de Seguridad, Rating y Sentimientos, para finalmente devolver la recomendación a la App Web.
1. <u>Entorno WEB:</u>
   - >El Back-End de la App Web contenida en GCP App Engine, recibe la recomendación de los 3 mejores hoteles.
   - > El Front-End de la App Web ([HotelWise](https://hotelwiseweb.uk.r.appspot.com)) muestra los resultados en pantalla.

## Consideraciones

Es importante destacar que los sistemas de NLP y ML son autonomos y escalables. Se realizaron pruebas con bases de datos de distintos tamaños y probaron funcionar correctamente, por lo que al momento de ampliar las locaciones de hoteles, podrán continuar trabajando.
Tambien relevante mencionar que los pedidos al sistema de recomendaciones pueden hacerse de 3 formas distintas, una de ellas es a traves de la página web, pero tambien pueden hacerse consultas en la terminal por linea de comandos y tambien utilizando un codigo de python.

### Linea de Comandos

```bash
curl -m 70 -X POST https://us-central1-hotelwiseweb.cloudfunctions.net/ML_HTML \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{
  "state": "Nombre Estado Seleccionado",
  "city": "Nombre Ciudad Seleccionada"
}'
```

### Por codigo Python

En este caso de proporciona un archivo con el código python que realiza el pedido y este es [Prueba_ML_HTTP.py](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/CloudFunctions/Prueba_ML_HTTP.py)

* Procedimiento:
> Ingresar en linea de comandos de la terminal (donde se encuentre descargado `Prueba_ML_HTTP.py`):

```bash
python Prueba_ML_HTTP.py
```
> Salida y requerimiento:
```bash
Ingrese Estado deseado: 
Ingrese Ciudad deseada:
```
> Retorno al Pedido:
```bash
Código de Estado: 200
Cloud Function activado correctamente!
Contenido de la Respuesta:

Hotel Recomendado 1: Nombre Hotel 1
Hotel Recomendado 2: Nombre Hotel 2
Hotel Recomendado 3: Nombre Hotel 3
```

---

# Contribuciones

¡Estamos abiertos a contribuciones! Si tienes ideas de mejora, problemas que reportar o características nuevas que te gustaría añadir, no dudes en abrir una solicitud de extracción o un problema en este repositorio.

# Créditos

- Desarrollado por HotelWise® 2024 Team.

- Logotipo diseñado por HotelWise® 2024 Copyright ©.

# Licencias

Este proyecto está bajo las Licencias:

- [![Licencia GPL 3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPL)
- [![Licencia MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE-GPL)
- [![Licencia Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE-APACHE)


# Contacto

Si tienes alguna pregunta, comentario o problema con la página web de HotelWise, no dudes en ponerte en contacto con nosotros.

- **Delfina Longo Peña**
  - ![mail](../../_src/icons/mail.ico) [delfinapena55@gmail.com](mailto:delfinapena55@gmail.com)
  - ![LinkedIn](../../_src/icons/linkedin.ico) [Delfina Longo Peña](https://www.linkedin.com/in/delfina-longo-pe%C3%B1a-44b4b623b)
  - ![GitHub](../../_src/icons/github_mark_icon.ico) [delfinap5](https://github.com/delfinap5)

- **Angel Prieto**
  - ![mail](../../_src/icons/mail.ico) [angelprieto92@gmail.com](mailto:angelprieto92@gmail.com)
  - ![LinkedIn](../../_src/icons/linkedin.ico) [Angel Prieto](https://www.linkedin.com/in/angelprieto92)
  - ![GitHub](../../_src/icons/github_mark_icon.ico) [PrietoPy](https://github.com/PrietoPy)

- **Carlos Hidalgo**
  - ![mail](../../_src/icons/mail.ico) [hidalgo.carlos1984@gmail.com](mailto:hidalgo.carlos1984@gmail.com)
  - ![LinkedIn](../../_src/icons/linkedin.ico) [Carlos Hidalgo](https://www.linkedin.com/in/carlos-hidalgo84)
  - ![GitHub](../../_src/icons/github_mark_icon.ico) [C-Hidalgo](https://github.com/C-Hidalgo)

- **Miguel Dallanegra**
  - ![mail](../../_src/icons/mail.ico) [mdallanegra@icloud.com](mailto:mdallanegra@icloud.com)
  - ![LinkedIn](../../_src/icons/linkedin.ico) [Miguel Dallanegra](https://www.linkedin.com/in/mdallanegra)
  - ![GitHub](../../_src/icons/github_mark_icon.ico) [mdallanegra](https://github.com/mdallanegra)

# Enlaces adicionales

- [Documentación completa del proyecto](https://github.com/HotelWise/HotelWise)
- [Repositorio de código fuente de la Web](https://github.com/HotelWise/HotelWise/tree/HotelWiseML)
- [Sitio web en vivo](https://hotelwiseweb.uk.r.appspot.com)