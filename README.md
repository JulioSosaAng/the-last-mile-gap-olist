# The Last Mile Gap — Olist Delivery & Satisfaction Analytics

> Analizando la brecha entre la entrega prometida y la experimentada en el marketplace Olist, y su impacto en la satisfacción del cliente.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)]()

## 📌 Sobre el proyecto

**The Last Mile Gap** es un proyecto de análisis de datos que investiga cómo los retrasos en la entrega afectan la satisfacción del cliente en **Olist**, un marketplace brasileño que conecta pequeños vendedores con clientes en todo el país.

El proyecto parte de una hipótesis verificable con el dataset público de Olist (2016–2018): los pedidos entregados a tiempo mantienen una reseña promedio cercana a 4.3 estrellas, mientras que los pedidos con retraso caen a ~2.5 estrellas. Sin embargo, no está claro **qué segmentos** (estado, seller, categoría) concentran los retrasos ni **qué factores operativos** explican esa caída. Este proyecto lo cuantifica y propone acciones priorizadas.

## 🎯 Objetivo

Identificar los focos de ineficiencia logística que más impactan en la satisfacción del cliente, segmentando el problema por región, seller y categoría de producto, y priorizando 2–3 acciones concretas que puedan ejecutarse con los datos disponibles.

👉 El detalle completo está en el [`business_case.md`](docs/business_case.md).

## 🛠️ Stack

| Capa | Herramienta | Rol |
| :--- | :--- | :--- |
| Procesamiento | Python + Pandas | ETL y limpieza |
| Base de datos | PostgreSQL (Neon / Supabase free tier) | Almacenamiento y análisis SQL |
| Análisis | SQL | Vistas analíticas y KPIs |
| Dashboard | Streamlit + Plotly | Visualización interactiva |
| Gestión | GitHub Projects | Backlog ágil y retrospectivas |

## 📁 Estructura del repositorio

```text
the-last-mile-gap-olist/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── business_case.md
│   ├── backlog.md
│   └── (recommendations, process_model, executive_summary — en construcción)
├── etl/
│   └── load_olist.py
├── sql/
│   ├── schema.sql
│   └── views.sql
├── notebooks/
│   └── 01_eda.ipynb
└── dashboard/
    └── app.py
```

## 🚀 Cómo ejecutar

> ⚠️ El proyecto está en desarrollo activo. Las instrucciones se irán completando a medida que avancen las iteraciones.

### 1. Clonar el repositorio

```bash
git clone https://github.com/JulioSosaAng/the-last-mile-gap-olist.git
cd the-last-mile-gap-olist
```

### 2. Crear entorno e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Descargar el dataset

Descargar los 9 CSVs de [Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y colocarlos en `data/`.

### 4. Configurar la base de datos

Crear un archivo `.env` en la raíz del proyecto con las credenciales de PostgreSQL:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=olist
DB_USER=tu_usuario
DB_PASSWORD=tu_password
```

### 5. Ejecutar el pipeline

```bash
python etl/load_olist.py
```

### 6. Levantar el dashboard

```bash
streamlit run dashboard/app.py
```

## 📚 Documentación

| Documento | Descripción |
| :--- | :--- |
| [`docs/business_case.md`](docs/business_case.md) | Contexto, problema, objetivo, KPIs, alcance y criterios de éxito |
| [`docs/backlog.md`](docs/backlog.md) | Historias de usuario, criterios de aceptación e iteraciones |
| `docs/recommendations.md` | (en construcción) Acciones priorizadas basadas en hallazgos |
| `docs/process_model.md` | (en construcción) Modelo AS-IS / TO-BE del proceso logístico |
| `docs/executive_summary.md` | (en construcción) Resumen ejecutivo de 1 página |

## 🧭 Por qué estas herramientas

- **Python + Pandas:** el pipeline ETL es reproducible y versionado. Pandas permite validar calidad del dato de forma explícita antes de cargar.
- **PostgreSQL:** el dataset tiene relaciones claras (PK/FK) y se beneficia de SQL real, no de un CSV plano. Además, permite exponer vistas analíticas reutilizables por el dashboard.
- **Streamlit:** permite un dashboard interactivo en Python puro, desplegable gratis en Community Cloud, sin necesidad de un frontend separado.
- **Plotly:** visualizaciones interactivas que se integran nativamente con Streamlit y soportan mapas, dispersión y filtros sin perder rendimiento.
- **GitHub Projects:** gestión ágil del backlog con historias de usuario, prioridad MoSCoW e iteraciones documentadas.

## 🗺️ Roadmap

| Iteración | Foco | Estado |
| :--- | :--- | :--- |
| 1 | Fundación y pipeline (ETL + esquema SQL + calidad del dato) | 🔄 En curso |
| 2 | Análisis MVP (5 preguntas clave + recomendaciones) | ⏳ Pendiente |
| 3 | Dashboard + artefactos de soporte (EDA, AS-IS/TO-BE, resumen ejecutivo) | ⏳ Pendiente |

## 🚫 Fuera de alcance

Este proyecto no incluye modelos predictivos de ML, análisis de sentimiento sobre texto libre, cálculo de CLV ni integración con datos externos. El foco es el análisis descriptivo y la priorización accionable. Las extensiones futuras se documentan en la sección 10 del business case.

## 👤 Autor

**Julio Sosa**
[GitHub](https://github.com/JulioSosaAng) · [LinkedIn](https://linkedin.com/in/jsangeles) · [Portfolio](https://juliososaang.github.io/mi-portfolio/)

---

*Proyecto de portafolio · Dataset: [Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)*