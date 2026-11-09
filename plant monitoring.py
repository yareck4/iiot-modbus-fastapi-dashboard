import time
import random
from threading import Thread
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Creamos los bloques de datos para Holding Registers 
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*10))
context = ModbusServerContext(slaves=store, single=True)

def actualizar_datos_maquina():
    print("🤖 Simulación de planta iniciada. Generando telemetría...")
    while True:
        # Registro 0: Temperatura de un motor
        temperatura = random.randint(60, 85)
        store.setValues(3, 0, [temperatura]) 
        
        # Registro 1: Conteo de piezas producidas
        piezas_actuales = store.getValues(3, 1, 1)
        nuevas_piezas = piezas_actuales[0] + random.randint(1, 3)   
        store.setValues(3, 1, [nuevas_piezas])
        
        print(f"📊 [TELEMETRÍA] Motor Temp: {temperatura}°C | Total Piezas: {nuevas_piezas}")

        time.sleep(2)

# Lanzamos la simulación en un hilo secundario
hilo_planta = Thread(target=actualizar_datos_maquina, daemon=True)
hilo_planta.start()

# Arrancamos el servidor Modbus TCP limpio
print("🏭 Servidor Modbus TCP listo en 127.0.0.1:5020...")
StartTcpServer(context=context, address=("127.0.0.1", 5020))
