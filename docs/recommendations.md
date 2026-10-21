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

## Hallazgo 4: Categorías con peor reseña (Problema logístico vs. Producto)
*(Responde a la Pregunta 4 del Business Case)*

- **Metodología:** Agrupación por categoría de producto (con volumen > 100 pedidos), calculando reseña promedio y % de pedidos tardíos.
- **Resultado (Top 5 peores reseñas):**
  1. `office_furniture`: 3.52 estrellas (11.96% de retrasos).
  2. `fixed_telephony`: 3.76 estrellas (5.19% de retrasos).
  3. `fashion_male_clothing`: 3.76 estrellas (6.60% de retrasos).
  4. `audio`: 3.83 estrellas (13.22% de retrasos).
  5. `home_confort`: 3.85 estrellas (11.22% de retrasos).
- **Conclusión preliminar:** No todas las malas reseñas son culpa de la logística. Categorías como `fixed_telephony` y `fashion_male_clothing` tienen retrasos bajos pero reseñas malas (problema de producto/expectativa). En cambio, `audio`, `home_confort` y `office_furniture` combinan malas reseñas con altas tasas de retraso, lo que requiere intervención logística urgente (embalaje y transporte de voluminosos/frágiles).

## Hallazgo 5: Impacto de la cantidad de ítems en los retrasos
*(Responde a la Pregunta 5 del Business Case)*

- **Metodología:** Agrupación de pedidos según la cantidad de ítems y cálculo de la tasa de retraso por grupo.
- **Resultado:**
  - 1 ítem: 86.835 pedidos (8.29% tardíos).
  - 2 ítems: 7.392 pedidos (6.63% tardíos).
  - 3 ítems: 1.306 pedidos (6.20% tardíos).
  - 4+ ítems: 937 pedidos (6.19% tardíos).
- **Conclusión preliminar:** El retraso es transversal a todos los tamaños de pedido. La diferencia entre pedidos de 1 ítem y múltiples ítems no es lo suficientemente significativa como para sesgar los hallazgos anteriores. El problema logístico es sistémico.

---

# Recomendaciones Accionables (Plan de Acción)

Basado en los 5 hallazgos anteriores, se proponen las siguientes 3 acciones priorizadas para la Gerencia de Operaciones de Olist.

## Recomendación 1: Intervención y auditoría a Sellers de Alto Volumen en SP
- **Problema:** Sellers de São Paulo concentran el mayor volumen absoluto de pedidos tardíos (hasta 216 retrasos por seller) y reseñas bajas (3.35).
- **Acción:** Auditar los procesos de despacho de los Top 10 sellers de SP con mayor volumen de quejas. Implementar un SLA (Acuerdo de Nivel de Servicio) más estricto o multas por despacho tardío.
- **Segmento objetivo:** Top 10 Sellers de SP por volumen de ventas.
- **KPI que mejora:** Tasa de entregas tardías y reseña promedio general (brecha de satisfacción).
- **Esfuerzo estimado:** Medio (Requiere gestión comercial y análisis de contratos).
- **Impacto estimado:** Alto (Reduciría miles de quejas al año concentradas en pocos actores).

## Recomendación 2: Plan Logístico Especial para el Nordeste
- **Problema:** Los estados de AL, MA, PI, CE y SE presentan las peores tasas porcentuales de retraso (llegando a 23.94% en Alagoas).
- **Acción:** Negociar tarifas y rutas preferenciales con operadores logísticos para la región Nordeste. Ajustar los plazos de entrega estimados en la plataforma para que sean más realistas y no defrauden al cliente.
- **Segmento objetivo:** Clientes en los estados de la región Nordeste.
- **KPI que mejora:** Tasa de retraso por estado y expectativa del cliente (evitar el retraso percibido).
- **Esfuerzo estimado:** Alto (Requiere renegociación con transportistas externos).
- **Impacto estimado:** Alto (Mejora drástica de la experiencia en un 20-25% de la población brasileña).

## Recomendación 3: Mejora en Empaque y Logística de Categorías Críticas
- **Problema:** Categorías como `office_furniture`, `audio` y `home_confort` combinan altos porcentajes de retraso (11% - 13%) con malas reseñas.
- **Acción:** Implementar un programa de capacitación para sellers de estas categorías sobre embalaje seguro para productos frágiles y voluminosos. Priorizar el uso de transportistas especializados en carga pesada.
- **Segmento objetivo:** Sellers de las categorías `office_furniture`, `audio` y `home_confort`.
- **KPI que mejora:** Reseña promedio por categoría.
- **Esfuerzo estimado:** Medio (Creación de guías de embalaje y comunicación).
- **Impacto estimado:** Medio-Alto (Mejora en la percepción de calidad del producto y reduce devoluciones).

## Riesgos y Supuestos de las Recomendaciones

**Supuestos:**
1. Se asume que los centros de distribución principales de Olist (y de la mayoría de sus sellers) siguen estando concentrados en la región Sudeste (especialmente São Paulo), lo que explica la diferencia de tiempos hacia el Nordeste.
2. Se asume que el `review_score` refleja fielmente la experiencia de entrega y no está influenciado por otros factores externos no capturados en el dataset (como atención al cliente post-venta).
3. Los plazos estimados de entrega (`order_estimated_delivery_date`) son fijados por Olist o los sellers, y no por los operadores logísticos.

**Riesgos:**
1. **Resistencia de los sellers:** Auditar o presionar a los grandes sellers de SP puede generar fricción comercial o pérdida de volumen a corto plazo si no se maneja con cuidado.
2. **Dependencia de terceros:** Las mejoras logísticas en el Nordeste dependen de la capacidad y voluntad de los operadores logísticos externos para renegociar rutas y tarifas.
3. **Efecto de "expectativa":** Ajustar los plazos estimados para que sean más realistas reducirá la tasa de retraso *percibido* (el KPI), pero no necesariamente acelerará la entrega física real. El cliente podría seguir insatisfecho si la espera sigue siendo muy larga.

---
*Nota: Las estimaciones de esfuerzo e impacto son hipótesis de negocio basadas en el análisis descriptivo, no en modelos predictivos.*