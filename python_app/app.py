import serial
import time
import mysql.connector
from mysql.connector import Error
from colorama import init, Fore, Back, Style


# Inicializamos colorama (autoreset=True limpia el color después de cada print)
init(autoreset=True)


class EstacionPlanB:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None
        self.db = None
        self.cursor = None


    def conectar_sistemas(self, db_host, db_user, db_pass, db_name, db_port):
        """Inicializa las conexiones físicas (Serial) y lógicas (MySQL)"""
        print(Fore.CYAN + Style.BRIGHT + "=" * 70)
        print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " 🚀 ESTACIÓN METEOROLÓGICA Y AMBIENTAL - ESCUELAS PRoA 🚀 ".center(70))
        print(Fore.CYAN + Style.BRIGHT + "=" * 70)
       
        # 1. Conexión Serial con el Arduino Uno físico
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=2)
            time.sleep(2)  # Pausa de cortesía para estabilizar el canal serial
            print(Fore.BLUE + Style.BRIGHT + f"🔌 [SERIAL] Conexión establecida con éxito en el puerto {self.port}")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"❌ [SERIAL] Error crítico: No se pudo abrir el puerto {self.port}. {e}")
            print(Fore.WHITE + "💡 Tip: Cerrá el Monitor Serie en el Arduino IDE antes de correr Python.")
            return False


        # 2. Conexión con el servidor MySQL Workbench
        try:
            self.db = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pass,
                database=db_name,
                autocommit=True  # 👈 Inserción inmediata sin bloqueo
            )
            self.cursor = self.db.cursor()
            print(Fore.CYAN + Style.BRIGHT + f"🗄️  [MySQL] Conectado exitosamente en el puerto {db_port} a la base de datos '{db_name}'.")
            return True
        except Error as e:
            print(Fore.RED + Style.BRIGHT + f"❌ [MySQL] Error de autenticación o conexión: {e}")
            print(Fore.WHITE + "💡 Tip: Verificá que la contraseña en la variable DB_PASS sea la correcta del Workbench.")
            return False


    def recibir_y_guardar(self):
        """Escucha el cable USB, procesa los datos y los inyecta en MySQL"""
        if not self.arduino or not self.db:
            return


        try:
            # Limpiamos el buffer para leer siempre el dato más reciente
            if self.arduino.in_waiting > 0:
                linea = self.arduino.readline().decode('utf-8', errors='ignore').strip()
            else:
                return
           
            # Filtro de seguridad: evita tramas vacías o mensajes de error de lectura
            if linea and "ERROR" not in linea:
                datos = linea.split(',')
               
                if len(datos) == 3:
                    humedad_act = int(float(datos[0]))
                    temperatura_act = int(float(datos[1]))
                    gas_act = int(float(datos[2]))
                   
                    # --- INTERFAZ VISUAL EN CONSOLA ---
                    print("\n" + Fore.BLUE + Style.BRIGHT + "┌" + "─" * 68 + "┐")
                    print(Fore.WHITE + Style.BRIGHT + f" │ 📊 MEDICIÓN EN VIVO ➔ 💧 Humedad: {humedad_act}% | 🌡️ Temp: {temperatura_act}°C | 💨 Gas/Aire: {gas_act} PPM ".ljust(68) + "│")
                    print(Fore.BLUE + Style.BRIGHT + "├" + "─" * 68 + "┤")


                    # EVALUACIÓN MEJORADA DE ALERTAS DE GAS Y CLIMA
                    if gas_act > 450:
                        print(Fore.WHITE + Back.RED + Style.BRIGHT + f" │ ☣️  [ALERTA CRÍTICA] Fuga de Gas / Concentración Alta ({gas_act} PPM) ".ljust(68) + "│")
                    elif gas_act >= 250:
                        print(Fore.BLACK + Back.YELLOW + Style.BRIGHT + f" │ ⚠️  [ALERTA MEDIA] Humo / Presencia de Vapores ({gas_act} PPM) ".ljust(68) + "│")
                    elif temperatura_act >= 35:
                        print(Fore.RED + Style.BRIGHT + f" │ 🔥 [ALERTA CLIMÁTICA] Ambiente con Calor Extremo ({temperatura_act}°C) ".ljust(68) + "│")
                    elif temperatura_act <= 15:
                        print(Fore.CYAN + Style.BRIGHT + f" │ ❄️ [ALERTA CLIMÁTICA] Ambiente con Frío Extremo ({temperatura_act}°C) ".ljust(68) + "│")
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f" │ 🟩 [ESTADO AMBIENTAL] Condiciones Saludables y Óptimas ".ljust(68) + "│")


                    print(Fore.BLUE + Style.BRIGHT + "└" + "─" * 68 + "┘")


                    # --- INYECCIÓN EN MYSQL WORKBENCH ---
                    # Nota: La columna 'fecha_hora' se autocompleta con CURRENT_TIMESTAMP en MySQL
                    sql = "INSERT INTO mediciones (temperatura, humedad, gas) VALUES (%s, %s, %s)"
                    valores = (temperatura_act, humedad_act, gas_act)
                   
                    self.cursor.execute(sql, valores)
                    print(Fore.CYAN + f"💾 [Base de Datos] Registro guardado a las {time.strftime('%H:%M:%S')}")


        except Exception as e:
            print(Fore.RED + f"⚠️ Error procesando la trama de datos: {e}")


    def cerrar_conexiones(self):
        """Finaliza el programa liberando los recursos de forma segura"""
        if self.cursor: self.cursor.close()
        if self.db: self.db.close()
        if self.arduino and self.arduino.is_open: self.arduino.close()
        print(Fore.WHITE + Back.BLUE + Style.BRIGHT + "\n🛑 Conexiones cerradas de forma segura. ¡Excelente trabajo Grupo Plan B! 🚀\n")




# --- EJECUCIÓN PRINCIPAL DE LA APLICACIÓN ---
if __name__ == "__main__":
   
    PUERTO_COM = 'COM4'
   
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASS = ''
    DB_NAME = 'estacionmetereologica_proa'


    mi_estacion = EstacionPlanB(port=PUERTO_COM)
   
    if mi_estacion.conectar_sistemas(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT):
        try:
            while True:
                mi_estacion.recibir_y_guardar()
                time.sleep(2)  # Muestreo cada 2 segundos
        except KeyboardInterrupt:
            mi_estacion.cerrar_conexiones()
