<p align="center">
    <img src="../../_src/logo/HotelWiseLogo.Horizontal.png">
</p>

# Recopilacion de Datos de Seguridad <!-- omit in toc -->

## Indice <!-- omit in toc -->

- [Descripción](#descripción)
  - [Datos de Seguridad](#datos-de-seguridad)
- [Tablas conseguidas](#tablas-conseguidas)
  - [Procesamiento](#procesamiento)
- [Contribuciones](#contribuciones)
- [Créditos](#créditos)
- [Licencias](#licencias)
- [Contacto](#contacto)
- [Enlaces adicionales](#enlaces-adicionales)

# Descripción

En esta sección se propone recuperar la información de crimenes en el territorio de los Estados Unidos. 

## Datos de Seguridad

El dato probó ser dificil de conseguir, pero afortunadamente se logró llegar a tablas con datos concretos. Los datos se extrajeron de la base de datos publicada por el FBI.
Las tablas recuperadas corresponden a los años 2018 y 2017, los datos de 2019 se encuentran incompletos, por lo que no se utilizaron y se desconoce la razón por la que no existen datos mas actualizados.
La información involucra al rededor de 8000 ciudades de los Estados Unidos y posee informacion de la poblacion de cada localidad, el tipo de delito cometido y la cantidad de cada uno.

# Tablas conseguidas

 Crimen en los Estados Unidos según recopilación del FBI de delitos conocidos por las autoridades, por estado y por ciudad.

* Estadisticas FBI 2017: https://ucr.fbi.gov/crime-in-the-u.s/2017/crime-in-the-u.s.-2017 
* Tabla: https://ucr.fbi.gov/crime-in-the-u.s/2017/crime-in-the-u.s.-2017/tables/table-8/table-8.xls
* Estadisticas FBI 2018: https://ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018 
* Tabla: https://ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018/tables/table-8/table-8.xls

## Procesamiento

Los datos proporcionados por las bases de datos se trabajaron de la siguiente forma:

- Se extrajeron los datos de ambas tablas.
- Se realizó una sumatoria de todos los delitos por cada localidad.
- Se generó el calclulo de la tasa de criminalidad por cada año y ciudad.
$$Tasa\;;de\;Delincuencia=\frac{Numero\;total\;de\;delitos}{Poblacion\;Total}\times Factor\;de\;Escala$$
>El factor escala utilizado es 1000 debido a que la variacion de la población entre ciudades es muy grande.
- Se limpiaron los datos innecesarios.
- Se unificaron las tablas de ambos años.
- Se realizó la resta de las tasas de criminalidad.
$$Variacion\;Tasa\;de\;Delincuencia=Tasa\;de\;Delincuencia\;Actual−Tasa\;de\;Delincuencia\;Anterior$$
> Realizar la resta entre las tasas de criminalidad implica que se puede analizar el dato simplemente con ver su tamaño y signo, lo que será my útil para la implementación de los KPI.
$$R=\frac{V_{(hoy)}-V_{(ayer)}}{V_{(ayer)}}$$
>  Para que se comprenda correctamente lo que se sugiere, es que los valores positivos resultantes de la resta indican un aumento en la seguridad de la zona (O disminución de la delincuencia) y por el contrario los valores negativos indican una disminucion en la seguridad (O aumento de la delincuencia), y obviamente el tamaño de los valores inidca directamente el indice de crecimiento de cada uno de ellos.
- Se realizaron algunos calculos estadísticos simples para poder identificar outliers y comprender mejor la situación evaluada.
- Se almacenó la base de datos resultante para luego ser utilizada por el sistema de Machine Learning en el [Análisis previo de Proyecto de Machine Learning](https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise) y en el [Despliegue del Proyecto de Machine Learning](https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise).

__Para mayor detalle se sugiere revisar el Jupyter Notebook que se encuentra en esta sección 
con el nombre [CriminalityUSA.ipynb](https://github.com/HotelWise/HotelWise/blob/HotelWiseML/HotelWise/Crime_In_The_USA/CriminalityUSA.ipynb)__

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