import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# 1. Cargar variables de entorno
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Configurar conexión a PostgreSQL
if not DATABASE_URL:
    raise ValueError("❌ No se encontró la variable DATABASE_URL en el archivo .env")

engine = create_engine(DATABASE_URL)

# 3. Definir las tablas y sus nombres de archivo
# El orden importa para futuras llaves foráneas
archivos = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv"
}

# 4. Columnas que son fechas y deben parsearse
columnas_fecha = {
    "orders": ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"],
    "order_items": ["shipping_limit_date"],
    "order_reviews": ["review_creation_date", "review_answer_timestamp"]
}

DATA_DIR = Path("data")

def cargar_datos():
    print("🚀 Iniciando pipeline ETL de Olist...\n")
    
    for tabla, archivo in archivos.items():
        ruta_archivo = DATA_DIR / archivo
        
        if not ruta_archivo.exists():
            print(f"⚠️  Archivo no encontrado: {archivo}. Saltando...")
            continue
            
        print(f"Leyendo {archivo}...")
        
        # Leer CSV
        df = pd.read_csv(ruta_archivo)
        
        # Parsear fechas si corresponde
        if tabla in columnas_fecha:
            for col in columnas_fecha[tabla]:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        # Subir a PostgreSQL
        try:
            df.to_sql(tabla, engine, if_exists='replace', index=False, method='multi', chunksize=5000)
            print(f"✅ Tabla '{tabla}' cargada con {len(df)} filas.")
        except Exception as e:
            print(f"❌ Error al cargar {tabla}: {e}")

    print("\n🎉 Pipeline finalizado.")

if __name__ == "__main__":
    cargar_datos()