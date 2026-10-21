import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Configuración de la página
st.set_page_config(page_title="The Last Mile Gap", page_icon="📦", layout="wide")

# Cargar variables de entorno
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Para cuando esté en Streamlit Cloud, leerá de st.secrets
if not DATABASE_URL:
    DATABASE_URL = st.secrets["DATABASE_URL"]

# Conexión a la base de datos (usamos caché para no reconectar en cada clic)
@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# Función para cargar datos (usamos caché de datos)
@st.cache_data
def load_data():
    query = "SELECT * FROM vw_order_delivery_metrics WHERE review_score IS NOT NULL"
    return pd.read_sql(query, engine)

df = load_data()

# --- INTERFAZ ---
st.title("📦 The Last Mile Gap")
st.markdown("### Análisis de Retrasos y Satisfacción en Olist")

# KPIs Principales
col1, col2, col3 = st.columns(3)

total_pedidos = len(df)
pedidos_tardios = df['is_late'].sum()
tasa_tardios = (pedidos_tardios / total_pedidos) * 100
resena_promedio_tarde = df[df['is_late'] == 1]['review_score'].mean()

col1.metric("Total Pedidos Analizados", f"{total_pedidos:,}")
col2.metric("Tasa de Pedidos Tardíos", f"{tasa_tardios:.2f}%")
col3.metric("Reseña Promedio (Tardíos)", f"{resena_promedio_tarde:.2f} ⭐")

st.divider()

# Gráfico 1: La brecha de satisfacción (Pregunta 1)
st.subheader("1. Impacto del retraso en la satisfacción")
df_agrupado = df.groupby('is_late')['review_score'].mean().reset_index()
df_agrupado['Estado'] = df_agrupado['is_late'].map({0: 'A tiempo', 1: 'Tardío'})

fig1 = px.bar(df_agrupado, x='Estado', y='review_score', 
              color='Estado',
              color_discrete_sequence=['#2ca02c', '#d62728'],
              labels={'review_score': 'Reseña Promedio'})
fig1.update_layout(
    showlegend=False, 
    height=400,
    xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
    yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black'))
)
fig1.update_traces(texttemplate='<b>%{y:.2f}</b>', textfont_size=16)
st.plotly_chart(fig1, use_container_width=True)

st.info("💡 **Hallazgo:** Los pedidos tardíos reducen la calificación promedio en casi 1.7 estrellas (de 4.29 a 2.57).")

# --- BARRA LATERAL (Filtros) ---
st.sidebar.header("Filtros Interactivos")
# Creamos una lista con todos los estados disponibles
lista_estados = df['customer_state'].unique()
# El usuario puede elegir uno o varios estados
estados_seleccionados = st.sidebar.multiselect(
    "Selecciona los Estados (customer_state):",
    options=lista_estados,
    default=lista_estados[:5] # Por defecto mostramos 5 para no saturar
)

# Filtramos el DataFrame original según la selección del usuario
if estados_seleccionados:
    df_filtrado = df[df['customer_state'].isin(estados_seleccionados)]
else:
    df_filtrado = df # Si no selecciona nada, mostramos todo

# --- GRÁFICO 2: Retraso por Estado (Pregunta 2) ---
st.divider()
st.subheader("2. Tasa de retrasos por Estado (Top 10)")

# Agrupamos por estado y calculamos el % de retraso
df_estados = df_filtrado.groupby('customer_state')['is_late'].mean().reset_index()
df_estados['porcentaje_tardios'] = df_estados['is_late'] * 100

# Ordenamos de mayor a menor y tomamos el Top 10
df_estados_top = df_estados.sort_values(by='porcentaje_tardios', ascending=False).head(10)

fig2 = px.bar(
    df_estados_top, 
    x='customer_state', 
    y='porcentaje_tardios',
    color='porcentaje_tardios',
    color_continuous_scale='YlOrRd', # <-- Cambiamos a Amarillo-Naranja-Rojo
    labels={'customer_state': 'Estado', 'porcentaje_tardios': '% Pedidos Tardíos'}
)

fig2.update_layout(
    height=400, 
    coloraxis_showscale=False,
    coloraxis_cmin=0,
    coloraxis_cmax=15,
    xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
    yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black'))
)

# Forzamos el color del texto a negro para que se lea sobre el amarillo
fig2.update_traces(textfont_color='black')
fig2.update_traces(texttemplate='<b>%{y:.2f}</b>', textfont=dict(color='black', size=16))

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Hallazgo:** Los estados de la región Nordeste (AL, MA, PI, CE, SE) presentan las peores tasas de retraso, superando el 15%.")

# --- GRÁFICO 3 Y 4: Sellers y Categorías ---
st.divider()
st.subheader("3. Análisis por Sellers y Categorías")

# Creamos dos columnas para que se vean lado a lado
col_izq, col_der = st.columns(2)

# 1. Consulta para Categorías (Pregunta 4)
@st.cache_data
def load_categorias():
    query = """
    SELECT 
        COALESCE(pct.product_category_name_english, p.product_category_name) AS categoria,
        ROUND(AVG(r.review_score), 2) AS resena_promedio,
        ROUND((SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT o.order_id)), 2) AS porcentaje_tardios
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_category_name_translation pct ON p.product_category_name = pct.product_category_name
    JOIN orders o ON oi.order_id = o.order_id
    LEFT JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered' AND p.product_category_name IS NOT NULL
    GROUP BY p.product_category_name, pct.product_category_name_english
    HAVING COUNT(DISTINCT o.order_id) > 100
    ORDER BY resena_promedio ASC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

df_cat = load_categorias()

with col_izq:
    st.markdown("**Top 10 Categorías con peor reseña**")
    
    # Scatter plot limpio, sin textos superpuestos
    fig3 = px.scatter(
        df_cat, 
        x='porcentaje_tardios', 
        y='resena_promedio',
        hover_name='categoria', # Muestra el nombre al pasar el mouse
        labels={'porcentaje_tardios': '% Retrasos', 'resena_promedio': 'Reseña Promedio'}
    )
    
    # Personalizamos los puntos (todos del mismo tamaño y color)
    fig3.update_traces(
        marker=dict(size=12, color='#d62728', line=dict(width=1, color='black')) 
    )
    
    # Ajustamos el diseño y los ejes
    fig3.update_layout(
        height=400, 
        xaxis_title="% Pedidos Tardíos", 
        yaxis_title="Reseña Promedio",
        yaxis=dict(
            range=[3.0, 4.5], 
            title_font=dict(color='black'), 
            tickfont=dict(color='black')
        ),
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        margin=dict(t=10),
        hoverlabel=dict(
            bgcolor="white",          
            font=dict(color="black", size=14), 
            bordercolor="black"       
        )
    )
    # Le agrega el signo de porcentaje al eje X
    fig3.update_xaxes(ticksuffix="%")
    
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Pasa el mouse por los puntos para ver la categoría. Muebles de oficina y electrónica tienen malas reseñas incluso con pocos retrasos (problema de producto), mientras que 'audio' sufre ambos problemas.")

# 2. Consulta para Sellers (Pregunta 3)
@st.cache_data
def load_sellers():
    query = """
    SELECT 
        LEFT(s.seller_id, 8) AS seller_id_corto,
        s.seller_state,
        COUNT(DISTINCT oi.order_id) AS total_pedidos,
        SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS pedidos_tardios
    FROM order_items oi
    JOIN sellers s ON oi.seller_id = s.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY s.seller_id, s.seller_state
    HAVING COUNT(DISTINCT oi.order_id) > 50
    ORDER BY pedidos_tardios DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

df_sell = load_sellers()

with col_der:
    st.markdown("**Top 10 Sellers con más pedidos tardíos**")
    fig4 = px.bar(
        df_sell,
        x='pedidos_tardios',
        y='seller_id_corto', # Usamos el ID corto
        orientation='h',
        text_auto='<b>.0f</b>',
        labels={'pedidos_tardios': 'Pedidos con retraso', 'seller_id_corto': 'ID del Seller'},
        color_discrete_sequence=['#1f77b4'] # Color azul fijo para todas
    )
    fig4.update_traces(textfont_size=14)
    fig4.update_layout(
        height=400, 
        showlegend=False, # Ocultamos la leyenda de colores
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(
            categoryorder='total ascending',
            title_font=dict(color='black'), 
            tickfont=dict(color='black')
        ),
        hoverlabel=dict(
            bgcolor="white",          
            font=dict(color="black", size=14), 
            bordercolor="black"       
        )
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Los grandes vendedores de São Paulo (SP) concentran el mayor volumen absoluto de quejas, a pesar de tener una tasa de error menor que el Nordeste.")