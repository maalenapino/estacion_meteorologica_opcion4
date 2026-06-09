CREATE DATABASE IF NOT EXISTS estacionmeteorologica_proa;
USE estacionmeteorologica_proa;

CREATE TABLE IF NOT EXISTS mediciones (
    id_mediciones INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperatura INT,          
    humedad INT               
);