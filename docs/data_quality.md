# Reporte de Calidad del Dato — Olist

## 1. Fechas de entrega nulas
- **Total de pedidos:** 99441
- **Pedidos sin fecha de entrega:** 2965 (2.98%)
- **Tratamiento:** Se excluyen del análisis de retrasos usando `WHERE order_delivered_customer_date IS NOT NULL` (ya aplicado en la vista `vw_order_delivery_metrics`).

## 2. Fechas inconsistentes
- **Pedidos entregados antes de la compra:** 0
- **Tratamiento:** Se consideran errores de sistema y no afectan el análisis general de retrasos.

## 3. Duplicados
- **Duplicados en `orders`:** 0
- **Duplicados en `order_items`:** 0
- **Tratamiento:** Ninguno. La granularidad se maneja con `DISTINCT order_id` cuando es necesario.