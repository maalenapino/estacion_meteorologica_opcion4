



-- 1. Creación de la base de datos
CREATE DATABASE IF NOT EXISTS estacionmetereologica_proa;

USE estacionmetereologica_proa;

-- 2. Creación de la tabla mediciones
CREATE TABLE IF NOT EXISTS mediciones (
    id_mediciones INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperatura INT, -- El DHT11 mide de 1 en 1 grado, INT es eficiente
    humedad INT      -- Guardamos un INT ya que la humedad del DHT11 viene entera
);

-- Agregar la columna 'gas' justo después de 'humedad'
ALTER TABLE mediciones 
ADD COLUMN gas INT AFTER humedad;


-- 3. Inserción de prueba (Opcional para verificar)
INSERT INTO mediciones (temperatura, humedad) VALUES (24, 55); 

-- 3. Inserciones de prueba (Normal, Calor y Fuga de Gas)
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (24, 55, 120); -- Óptimo
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (36, 40, 150); -- Alerta Calor
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (22, 60, 480); -- Alerta Fuga de Gas


-- 4. Ver todos los datos crudos
SELECT * FROM mediciones;

-- 5. Consulta Avanzada con Reporte de Diagnóstico Inteligente (Acorde al Arduino)
-- SQL temperaturas
SELECT 
    fecha_hora,
    temperatura,
    humedad,
    CASE 
        WHEN temperatura >= 35 THEN 'ALERTA: CALOR EXTREMO'
        WHEN temperatura >= 30 AND temperatura < 35 THEN 'PRECAUCIÓN: TEMP ELEVADA'
        WHEN temperatura < 15 THEN 'ALERTA: FRÍO EXTREMO'
        ELSE 'ESTADO ÓPTIMO'
    END AS diagnostico_clima
FROM mediciones 
ORDER BY fecha_hora DESC;


-- 4. Consulta Avanzada con Diagnóstico Inteligente Multi-Sensor
SELECT 
    fecha_hora,
    temperatura,
    humedad,
    gas,
    CASE 
        WHEN gas > 300 THEN 'ALERTA: GAS / ANOMALÍA EN AIRE'
        WHEN temperatura >= 35 THEN 'ALERTA: CALOR EXTREMO'
        WHEN temperatura <= 15 THEN 'ALERTA: FRÍO EXTREMO'
        ELSE 'ESTADO ÓPTIMO'
    END AS diagnostico_integral
FROM mediciones 
ORDER BY fecha_hora DESC;



SELECT 
    fecha_hora,
    gas,
    CASE 
        WHEN gas > 500 THEN 'ALERTA CRÍTICA: FUGA DE GAS / CONCENTRACIÓN ALTA'
        WHEN gas BETWEEN 250 AND 500 THEN 'ALERTA MEDIA: HUMO / VAPORES EN AIRE'
        WHEN gas BETWEEN 120 AND 249 THEN 'PRECAUCIÓN: AIRE POCO PURO'
        ELSE 'ESTADO ÓPTIMO'
    END AS diagnostico_aire
FROM mediciones 
ORDER BY id_mediciones DESC;


SELECT user, host
FROM mysql.user;
