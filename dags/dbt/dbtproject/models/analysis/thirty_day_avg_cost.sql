-- Seleccionamos los datos de reservas, calculando el promedio móvil de 30 días y la diferencia con el costo actual
SELECT
  BOOKING_DATE, -- Fecha en la que se realizó la reserva
  HOTEL,        -- Nombre o identificador del hotel
  COST,         -- Costo de la reserva
  -- Calculamos el promedio móvil de 30 días usando una ventana sobre las filas de los 29 días anteriores más el día actual
  AVG(COST) OVER (
    ORDER BY BOOKING_DATE ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) as "30_DAY_AVG_COST", -- Promedio móvil del costo en los últimos 30 días (incluyendo el actual)
  -- Calculamos la diferencia entre el costo actual y el promedio móvil de 30 días
  COST - AVG(COST) OVER (
    ORDER BY BOOKING_DATE ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) as "DIFF_BTW_ACTUAL_AVG" -- Diferencia entre el costo actual y el promedio móvil
FROM {{ ref('prepped_data') }} -- Tabla o vista preprocesada en dbt
