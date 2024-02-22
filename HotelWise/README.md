<p align="center">
    <img src="../_src/logo/HotelWiseLogo.png">
</p>

# Despliegue de la Aplicacion Web del Proyecto <!-- omit in toc --> 

## Indice <!-- omit in toc --> 

- [Descripción](#descripción)
- [Despliegue de una Aplicación Django en Google App Engine usando Docker](#despliegue-de-una-aplicación-django-en-google-app-engine-usando-docker)
- [Pasos para el armar el servidor docker](#pasos-para-el-armar-el-servidor-docker)
  - [1. Clonar el repositorio](#1-clonar-el-repositorio)
  - [2. Configurar la aplicación Django](#2-configurar-la-aplicación-django)
  - [3. Configurar Dockerfile](#3-configurar-dockerfile)
  - [4. Correr en servidor local la imagen de Docker](#4-correr-en-servidor-local-la-imagen-de-docker)
  - [5. Configuracion Google Cloud Platform](#5-configuracion-google-cloud-platform)
  - [6. Desplegar la aplicación en Google App Engine](#6-desplegar-la-aplicación-en-google-app-engine)
    - [Ajustar los Dockerfiles según las necesidades de la aplicacion](#ajustar-los-dockerfiles-según-las-necesidades-de-la-aplicacion)
    - [Comandos para desplegar en GCP](#comandos-para-desplegar-en-gcp)
- [Contribuciones](#contribuciones)
- [Créditos](#créditos)
- [Licencia](#licencia)
- [Contacto](#contacto)
- [Enlaces adicionales](#enlaces-adicionales)


## Descripción

Partiendo de la App creada en forma local en la rama [HotelWiseWeb](https://github.com/HotelWise/HotelWise/tree/HotelWiseWeb/) creada en Django, se procede a llevarla a produccion. Para ello se creará un contenedor con los archivos de la aplicación, utilizando Docker y luego se desplegará en GCP utilizando el servicio App Engine que lo publicará en la web.

## Despliegue de una Aplicación Django en Google App Engine usando Docker

Este repositorio contiene los archivos necesarios para desplegar una aplicación Django en Google App Engine utilizando Docker.

## Pasos para el armar el servidor docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/HotelWise/HotelWise/tree/HotelWiseWeb/HotelWise.git
cd HotelWise/HotelWiseWeb/HotelWise/
```

### 2. Configurar la aplicación Django

Realizar las configuraciones y revisiones necesarias en `settings.py` y `requirements.txt` para que corra correctamente en contenedor.

### 3. Configurar Dockerfile

Ajustar los Dockerfiles según las necesidades de la aplicacion

  1. `Dockerfile`
  2. `docker-compose.yml`

### 4. Correr en servidor local la imagen de Docker

```bash
docker-compose up
```
Posibles IP locales para ver en navegador:
  * `http://localhost:8000`
  * `http://127.0.0.1:8000`

`Oprima ctl+c para apagar el servidor.`

### 5. Configuracion Google Cloud Platform

Pasos a seguir para subir la página

  1. Crear Proyecto Nuevo 
  2. Ir a App Engine
  3. Crear Aplicacion
  4. Elegir servidor de trabajo (Idealmente cerca de la ubicación de servicio.)
  5. Lenguaje de trabajo (Python y Standard)


### 6. Desplegar la aplicación en Google App Engine

#### Ajustar los Dockerfiles según las necesidades de la aplicacion 

  1. `.gcloudignore`
  2. `docker-compose-deploy.yml`
  3. `app.yaml`

#### Comandos para desplegar en GCP

Ejecutar en Terminal (local) y en la carpeta del proyecto:

  1. Correr: `docker-compose -f docker-compose-deploy.yml run --rm gcloud sh -c "gcloud auth login"` y seguir los pasos que van apareciendo.
  2. Correr `docker-compose run --rm app sh -c "python manage.py collectstatic"` para recolectar los datos estáticos del proyecto (Imagenes, texto, etc.)
  3. Correr `docker-compose -f docker-compose-deploy.yml run --rm gcloud sh -c "gcloud app deploy --project PROJECT_ID"` para subir el projecto a GCP. Notar que `PROJECT_ID` es el nombre que tiene el proyecto creado en la consola de Google Cloud Platform.
  4. Una vez terminado el proceso de subida le dará un IP publico donde ver la aplicacion o página web.

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
- [Repositorio de código fuente de la Web](https://github.com/HotelWise/HotelWise/tree/HotelWiseWeb/HotelWise)
- [Sitio web en vivo](https://hotelwiseweb.uk.r.appspot.com)


