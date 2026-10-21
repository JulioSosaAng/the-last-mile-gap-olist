# Recomendaciones y Hallazgos — The Last Mile Gap

## Hallazgo 1: El impacto del retraso en la satisfacción
*(Responde a la Pregunta 1 del Business Case)*

- **Metodología:** Se agruparon los pedidos entregados según si superaron la fecha estimada (`is_late`) y se calculó el promedio de `review_score`.
- **Resultado:** 
  - Pedidos a tiempo: 88.653 pedidos con una reseña promedio de **4.29**.
  - Pedidos tardíos: 7.700 pedidos con una reseña promedio de **2.57**.
- **Conclusión preliminar:** Existe una correlación negativa directa y severa entre el retraso y la satisfacción. La caída de casi 1.7 estrellas confirma que la logística es el principal driver de insatisfacción en la plataforma.

## Hallazgo 2: Concentración geográfica de los retrasos
*(Responde a la Pregunta 2 del Business Case)*

- **Metodología:** Se calculó la tasa de pedidos tardíos agrupada por `customer_state` (filtrando estados con más de 100 pedidos).
- **Resultado (Top 5 estados con mayor retraso):**
  1. AL (Alagoas): 23.94% de pedidos tardíos.
  2. MA (Maranhão): 19.56%.
  3. PI (Piauí): 15.93%.
  4. CE (Ceará): 15.37%.
  5. SE (Sergipe): 15.22%.
- **Conclusión preliminar:** El problema no está distribuido uniformemente. Existe una fuerte correlación geográfica: los estados de la región Nordeste (más alejados de los principales centros de distribución) sufren las peores tasas de demora. Esto sugiere que las recomendaciones deben incluir acuerdos logísticos específicos para esta región.

## Hallazgo 3: Sellers de alto volumen con foco de insatisfacción
*(Responde a la Pregunta 3 del Business Case)*

- **Metodología:** Se cruzaron los ítems de pedidos, sellers y reseñas, agrupando por `seller_id` y filtrando por volumen (>50 pedidos).
- **Resultado (Top sellers con más pedidos tardíos):** 
  Los 5 sellers con peor performance absoluta están radicados en **SP (São Paulo)**. A pesar de tener una tasa de retraso porcentual menor que los estados del Nordeste, su enorme volumen de ventas hace que concentren entre 131 y 216 pedidos tardíos cada uno, con reseñas promedio que caen a **3.35 - 4.14**.
- **Conclusión preliminar:** Existen dos focos de acción: 1) Mejoras logísticas regionales en el Nordeste, y 2) Intervención directa (auditoría o acuerdos) con los grandes sellers de São Paulo para reducir su volumen de quejas y mejorar su reseña.

*(Próximamente: Hallazgo 4 con las recomendaciones accionables)*