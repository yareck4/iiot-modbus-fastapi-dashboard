# 🏭 Pasarela IIoT Industrial y Panel de Monitoreo en Tiempo Real

Este proyecto implementa una arquitectura **Full-Stack para la Industria 4.0** que conecta entornos de hardware industrial y automatización de bajo nivel con aplicaciones web modernas de alto rendimiento. El sistema simula la adquisición de datos de variables analógicas provenientes de una línea de producción mediante el protocolo **Modbus TCP**; procesa dicha información a través de una **API Gateway desarrollada con FastAPI** y la presenta dinámicamente en un **panel web en tiempo real**, el cual incluye alertas lógicas ante situaciones de sobrecalentamiento de motores.

---

## 🛠️ Arquitectura del Sistema

El ecosistema se divide en tres capas desacopladas para garantizar una alta disponibilidad y mitigar la latencia en la transmisión de datos distribuidos:

1. **Simulador de Planta (Nivel inferior / Edge):** Un script en Python que ejecuta un servidor Modbus TCP local. Este genera telemetría dinámica y aleatoria para emular sensores físicos de temperatura en motores, así como contadores de ciclos de producción almacenados en los *registros de retención* (*Holding Registers*).
2. **API Gateway (Capa de ingesta / Backend):** Desarrollada utilizando FastAPI y PyModbus. Actúa como un cliente Modbus (*Modbus Master/Client*) que consulta periódicamente los registros del servidor, decodifica los flujos de bytes en datos estructurados y aplica reglas de lógica de negocio antes de exponer un *endpoint* JSON público, protegido mediante políticas CORS.
3. **Panel de Supervisión (Interfaz de control / Frontend):** Una interfaz para el operador construida con HTML5, CSS3 clásico (adecuado para entornos industriales sin conexión a internet) y JavaScript nativo. Esta consume la API de forma asíncrona mediante un bucle de consulta continua (*polling*), alimentando gráficos de tendencias mediante la librería **Chart.js**. ---

## 📂 Estructura del repositorio

```text
├── .venv/                   # Entorno virtual de Python aislado
├── plant monitoring.py    # Servidor Modbus TCP (simulador de maquinaria)
├── client_api.py           # API Gateway con FastAPI (cliente Modbus)
├── index.html               # Panel de control (interfaz de usuario para el operador)
└── README.md                # Documentación técnica del sistema
---

## 🚀 Guía de despliegue e instalación

### 1. Clonar el repositorio y configurar el entorno
```bash
git clone https://github.com
cd iiot-modbus-fastapi-dashboard
```

### 2. Instalar dependencias (versiones estables)
Para evitar problemas de compatibilidad causados ​​por cambios estructurales en versiones más recientes de las librerías, instalamos versiones estables específicas:
```bash
# Asegúrate de ejecutar esto utilizando el 'pip' de tu entorno virtual local
.\.venv\Scripts\pip install --force-reinstall pymodbus==2.5.3
.\.venv\Scripts\pip install fastapi uvicorn
```

### 3. Ejecución del sistema (requiere ventanas de terminal independientes)

*   **Terminal 1 (Simulación de planta):** Inicia el flujo de telemetría Modbus TCP en el puerto local `5020`. 
```bash
python "monitoreo de planta.py"
```
*   **Terminal 2 (Servidor web/API Gateway):** Inicia el servidor asíncrono Uvicorn en el puerto `8000`. 
```bash
python "cliente_api.py"
```

### 4. Puntos de acceso al sistema
*   **Endpoint JSON (datos brutos):** [http://127.0.0](http://127.0.0)
*   **Documentación interactiva (Swagger):** [http://127.0.0](http://127.0.0)
*   **Interfaz visual (Dashboard):** Haz doble clic en el archivo `index.html` para abrirlo directamente en tu navegador web preferido. ---

## 🧠 Registro de ingeniería: Lecciones aprendidas y resolución de problemas

Durante el ciclo de vida de desarrollo e implementación de esta solución *full-stack*, surgieron diversos cuellos de botella relacionados con la infraestructura y el entorno, los cuales fueron resueltos. Esta sección documenta el proceso de diagnóstico y las soluciones aplicadas, ofreciendo perspectivas técnicas —orientadas a perfiles de ingeniería de nivel intermedio a avanzado— sobre el código base:

### Fase 1: Entornos virtuales aislados y conflictos de indexación en el IDE
*   **Síntoma:** Tras ejecutar un comando `pip install` genérico, Visual Studio Code (a través de Pylance) mostraba advertencias, señalando las importaciones de `pymodbus` como no resueltas (`ImportError`).
*   **Diagnóstico:** El IDE inicializó automáticamente un entorno virtual aislado (`.venv`). El comando de instalación estándar instaló los paquetes en el entorno global del sistema operativo, dejando el directorio específico del proyecto sin la librería requerida.
*   **Resolución:** Se forzó la instalación del paquete apuntando explícitamente al ejecutable binario ubicado dentro de las carpetas locales del proyecto, mediante el comando `.\.venv\Scripts\pip install`.

### Fase 2: Bloqueo de la terminal de PowerShell debido a rutas en directorios en la nube
*   **Síntoma:** PowerShell interrumpía la ejecución, arrojando un error de sintaxis crítico: *"The ampersand (&) character is not allowed..."* (El carácter ampersand «&» no está permitido...).
*   **Diagnóstico:** El proyecto se encontraba alojado dentro de un directorio sincronizado en la nube (específicamente, `OneDrive - Laureate Mexico`). PowerShell reserva el símbolo `&` como un operador lógico de ejecución para scripts; al encontrar este símbolo en medio de una ruta de archivo, el analizador (*parser*) de la terminal fallaba.
*   **Resolución:** Se cambió la instancia de terminal activa en VS Code al intérprete clásico **Command Prompt (CMD)**, el cual gestiona correctamente las rutas que contienen caracteres especiales siempre que estas se encuentren encerradas entre comillas dobles.