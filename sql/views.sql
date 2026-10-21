-- 1. Vista principal de métricas de entrega
-- Calcula si el pedido llegó tarde y lo une con su reseña
CREATE OR REPLACE VIEW vw_order_delivery_metrics AS
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_state,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    r.review_score,
    -- Diferencia en días entre lo real y lo estimado
    DATE_PART('day', o.order_delivered_customer_date - o.order_estimated_delivery_date) AS dias_diferencia,
    -- Flag: 1 si llegó tarde, 0 si llegó a tiempo o antes
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 
        ELSE 0 
    END AS is_late
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered' 
  AND o.order_delivered_customer_date IS NOT NULL;