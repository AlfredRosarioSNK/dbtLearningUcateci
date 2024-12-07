# Proyecto de Pipeline de Ingeniería de Datos

## Miembros del Equipo
- Luis Caba 2021-0799
- Alfred Rosario 2021-0798
- Brayan Peñalo 2020-0962

## Descripción del Proyecto
Este es un proyecto de Ingeniería de Datos que utiliza Apache Airflow, dbt, Snowflake y Astronomer para crear un pipeline de datos. El proyecto está construido usando Astro CLI y Docker para agilizar el despliegue.

## Arquitectura del Proyecto
- **Tecnologías Utilizadas**: 
  - Apache Airflow
  - dbt (para la transformación de datos)
  - Snowflake
  - Astro CLI
  - Docker

## Estructura del Proyecto
- `dags/`: Contiene las definiciones de DAGs de Apache Airflow
- `include/`: Archivos y recursos del proyecto
- `Dockerfile`: Contenedor Docker
- `packages.txt`: Dependencias
- `requirements.txt`: Dependencias de paquetes de Python
- `airflow_settings.yaml`: Configuración local de Airflow

## Configuración de Desarrollo Local

### Requisitos Previos
- Docker
- Astro CLI
- Cuenta de Snowflake (importante)

### Pasos para Ejecutar Localmente
1. Clonar el repositorio
2. Ejecutar `astro dev start` para levantar el entorno local de Airflow (Es necesario tener docker abierto)
3. Acceder a la UI de Airflow en http://localhost:8080/
   - Nombre de usuario: admin
   - Contraseña: admin

### Contenedores Docker
El proyecto utiliza 4 contenedores Docker:
- Postgres (Base de datos de Metadatos)
- Servidor Web de Airflow
- Planificador de Airflow
- Disparador de Airflow

## Despliegue
El despliegue se puede realizar a través de la plataforma Astronomer o configuraciones locales de Docker.

## Inspiración del Quick Lab
El proyecto está basado en un Quick Lab de Snowflake, demostrando un pipeline de pruebas utilizando dbt y Airflow.

