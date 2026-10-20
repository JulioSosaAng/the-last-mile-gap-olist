# Business Case: The Last Mile Gap — Olist Delivery & Satisfaction Analytics

## 1. Contexto
- Olist es un marketplace brasileño que conecta a pequeños vendedores con clientes en todo el país. Su operación depende de una red logística externa y de la performance de miles de sellers independientes. El dataset público de Olist cubre pedidos entre 2016 y 2018 e incluye información de órdenes, ítems, pagos, reseñas, productos, vendedores y ubicación geográfica de clientes y sellers. Es un caso realista de e-commerce con datos estructurados y relaciones claras entre tablas.

## 2. Problema de negocio
- La satisfacción del cliente en Olist está fuertemente condicionada por la experiencia logística. Análisis previos sobre este mismo dataset muestran que los pedidos entregados a tiempo mantienen una reseña promedio cercana a 4.3 estrellas, mientras que los pedidos con retraso caen a valores cercanos a 2.5 estrellas. Sin embargo, no está claro qué segmentos concentran los retrasos ni qué factores operativos (seller, región de destino, categoría de producto) explican esa caída. Sin esa claridad, Olist no puede priorizar acciones correctivas ni asignar recursos de mejora logística de forma efectiva.

## 3. Objetivo del análisis
- Identificar los focos de ineficiencia logística que más impactan en la satisfacción del cliente, cuantificando el efecto de los retrasos sobre las reseñas y segmentando el problema por región, seller y categoría. El resultado debe permitir priorizar 2–3 acciones concretas (por ejemplo, intervención sobre sellers con mayor tasa de demora, ajuste de expectativas de entrega en regiones críticas, o revisión de categorías con peor desempeño) que puedan ejecutarse con los datos disponibles.

## 4. Preguntas clave (3–5)
1. ¿Cuál es la relación entre el retraso en la entrega y la reseña del cliente?
   - Tablas: orders (fechas real vs. estimada) + order_reviews (review_score). Es la pregunta ancla del proyecto.
2. ¿Qué estados (customer_state) concentran la mayor proporción de pedidos entregados fuera de plazo?
   - Tablas: orders + customers. Permite segmentar geográficamente el problema.
3. ¿Qué sellers presentan la peor combinación de retraso y reseña promedio?
   - Tablas: orders + order_items + sellers + order_reviews. Identifica focos de intervención operativa.
4. ¿Qué categorías de producto (product_category_name) tienen la peor reseña promedio y si esa caída está asociada a retrasos?
   - Tablas: order_items + products + orders + order_reviews. Distingue si el problema es logístico o de producto.
5. ¿El retraso afecta por igual a pedidos con uno o varios ítems?
   - Tablas: order_items + orders. Controla la granularidad del dataset (un pedido puede tener varias filas) y evita conclusiones sesgadas.

## 5. Alcance
**Incluye:**
- Análisis de pedidos con estado delivered (entregados) dentro de la ventana 2016–2018 del dataset.
- Cálculo de retraso como order_delivered_customer_date > order_estimated_delivery_date.
- Cruce con order_reviews para medir satisfacción por segmento (estado, seller, categoría).
- Un dashboard interactivo (Streamlit + Plotly) con los KPIs y los filtros principales.
- Documentación del pipeline (Python + SQL) y del backlog ágil.

**No incluye:**
- Predicción de retrasos ni modelos de machine learning (el objetivo es descriptivo y de priorización, no predictivo).
- Análisis de sentimiento sobre el texto libre de las reseñas (el dataset tiene campos de comentario, pero eso desviaría el foco del problema logístico).
- Cálculo de retención o CLV basado en customer_unique_id (es un análisis valioso, pero pertenece a otro proyecto).
- Datos externos (población, competencia, costos operativos reales) que no estén en el dataset de Olist.

## 6. Stakeholders (Roles Ficticios)
- Gerencia de Operaciones / Logística: es el stakeholder principal. Necesita saber qué estados y sellers concentran los retrasos para priorizar acuerdos con operadores logísticos y acciones de mejora.
- Equipo de Gestión de Sellers: le interesa identificar sellers con mala performance (retrasos + reseñas bajas) para decidir intervenciones, capacitación o revisión de acuerdos comerciales.
- Equipo de Calidad / Experiencia del Cliente: quiere entender qué categorías de producto y qué segmentos geográficos generan peor satisfacción, para ajustar expectativas de entrega y comunicación al cliente.
- Gerencia Comercial / Category Management: usa los hallazgos por categoría para decidir dónde enfocar campañas o revisar el catálogo.
- Analista de Datos / BI (rol espejo): consume el pipeline y el dashboard como base para reportes recurrentes; es el rol que más se beneficia de la automatización (Python + SQL) y de la documentación ágil.

## 7. KPIs propuestos
- KPIs de logística:
  - Tasa de entregas tardías: % de pedidos delivered donde order_delivered_customer_date > order_estimated_delivery_date. Base: orders.
  - Días promedio de retraso: promedio de order_delivered_customer_date − order_estimated_delivery_date solo en pedidos tardíos. Base: orders.
  - Tiempo promedio de entrega real: order_delivered_customer_date − order_purchase_timestamp. Base: orders.
- KPIs de satisfacción:
  - Reseña promedio: promedio de review_score. Base: order_reviews.
  - % de reseñas negativas: % de review_score ≤ 2. Base: order_reviews.
  - Brecha de satisfacción por retraso: diferencia de reseña promedio entre pedidos a tiempo y pedidos tardíos. Es el KPI ancla del proyecto (pregunta 1).
- KPIs de segmentación:
  - Tasa de retraso por estado (customer_state): % de pedidos tardíos por estado. Base: orders + customers.
  - Tasa de retraso y reseña promedio por seller: ranking de sellers con peor performance. Base: orders + order_items + sellers + order_reviews.
  - Reseña promedio y tasa de retraso por categoría (product_category_name): Base: order_items + products + orders + order_reviews.
- KPI de calidad del dato (para el pipeline):
  - % de pedidos con fechas de entrega nulas o inconsistentes: sirve para documentar la limpieza y demostrar rigor técnico. Base: orders.

## 8. Entregables
- **MVP**
  - Pipeline de datos reproducible (Python + SQL):
    - etl/load_olist.py: lee los CSVs, valida calidad (nulos en fechas de entrega, duplicados en order_id, granularidad de order_items) y carga a PostgreSQL. Desarrollo en PostgreSQL local; despliegue contra una BD hospedada gratuita (Neon o Supabase free tier) para que el dashboard funcione en la nube.
    - sql/schema.sql y sql/views.sql: esquema y vistas analíticas (vw_order_delivery_metrics, vw_seller_performance, vw_category_performance).
  - Dashboard interactivo (Streamlit + Plotly): KPIs de la sección 7, filtros por estado, seller y categoría, y vista principal con la brecha de satisfacción por retraso. Desplegado en Streamlit Community Cloud conectado a la BD hospedada.
  - Documento de recomendaciones (docs/recommendations.md): 2–3 acciones priorizadas, cada una con segmento objetivo, KPI que mejora, esfuerzo estimado e impacto aproximado.

- **Artefactos de soporte**
  - Modelo del proceso de negocio AS-IS / TO-BE (docs/process_model.md): diagrama simple del flujo pedido → pago → aprobación → envío → entrega → reseña, con los puntos donde se originan los retrasos y la propuesta de mejora. Entrena directamente "business process modeling".
  - Análisis exploratorio documentado (notebooks/01_eda.ipynb): hallazgos, decisiones de limpieza y respuestas a las preguntas 1–5, referenciando las consultas SQL usadas.
  - Resumen ejecutivo de 1 página (docs/executive_summary.md): problema, hallazgo principal, recomendación y siguiente paso, en lenguaje no técnico. Entrena "technical communication and consultation".
  - Documentación ágil (docs/backlog.md + tablero en GitHub Projects): historias de usuario con criterios de aceptación, definición de hecho e iteraciones con retrospectiva.
  - README del repositorio: visión general, stack, cómo ejecutar el pipeline, enlaces al dashboard y al business case, y una sección breve de "por qué estas herramientas" (justifica Streamlit, Plotly, PostgreSQL; entrena "embracing emerging technologies").

## 9. Criterios de éxito
- Cobertura analítica: las 5 preguntas clave de la sección 4 tienen respuesta documentada con consultas SQL y visualizaciones.
- Reproducibilidad: cualquier persona puede clonar el repo, ejecutar el pipeline contra la BD hospedada y levantar el dashboard siguiendo el README, sin intervención manual.
- Accionabilidad: al menos 2 recomendaciones priorizadas, cada una con segmento, KPI, esfuerzo e impacto estimado.
- Calidad del dato: el pipeline reporta el % de pedidos con fechas inconsistentes y documenta el tratamiento aplicado (excluidos, imputados o marcados).
- Comunicación: una persona no técnica puede responder la pregunta 1 (brecha de satisfacción por retraso) usando solo el dashboard, sin leer SQL ni documentación técnica. Idealmente validado con alguien externo al proyecto.
- Modelado de proceso: el documento AS-IS/TO-BE identifica al menos 2 puntos del proceso donde se origina el retraso y los conecta con una recomendación concreta.
- Gestión ágil: al menos 2 iteraciones documentadas (planificación → ejecución → retrospectiva) con el tablero actualizado y la definición de hecho aplicada.

## 10. Supuestos / Próximos pasos

### Supuestos
- Dataset público de Olist (Kaggle), sin datos externos.
- Análisis limitado a pedidos con estado delivered y fechas de entrega no nulas.
- Roles de la sección 6 ficticios pero realistas (caso de portafolio).
- PostgreSQL local para desarrollo y una BD hospedada gratuita (Neon o Supabase free tier) para el despliegue del dashboard en Streamlit Community Cloud.
- El MVP es pipeline + dashboard + recomendaciones; el EDA, el modelo de proceso y los documentos ágiles se completan en iteraciones posteriores.

### Próximos pasos (fuera del alcance actual)
- Modelo predictivo de retrasos (ML): variables de seller, región y categoría para anticipar pedidos en riesgo.
- Análisis de sentimiento (NLP): sobre review_comment_message para complementar el review_score numérico.
- Recurrencia y CLV: usando customer_unique_id para medir retención y valor del cliente.
- Transformaciones con dbt y orquestación con un scheduler (cron o Airflow).
- Versionado de datos con DVC o lakeFS (no con dbt, que es para transformaciones).
- Integración con datos externos: población por estado o costos logísticos, para enriquecer el análisis de retrasos.