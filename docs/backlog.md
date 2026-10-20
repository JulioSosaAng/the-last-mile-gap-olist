# Backlog — The Last Mile Gap

> Este documento es el espejo versionado del tablero en GitHub Projects.
> La fuente operativa es el tablero; este archivo se actualiza al inicio y cierre de cada iteración.

## Definición de Hecho (DoD)

Aplica a todas las historias de usuario:

- [ ] Código versionado con commit descriptivo en el repo
- [ ] Documentación actualizada (`README.md` o `docs/`)
- [ ] Criterios de aceptación verificados
- [ ] Si aplica: resultado visible en el dashboard o en un documento de `docs/`
- [ ] Sin secretos ni credenciales en el código (uso de `.env`)

## Prioridad (MoSCoW)

- **Must:** obligatorio para el MVP
- **Should:** importante pero no bloquea el MVP
- **Could:** valioso si hay tiempo
- **Won't:** fuera de alcance (ver sección 5 del business case)

## Iteraciones

| Iteración | Foco | Historias |
| :--- | :--- | :--- |
| 1 | Fundación y pipeline | US-01 a US-04 |
| 2 | Análisis MVP y recomendaciones | US-05 a US-10 |
| 3 | Dashboard y artefactos de soporte | US-11 a US-15 |

---

## Iteración 1 — Fundación y pipeline

### US-01: Estructura inicial del repositorio
**Como** analista, **quiero** tener la estructura base del repo (`docs/`, `etl/`, `sql/`, `notebooks/`, `dashboard/`, `requirements.txt`, `.gitignore`) **para** empezar a trabajar de forma ordenada.

**Prioridad:** Must · **Estimación:** 1

**Criterios de aceptación:**
- [ ] Carpetas creadas según estructura acordada
- [ ] `requirements.txt` con pandas, sqlalchemy, psycopg2-binary, streamlit, plotly, python-dotenv
- [ ] `.gitignore` excluye `data/`, `.env`, `__pycache__/`, `*.ipynb_checkpoints`
- [ ] `README.md` inicial con nombre del proyecto y descripción de una línea
- [ ] Commit inicial subido a GitHub

### US-02: Pipeline de carga ETL
**Como** analista, **quiero** un script en Python que lea los CSVs de Olist y los cargue a PostgreSQL **para** tener los datos disponibles para análisis SQL.

**Prioridad:** Must · **Estimación:** 5

**Criterios de aceptación:**
- [ ] `etl/load_olist.py` lee los 9 CSVs del dataset (`customers`, `orders`, `order_items`, `order_payments`, `order_reviews`, `products`, `sellers`, `geolocation`, `product_category_name_translation`)
- [ ] Crea el esquema si no existe
- [ ] Aplica tipos de datos correctos: fechas como `TIMESTAMP`, precios como `NUMERIC`, IDs como `VARCHAR`
- [ ] Reporta al final: filas cargadas por tabla y advertencias detectadas
- [ ] Ejecutable con `python etl/load_olist.py`
- [ ] Parámetros de conexión leídos desde `.env` (no hardcodeados)
- [ ] Documentado en README

### US-03: Esquema SQL y vistas analíticas
**Como** analista, **quiero** crear el esquema SQL y las vistas de KPIs **para** reutilizarlas en análisis y dashboard sin repetir lógica.

**Prioridad:** Must · **Estimación:** 5

**Criterios de aceptación:**
- [ ] `sql/schema.sql` crea tablas con PK/FK correctas según el modelo del dataset
- [ ] `sql/views.sql` incluye `vw_order_delivery_metrics`, `vw_seller_performance`, `vw_category_performance`
- [ ] Cada vista implementa uno o más KPIs de la sección 7 del business case
- [ ] Las vistas usan `DISTINCT order_id` cuando corresponde para no inflar métricas por granularidad de `order_items`
- [ ] Ejecutables en orden (`schema.sql` → `views.sql`) sin errores

### US-04: Reporte de calidad del dato
**Como** analista, **quiero** un reporte de calidad del dato **para** documentar el rigor técnico y justificar las decisiones de limpieza.

**Prioridad:** Should · **Estimación:** 3

**Criterios de aceptación:**
- [ ] Reporta % de pedidos con `order_delivered_customer_date` nula
- [ ] Reporta % de pedidos con fechas inconsistentes (`order_delivered_customer_date` < `order_purchase_timestamp`)
- [ ] Reporta duplicados por `order_id` en `orders`
- [ ] Reporta duplicados por `order_id` + `order_item_id` en `order_items`
- [ ] Salida en consola + `docs/data_quality.md`
- [ ] Documenta el tratamiento aplicado (excluido / imputado / marcado)

---

## Iteración 2 — Análisis MVP y recomendaciones

### US-05: Análisis de retraso vs. reseña (Pregunta 1)
**Como** Gerencia de Operaciones, **quiero** cuantificar la brecha de satisfacción entre pedidos a tiempo y pedidos tardíos **para** demostrar el impacto del retraso en la reseña.

**Prioridad:** Must · **Estimación:** 3

**Criterios de aceptación:**
- [ ] Consulta SQL que compara reseña promedio entre pedidos a tiempo y tardíos
- [ ] Resultado: brecha en estrellas (valor numérico)
- [ ] Visualización (barras o violin plot) guardada en el notebook o dashboard
- [ ] Hallazgo documentado en `docs/recommendations.md`

### US-06: Tasa de retraso por estado (Pregunta 2)
**Como** Gerencia de Operaciones, **quiero** identificar los estados con mayor proporción de pedidos tardíos **para** priorizar acciones logísticas por región.

**Prioridad:** Must · **Estimación:** 3

**Criterios de aceptación:**
- [ ] Consulta SQL con `JOIN` entre `orders` y `customers` por `customer_state`
- [ ] Ranking de estados por tasa de retraso (con volumen mínimo para evitar ruido)
- [ ] Mapa o barra horizontal con top 10 estados
- [ ] Hallazgo documentado en `docs/recommendations.md`

### US-07: Sellers con peor performance (Pregunta 3)
**Como** Equipo de Gestión de Sellers, **quiero** un ranking de sellers con peor combinación de retraso y reseña **para** decidir intervenciones.

**Prioridad:** Must · **Estimación:** 5

**Criterios de aceptación:**
- [ ] Consulta con `JOIN` entre `orders`, `order_items`, `sellers` y `order_reviews`
- [ ] Ranking con al menos 10 sellers y umbral mínimo de pedidos (evitar sellers con 1 pedido)
- [ ] Columnas: `seller_id`, `customer_state` predominante, `% tardíos`, reseña promedio, nº pedidos
- [ ] Hallazgo documentado en `docs/recommendations.md`

### US-08: Categorías con peor reseña (Pregunta 4)
**Como** Gerencia Comercial, **quiero** identificar las categorías con peor reseña promedio y determinar si la caída está asociada a retrasos **para** decidir revisiones de catálogo o de expectativas de entrega.

**Prioridad:** Must · **Estimación:** 5

**Criterios de aceptación:**
- [ ] Consulta con `JOIN` entre `order_items`, `products`, `orders` y `order_reviews`
- [ ] Categorías ordenadas por reseña promedio ascendente (con volumen mínimo)
- [ ] Columna adicional: % de retraso por categoría, para distinguir causa logística vs. producto
- [ ] Visualización de dispersión (tasa de retraso vs. reseña promedio)
- [ ] Hallazgo documentado en `docs/recommendations.md`

### US-09: Retraso por cantidad de ítems (Pregunta 5)
**Como** analista, **quiero** verificar si el retraso varía según la cantidad de ítems del pedido **para** descartar sesgos de granularidad.

**Prioridad:** Must · **Estimación:** 3

**Criterios de aceptación:**
- [ ] Consulta que calcula tasa de retraso agrupando pedidos por cantidad de ítems (1, 2, 3+)
- [ ] Uso de `DISTINCT order_id` o subconsulta para no inflar por `order_items`
- [ ] Resultado documentado en notebook
- [ ] Conclusión explícita: si hay o no sesgo de granularidad

### US-10: Documento de recomendaciones
**Como** stakeholder, **quiero** un documento con 2–3 acciones priorizadas **para** pasar del análisis a la decisión.

**Prioridad:** Must · **Estimación:** 5

**Criterios de aceptación:**
- [ ] `docs/recommendations.md` con al menos 2 recomendaciones
- [ ] Cada recomendación incluye: segmento objetivo, KPI que mejora, esfuerzo estimado, impacto estimado
- [ ] Cada recomendación se traza a una pregunta de la sección 4 del business case
- [ ] Incluye una sección de "riesgos y supuestos"
- [ ] Revisado contra el criterio de accionabilidad de la sección 9 del business case

---

## Iteración 3 — Dashboard y artefactos de soporte

### US-11: Dashboard interactivo
**Como** stakeholder no técnico, **quiero** un dashboard que muestre los KPIs y permita filtrar **para** responder la pregunta 1 sin leer SQL.

**Prioridad:** Must · **Estimación:** 8

**Criterios de aceptación:**
- [ ] `dashboard/app.py` en Streamlit con al menos 4 KPIs de la sección 7
- [ ] Filtros: estado (`customer_state`), seller, categoría de producto
- [ ] Vista principal: brecha de satisfacción por retraso (respuesta a Pregunta 1)
- [ ] Conectado a la BD hospedada (Neon o Supabase free tier)
- [ ] Desplegado en Streamlit Community Cloud con URL pública
- [ ] URL documentada en README

### US-12: Notebook de EDA documentado
**Como** analista, **quiero** un notebook que documente la exploración y las decisiones de limpieza **para** dar trazabilidad al análisis.

**Prioridad:** Should · **Estimación:** 5

**Criterios de aceptación:**
- [ ] `notebooks/01_eda.ipynb` con secciones: contexto, carga, calidad del dato, hallazgos
- [ ] Cada pregunta de la sección 4 del business case tiene una celda de respuesta
- [ ] Las consultas SQL usadas están referenciadas o incluidas
- [ ] Conclusiones al final de cada sección

### US-13: Modelo de proceso AS-IS / TO-BE
**Como** stakeholder, **quiero** un modelo visual del proceso actual y propuesto **para** entender dónde se originan los retrasos y cómo la recomendación lo mejora.

**Prioridad:** Should · **Estimación:** 3

**Criterios de aceptación:**
- [ ] `docs/process_model.md` con diagrama AS-IS (pedido → pago → aprobación → envío → entrega → reseña)
- [ ] Identificación de al menos 2 puntos donde se origina el retraso
- [ ] Diagrama TO-BE conectado a una recomendación concreta de `docs/recommendations.md`

### US-14: Resumen ejecutivo
**Como** stakeholder no técnico, **quiero** un resumen de 1 página **para** entender el problema, el hallazgo y la recomendación sin leer el business case completo.

**Prioridad:** Should · **Estimación:** 2

**Criterios de aceptación:**
- [ ] `docs/executive_summary.md` de 1 página máximo
- [ ] Incluye: problema, hallazgo principal, recomendación, siguiente paso
- [ ] Sin jerga técnica ni referencias a tablas o queries
- [ ] Validado con una persona externa al proyecto (criterio de comunicación de la sección 9 del business case)

### US-15: README final y retrospectivas
**Como** visitante del repo, **quiero** un README que explique el proyecto y cómo ejecutarlo **para** reproducirlo sin ayuda.

**Prioridad:** Must · **Estimación:** 3

**Criterios de aceptación:**
- [ ] README con: visión general, stack, cómo ejecutar el pipeline, enlaces a dashboard, business case y recomendaciones
- [ ] Sección "por qué estas herramientas" (justifica Streamlit, Plotly, PostgreSQL)
- [ ] Retrospectivas de iteraciones 1 y 2 documentadas en `docs/retrospectives.md` (o sección en README)
- [ ] Badge de Streamlit y enlace a la URL pública del dashboard

---

## Fuera de alcance (Won't)

Ver sección 5 del `business_case.md`:

- Modelos de machine learning para predecir retrasos
- Análisis de sentimiento sobre `review_comment_message`
- Cálculo de retención o CLV con `customer_unique_id`
- Integración con datos externos