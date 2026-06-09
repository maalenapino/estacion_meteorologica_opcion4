#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Según tu PDF de Robótica, la pantalla usa el protocolo I2C.
// Se inicializa con la dirección típica 0x27 (o 0x3F según el modelo), de 16 columnas y 2 filas.
LiquidCrystal_I2C lcd(0x27, 16, 2); 

void setup() {
  // Abre el canal de comunicación serial a 9600 baudios para "escuchar" a Python
  Serial.begin(9600); 
  
  // Inicializa la pantalla y enciende la luz de fondo (VCC y GND en tu circuito)
  lcd.init();         
  lcd.backlight();    
  
  // Mensaje inicial de espera (mientras no lleguen datos de la Base de Datos)
  lcd.setCursor(0, 0);
  lcd.print("Estacion ProA");
  lcd.setCursor(0, 1);
  lcd.print("Esperando datos...");
}

void loop() {
  // Comprueba si Python envió un dato por el puerto serie
  if (Serial.available() > 0) {
    
    // Lee la cadena de texto que viaja por el cable USB hasta encontrar el salto de línea
    String datoTemperatura = Serial.readStringUntil('\n'); 
    
    // Limpia los mensajes anteriores para que no se superpongan las letras
    lcd.clear(); 
    
    // Renglón 1: Título fijo de la estación
    lcd.setCursor(0, 0);
    lcd.print("ESTACION METEO");
    
    // Renglón 2: Muestra la variable que vino desde MySQL a través de Python
    lcd.setCursor(0, 1);
    lcd.print("Temp: " + datoTemperatura + " C");
  }
}