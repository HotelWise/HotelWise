<p align="center">
    <img src="../_src/logo/HotelWiseLogo.Horizontal.png">
</p>

# Análisis previo Proyecto de Machine Learning <!-- omit in toc -->

## Indice <!-- omit in toc -->

- [Análisis Preliminar de Modelos](#análisis-preliminar-de-modelos)
- [Etapas de revision de modelos:](#etapas-de-revision-de-modelos)
  - [Etapa Inicial](#etapa-inicial)
  - [Etapa NLP](#etapa-nlp)
    - [Bibliotecas:](#bibliotecas)
      - [NLTK:](#nltk)
      - [Stanza:](#stanza)
      - [TensorFlow:](#tensorflow)
    - [Eleccion del modelo de NLP](#eleccion-del-modelo-de-nlp)
  - [Etapa ML](#etapa-ml)
    - [Modelos:](#modelos)
      - [SciKit mediante Cosine Similarity:](#scikit-mediante-cosine-similarity)
      - [Tensorflow Recommenders](#tensorflow-recommenders)
    - [Eleccion del sistema de recomendaciones ML](#eleccion-del-sistema-de-recomendaciones-ml)
- [Despliegue de los Modelos](#despliegue-de-los-modelos)
- [Contribuciones](#contribuciones)
- [Créditos](#créditos)
- [Licencias](#licencias)
- [Contacto](#contacto)
- [Enlaces adicionales](#enlaces-adicionales)

---

# Análisis Preliminar de Modelos

Aqui se realizan diferentes trabajos sobre las bases de datos distribuidas por Engineering, para poder implementar los modelos de aprendizaje automático propuestos.

# Etapas de revision de modelos:

A continuación se explican los pasos utilizados para desplegar el modelo de Machine Learning, partiendo de reacomodamiento de los dataframes para mayor facilidad en la implementación de análisis de sentimiento y recomendaciones.

## Etapa Inicial

Acomodamiento de columnas y extraccion de amenities para posterior trabajo en el filtrado y recomendación de hoteles.
  - En el notebook [00.DB.FIX.Amenities.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/00.DB.FIX.Amenities.ipynb) se realiza un pequeño trabajo sobre los datos obtenidos del ETL para comenzar a diseñar los dataframes necesarios para Machine Learning.

Implementacion de bases de datos de seguridad para mayor exactitud en la recomendación de hoteles.
  - En el notebook [00.DB.FIX.Crime.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/00.DB.FIX.Crime.ipynb) se realizan los tratamientos preliminares necesarios para comenzar a trabajar con las bases de datos luego implementar el codigo en Cloud Functions.
  - En la sección [Crime_In_The_USA](https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise/Crime_In_The_USA) se habla de la recoleccion de la información de crimenes y el tratamiento del índice de seguridad.
  
## Etapa NLP

Etapa donde se comienza a trabajar con los datos ya listos para implementar el modelo de procesamiento de lenguaje natural, a fin de hacer el análisis de sentimiento. Para ello se implementaron tres modelos en pos de seleccionar el mas económico, eficiente y exacto. Como resultado se obtendrá la clasificación de las reseñas realizadas por los usuarios en dos grupos, a los comentarios Positivos se les asignará un 1 y a los Negativos se les asignará un 0 para que el modelo de ML comprenda efectivamente como procesar el dato.

### Bibliotecas:

#### NLTK:

"Natural Language Toolkit" Es una biblioteca de procesamiento de lenguaje natural que proporciona una serie de herramientas y recursos para trabajar con texto y este debe realizarse en varias etapas.

**Pre-procesamiento del texto**:

  - Tokenización: División de un texto en unidades más pequeñas, como palabras o frases
  - Etiquetado de partes del discurso y reconocimiento de palabras clave mediante diccionarios referidos al tema a tratar. 
  - Asignación de etiquetas gramaticales a cada palabra en un texto, como sustantivo, verbo, adjetivo, etc.

**Procesamiento del texto**:

  - Análisis sintáctico: Análisis de la estructura gramatical de las oraciones.
  - Análisis semántico: Análisis del significado de las palabras y oraciones.
  - Clasificación de textos: Para este caso análisis de sentimientos

En el notebook [01.NLP.01.NLTK.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/01.NLP.01.NLTK.ipynb) se puede ver una forma de implementar las bibliotecas y desplegar el modelo.

#### Stanza:

Es una biblioteca de procesamiento de lenguaje natural (NLP) desarrollada por el grupo de investigación de procesamiento de lenguaje natural de la Universidad de Stanford. Anteriormente conocida como StanfordNLP, esta proporciona una interfaz simple y fácil de usar para realizar tareas de NLP como tokenización, etiquetado de partes del discurso (POS), análisis sintáctico, análisis de dependencias y reconocimiento de entidades nombradas (NER), entre otros.
Para este caso no es necesario realizar las etapas de pre-procesamiento, ya que vienen implementados en la biblioteca, por lo que solo es necesario programarlo y desplegarlo para que pueda hacer el análisis.

En el notebook [01.NLP.02.Stanza.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/01.NLP.02.Stanza.ipynb) se puede ver una forma de implementar las bibliotecas y desplegar el modelo.

#### TensorFlow:

Tensorflow Text es una extensión de TensorFlow que proporciona una serie de operaciones y herramientas específicamente diseñadas para trabajar con texto en modelos de aprendizaje automático. Este ya incluye funcionalidades para preprocesar texto, como tokenización y conversión de texto. Estas herramientas son útiles para tareas de procesamiento de lenguaje natural (NLP) como el análisis de sentimientos y al ser parte de TensorFlow se integra bien con otras herramientas y bibliotecas de aprendizaje automático disponibles en el ecosistema de Google.

En el notebook [01.NLP.03.TensorFlow.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/01.NLP.03.TensorFlow.ipynb) se puede ver una forma de implementar las bibliotecas y desplegar el modelo.

### Eleccion del modelo de NLP

Después de haber realizado pruebas con las bibliotecas y nodelos de procesamiento de lenguaje natural, se ha decidido trabajar con **NLTK**, ya que ha demostrado ser muy exacto, relativamente rápido y muy liviano para trabajar, por lo que implicará un menor costo en su implementación. Aunque consume memoria y tiempo, ocupa menos recursos de CPU que es por lo que se cobra cuando el codigo se encuentra desplegado en Cloud Function. 

## Etapa ML

En esta etapa se trabaja con el análisis de sentimientos realizado en NLP, el indice de seguridad de las localidades donde se encuentran los hoteles y el rating promedio que cada uno de ellos posee.
Aqui se evalúan dos modelos de Machine Learning que son de los mas utilizados, los cuales se presentan a continuación.

### Modelos:

#### SciKit mediante Cosine Similarity:

La similitud de coseno es una medida utilizada para determinar cuán similares son dos vectores en un espacio multidimensional. En el contexto del aprendizaje automático se utiliza comúnmente para comparar la similitud entre elementos representados como vectores de términos.
Es una técnica de filtrado colaborativo que utiliza la similitud de elementos para realizar sugerencias entre ellos. Este enfoque se utiliza comúnmente en sistemas de recomendación de películas, productos, noticias, etc., por lo que para recomendar hoteles será de gran utilidad.
En el notebook [02.ML.01.ConsineSimilarity.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/02.ML.01.ConsineSimilarity.ipynb) se puede ver una forma de implementar las bibliotecas y desplegar el modelo.

#### Tensorflow Recommenders

Es una biblioteca de TensorFlow diseñada específicamente para la construcción de sistemas de recomendación utilizando técnicas de aprendizaje profundo y métodos de aprendizaje colaborativo. Esta biblioteca proporciona una serie de herramientas y utilidades para simplificar y agilizar el proceso de desarrollo de sistemas de recomendación.
A continuacion se pueden ver algunas de sus características mas importantes:
- Modelos de recomendación predefinidos: TFRS ofrece una variedad de modelos de recomendación predefinidos, como modelos de factorización matricial, modelos de redes neuronales, modelos híbridos y más. Estos modelos se pueden adaptar fácilmente para satisfacer las necesidades específicas del proyecto de recomendación.
- Componentes personalizables: Además de los modelos predefinidos, TFRS proporciona componentes flexibles y personalizables que permiten a los desarrolladores construir y experimentar con modelos de recomendación a medida. Esto incluye capas personalizadas, funciones de pérdida personalizadas, y más.
- Datasets y procesamiento de datos: TFRS incluye herramientas para trabajar con conjuntos de datos de recomendación, incluyendo preprocesamiento de datos, manejo de datos estructurados y no estructurados, y funciones para cargar y gestionar datos de manera eficiente.
- Entrenamiento y evaluación de modelos: TFRS proporciona utilidades para entrenar y evaluar modelos de recomendación, incluyendo técnicas de validación cruzada, métricas de evaluación de modelos y herramientas para el seguimiento del progreso del entrenamiento.
- Integración: Como parte del ecosistema de Google, TFRS se integra bien con otras herramientas y bibliotecas de TensorFlow, lo que permite a los desarrolladores aprovechar las funcionalidades adicionales de TensorFlow para construir sistemas de recomendación completos y escalables.

### Eleccion del sistema de recomendaciones ML 

En este caso aunque TensorFlow es sin dudas el mejor, su dificultad para ser implmentado y los altos requerimientos para procesar datos, lo hace el mas costoso y e improductivo por el momento. Además en las pruebas realizadas arrojó un 30% de efectividad, por lo que debería continuarse el entrenamiento y perfeccionamiento del código para su correcto despliegue. Por esto se ha resuelto dejarlo de lado debido a que el corto tiempo disponible y posibles dificultades que puedan encontrarse posteriormente para la correcta implementación de todo el proyecto. 
Por ello se ha recurrido al modelo **SciKit** con **Cosine Similarity** que es efectivo, relativamente simple de implementar y consume pocos recursos, por lo que puede ser utilizado en un entorno de desarrollo simple como Cloud Functions. Si bien no es el mas rápido, su robustez hace que genere recomendaciones sin problemas. Tambien resulta muy versatil ya que puede ser convocado desde varios entornos, lo que lo hace ideal para ser implementado en una Aplicación Web. Otra de sus virtudes es que al consumir pocos recursos de procesamiento, genera poco gasto, siendo alto el resultado costo-beneficio.

# Despliegue de los Modelos

Como se ha podido determinar de todos los análisis previos, los modelos a implementar son lo suficientemente pequeños para ser desplegados mediante Cloud Functions, lo que será ampliado en la sección [CloudFunctions](https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise/CloudFunctions).

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
  - ![mail](../_src/icons/mail.ico) [delfinapena55@gmail.com](mailto:delfinapena55@gmail.com)
  - ![LinkedIn](../_src/icons/linkedin.ico) [Delfina Longo Peña](https://www.linkedin.com/in/delfina-longo-pe%C3%B1a-44b4b623b)
  - ![GitHub](../_src/icons/github_mark_icon.ico) [delfinap5](https://github.com/delfinap5)

- **Angel Prieto**
  - ![mail](../_src/icons/mail.ico) [angelprieto92@gmail.com](mailto:angelprieto92@gmail.com)
  - ![LinkedIn](../_src/icons/linkedin.ico) [Angel Prieto](https://www.linkedin.com/in/angelprieto92)
  - ![GitHub](../_src/icons/github_mark_icon.ico) [PrietoPy](https://github.com/PrietoPy)

- **Carlos Hidalgo**
  - ![mail](../_src/icons/mail.ico) [hidalgo.carlos1984@gmail.com](mailto:hidalgo.carlos1984@gmail.com)
  - ![LinkedIn](../_src/icons/linkedin.ico) [Carlos Hidalgo](https://www.linkedin.com/in/carlos-hidalgo84)
  - ![GitHub](../_src/icons/github_mark_icon.ico) [C-Hidalgo](https://github.com/C-Hidalgo)

- **Miguel Dallanegra**
  - ![mail](../_src/icons/mail.ico) [mdallanegra@icloud.com](mailto:mdallanegra@icloud.com)
  - ![LinkedIn](../_src/icons/linkedin.ico) [Miguel Dallanegra](https://www.linkedin.com/in/mdallanegra)
  - ![GitHub](../_src/icons/github_mark_icon.ico) [mdallanegra](https://github.com/mdallanegra)

# Enlaces adicionales

- [Documentación completa del proyecto](https://github.com/HotelWise/HotelWise)
- [Repositorio de código fuente de la Web](https://github.com/HotelWise/HotelWise/tree/HotelWiseML)
- [Sitio web en vivo](https://hotelwiseweb.uk.r.appspot.com)