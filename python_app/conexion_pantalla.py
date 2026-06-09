import random
import time

# Clase Sensor según la estructura formal del PDF de la escuela
class Sensor:
    def __init__(self, nombre, pin):
        self.nombre = nombre
        self.pin = pin
        self.valor_actual = 0

    def simular_lectura(self):
        # La guía didáctica pide usar condicionales según el tipo de sensor
        if self.nombre == "TMP36":
            self.valor_actual = random.randint(10, 35) # Simula grados Celsius
        else:
            self.valor_actual = random.randint(40, 90) # Simula % de humedad
        
        print(f"[{self.nombre}] Nueva lectura procesada en pin {self.pin}: {self.valor_actual}")
        return self.valor_actual

# Instanciación y prueba del sistema simulado para tu grupo
sensor_temperatura = Sensor("TMP36", "A0")

print("--- Ejecutando Simulación de la Estación (Grupo 4) ---")
for i in range(3):
    dato_falso = sensor_temperatura.simular_lectura()
    # Este dato simulado es el que tu puente enviará luego a la pantalla
    print(f"Dato listo para enviar a la pantalla LCD: {dato_falso}")
    time.sleep(2)