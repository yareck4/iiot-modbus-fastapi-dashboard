from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import HTMLResponse
from pymodbus.client.sync import ModbusTcpClient
import uvicorn
import os

# 1. Inicializamos la aplicación FastAPI
app = FastAPI(
    title="IIoT Industrial Gateway API",
    description="API para conectar sistemas web con redes Modbus TCP de planta",
    version="1.0.0"
)

# 👈 CONFIGURACIÓN DE CORS: Permite que cualquier página web consulte tu API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def leer_dashboard():
    """Sirve el archivo index.html directamente en la raíz del servidor web"""
    ruta_html = os.path.join(os.path.dirname(__file__), "index.html")
    with open(ruta_html, "r", encoding="utf-8") as archivo:
        return archivo.read()

# 2. Configuramos el cliente Modbus apuntando al servidor local (puerto 5020)
MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 5020

@app.get("/api/telemetria")
def obtener_telemetria_planta():
    """
    Endpoint que realiza la adquisición de datos en tiempo real 
    desde el servidor Modbus de la planta.
    """
    # Conectamos con el PLC / Servidor
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    conexion = client.connect()
    
    if not conexion:
        return {"status": "error", "message": "No se pudo conectar con la planta industrial"}
    
    try:
        # Leemos los Holding Registers 
        # Empezamos en la casilla 0 y leemos 2 registros consecutivos
        resultado = client.read_holding_registers(0, 2)
        
        if resultado.isError():
            return {"status": "error", "message": "Error al leer los registros Modbus"}
        
        # Extraemos los valores del arreglo de bytes
        registros = resultado.registers # Devuelve una lista tipo 
        temperatura = registros[0]
        total_piezas = registros[1]
        
        # Retornamos los datos estructurados en formato JSON para el frontend
        return {
            "status": "success",
            "data": {
                "motor_temperatura_celsius": temperatura,
                "produccion_total_piezas": total_piezas,
                "estado_sistema": "OPERANDO_NORMAL" if temperatura < 80 else "ALERTA_SOBRECALENTAMIENTO"
            }
        }
        
    finally:
        # Cerramos siempre la conexión de red
        client.close()

if __name__ == "__main__":
    # Arrancamos el servidor web Uvicorn en el puerto 8000
    print("🚀 API Gateway levantada en http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
