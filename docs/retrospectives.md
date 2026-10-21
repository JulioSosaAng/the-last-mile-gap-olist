# Retrospectivas del Proyecto (Agile)

Este documento registra las retrospectivas al final de cada iteración, siguiendo el formato clásico ágil: *¿Qué salió bien?*, *¿Qué se puede mejorar?* y *Plan de acción*.

## Iteración 1: Fundación y Pipeline
- **¿Qué salió bien?** El diseño del esquema relacional en PostgreSQL y la conexión exitosa con Neon. La lógica del ETL en Python demostró ser robusta.
- **¿Qué se puede mejorar?** La velocidad inicial de carga de la tabla `geolocation` fue muy lenta.
- **Plan de acción:** Se implementó `chunksize=5000` y `method='multi'` en Pandas `to_sql`, acelerando futuras cargas masivas.

## Iteración 2: Análisis MVP y Recomendaciones
- **¿Qué salió bien?** La validación de la hipótesis principal (caída de 4.29 a 2.57 estrellas) y la facilidad para identificar patrones geográficos (Nordeste) y de vendedores (SP).
- **¿Qué se puede mejorar?** La exploración inicial de datos requería escribir consultas SQL muy largas en el editor de Neon.
- **Plan de acción:** Se consolidaron las métricas en vistas SQL (`vw_order_delivery_metrics`), optimizando las consultas para el futuro dashboard.

## Iteración 3: Dashboard y Artefactos de Soporte
- **¿Qué salió bien?** La implementación de Streamlit y Plotly permitió crear una interfaz muy profesional. Los filtros interactivos funcionan sin demoras.
- **¿Qué se puede mejorar?** El despliegue en Streamlit Cloud falló inicialmente por la versión de Python (3.14) y las dependencias.
- **Plan de acción:** Se fijó el entorno a Python 3.12 (`runtime.txt`) y se actualizaron las versiones en `requirements.txt`, logrando un despliegue exitoso.