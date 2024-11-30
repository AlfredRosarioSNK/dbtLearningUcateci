-- Seleccionamos la fecha de reserva, el hotel, y contamos el número de reservas (ID) realizadas
SELECT
  BOOKING_DATE, -- Fecha en la que se realizó la reserva
  HOTEL,        -- Nombre o identificador del hotel
  COUNT(ID) as count_bookings -- Número total de reservas por combinación de hotel y fecha
FROM {{ ref('prepped_data') }} -- Tabla o vista preprocesada en dbt
GROUP BY
  BOOKING_DATE, -- Agrupamos por fecha de reserva
  HOTEL         -- Agrupamos por hotel
