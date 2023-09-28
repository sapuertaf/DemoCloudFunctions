# Demo DataProc Spark Cloud Functions
💡 Notas

- C4 Model para diagramas
- Máximo 2 niveles de anidación para numeración de títulos (i.e. 2.1.)
- 1 video por documentación. Si existen vários videos, unirlos en uno solo.
</aside>

# 1. Objetivo

Desplegar una arquitectura basada en eventos haciendo uso de los servicios: Cloud Functions, DataProc y Cloud Storage; el sistema deberá de funcionar de la siguiente forma:

1. Una vez un nuevo archivo sea escrito correctamente al bucket: raw-data-spark la Cloud Function spark-function deberá de ejecutar la plantilla de Dataproc: spark.
2. La plantilla de Dataproc deberá de leer los datos ingresados al bucket, procesarlos y almacenarlos en el bucket: output-spark en formato Delta Lake.
3. Un “checkpoint” de Spark deberá de ser incluido con el fin de no reprocesar datos anteriormente procesados. 
4. Tanto el código usado por la plantilla de Dataproc, como el código usado por la Cloud Function deberán de ser almacenados en un Bucket de Cloud Storage. 

# 2. Recursos usados

| Recurso | Tipo | Version | Descripción |
| --- | --- | --- | --- |
| Cloud Function |  |  | Usado para ejecutar cierto codigo dado, una vez se crea un nuevo archivo en el raw-data-bucket. |
| Dataproc |  |  | Usado para procesar los datos presentes en el Bucket raw-data-spark y actualizar la tabla Delta presente en el Bucker output-spark. |
| Cloud Storage |  |  | Usado para almacenar en distintos Buckets el código, tanto de la función como de dataproc, los archivos a ser procesados por dataproc y la tabla Delta.  |

# 3. Ambiente de desarrollo

En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto.

## Estructura del código

A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.

```
DemoCloudFunctions-Dataproc&Spark
├── data
│   └── clients3.csv
├── dataproc
│   └── main.py
├── deploy
│   ├── makefile
│   └── spark.yaml
├── docs
├── function
│   ├── main.py
│   └── requirements.txt
└── generator
    └── client_gener.py
```

# 4. Arquitectura de la solución

El siguiente diagrama detalla la arquitectura de la solución implementada:

![Diagrama de despliegue: Infraestructura de GCP usada.](https://dev.azure.com/quind/0d6ed6ae-137f-4fce-9c85-e34317a683a5/_apis/git/repositories/b0b783d7-94ec-4456-ac27-1d826d004e7c/items?path=/docs/arquiFuncionSpark.png&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=main&resolveLfs=true&%24format=octetStream&api-version=5.0)

Diagrama de despliegue: Infraestructura de GCP usada.

# 5. Implementación

## IAM y permisos requeridos

La siguiente tabla muestra los roles y permisos requeridos por Cloud Functions para funcionar correctamente.

| Nombre Rol | Descripción |
| --- | --- |
| roles/iam.serviceAccountTokenCreator | Permite la creación tokens de acceso para cuentas de servicio, lo que permite el acceso a recursos específicos de manera segura. |
| roles/eventarc.eventReceiver | Permisos para actuar como receptor de eventos en aplicaciones basadas en Cloud Run. Las cuentas de servicio o usuarios que tengan este rol pueden suscribirse a eventos y ejecutar servicios de Cloud Run que se activan cuando ocurren esos eventos. |
| roles/pubsub.publisher | Sirve para conceder permisos a usuarios o servicios que necesitan la capacidad de publicar mensajes en temas de Pub/Sub; ayuda a controlar y gestionar el flujo de información del proyecto. |

## Requisitos previos

Para una correcta ejecucion, el proyecto requiere de:

1. Instalar la CLI de Google Cloud [🌐 **Instala la CLI de gcloud**](https://cloud.google.com/sdk/docs/install?hl=es-419) 
2. Crear la cuenta de servicio respectiva con roles y permisos; por defecto Cloud Functions usara la cuenta de servicio de Compute Engine. 
3. Instalar el comando “make” para la distribución o Sistema Operativo correspondiente.

## Guía de uso

La siguiente guía brindará los pasos a seguir para un correcto funcionamiento y ejecución.

1. Inicializar la CLI de gcloud
    
    ```bash
    gcloud init
    ```
    
2. Clonar el código requerido
    
    ```bash
    git clone https://dev.azure.com/quind/big-data/_git/DemoCloudFunctions-Dataproc-Spark
    ```
    
3. Dirigirnos a la carpeta “deploy” del repositorio clonado anteriormente
    
    ```bash
    cd DemoCloudFunctions-Dataproc-Spark/deploy
    ```
    
4. Ejecutar el archivo “makefile”
    
    ```bash
    make
    ```