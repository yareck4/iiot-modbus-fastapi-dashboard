# iiot-modbus-fastapi-dashboard
FULL-STACK IIOT SYSTEM: A robust Python backend that maps industrial Modbus TCP registers, exposing them through a high-performance API Gateway with FastAPI for real-time analytical visualization on an interactive web dashboard.

# 🏭 Industrial IIoT Gateway & Real-Time Monitoring Dashboard

This project implements a **Full-Stack Industry 4.0** architecture that bridges low-level industrial hardware/automation environments with modern, high-performance web applications. The system simulates data acquisition of analog variables from a production line using the **Modbus TCP** protocol, processes the information through an **API Gateway built with FastAPI**, and dynamically deploys it onto a **Real-Time Web Dashboard** featuring logical alert triggers for motor overheating conditions.

---

## 🛠️ System Architecture

The ecosystem is fragmented into three decoupled layers to guarantee high availability and mitigate latency across distributed data transmission:

1. **Plant Simulator (Low-Level / Edge):** A Python script that spins up a local Modbus TCP server. It generates dynamic, randomized telemetry to emulate physical motor temperature sensors and production cycle counters stored within the *Holding Registers*.
2. **API Gateway (Ingestion Layer / Backend):** Developed using FastAPI and PyModbus. It acts as the Modbus Master/Client that periodically polls the server's registers, decodes raw byte arrays into structured data, and injects business logic constraints before exposing a public JSON endpoint secured with CORS policies.
3. **Supervision Dashboard (Control Front / Frontend):** An operator interface constructed with HTML5, classic CSS3 (for offline industrial environments), and native JavaScript. It asynchronously consumes the API using a continuous *Polling* loop to populate trending line charts via **Chart.js**.

---

## 📂 Repository Structure

```text
├── .venv/                   # Isolated Python Virtual Environment
├── plant monitoring.py    # Modbus TCP Server (Machinery Simulator)
├── client_api.py           # FastAPI API Gateway (Modbus Client)
├── index.html               # Frontend Dashboard (Operator UI)
└── README.md                # Technical System Documentation
```

---

## 🚀 Deployment & Installation Guide

### 1. Clone the repository and configure the environment
```bash
git clone https://github.com
cd iiot-modbus-fastapi-dashboard
```

### 2. Install dependencies fixing stable versions
To prevent backward compatibility failures due to breaking architectural changes in the latest library versions, we force the installation of the classic stable branch:
```bash
# Ensure you execute this pointing to your local virtual environment's pip
.\.venv\Scripts\pip install --force-reinstall pymodbus==2.5.3
.\.venv\Scripts\pip install fastapi uvicorn
```

### 3. Running the System (Requires independent terminal windows)

*   **Terminal 1 (Production Line Edge):** Fires up the Modbus TCP telemetry stream on local port `5020`.
    ```bash
    python "monitoreo de planta.py"
    ```
*   **Terminal 2 (Web Server Gateway):** Launches the Uvicorn asynchronous HTTP engine on port `8000`.
    ```bash
    python "cliente_api.py"
    ```

### 4. System Access Points
*   **Raw JSON Endpoint:** [http://127.0.0](http://127.0.0)
*   **Interactive Swagger Documentation:** [http://127.0.0](http://127.0.0)
*   **Dashboard UI Visualization:** Double-click the `index.html` file to launch it directly in your preferred web browser.

---

## 🧠 Engineering Log: Lessons Learned & Troubleshooting

During the development and deployment lifecycle of this full-stack solution, several infrastructure and environment bottlenecks were encountered and solved. This section documents the diagnostic process and resolutions applied, providing mid-to-senior level engineering insights to the codebase:

### Phase 1: Isolated Virtual Environments & IDE Indexing Conflicts
*   **Symptom:** After executing a generic `pip install`, Visual Studio Code (Pylance) kept flags raised, marking `pymodbus` imports as unresolved (`ImportError`).
*   **Diagnosis:** The IDE automatically initialized an isolated virtual environment (`.venv`). The standard install command injected packages into the global operating system core, leaving the specific project directory completely devoid of the library.
*   **Resolution:** Package installation was forced by explicitly targeting the binary executable inside the local project folders using `.\.venv\Scripts\pip install`.

### Phase 2: PowerShell Execution Terminal Blocked by Cloud Directory Paths
*   **Symptom:** PowerShell interrupted execution, throwing a critical syntax error: *"The ampersand (&) character is not allowed..."*.
*   **Diagnosis:** The project was nested inside a synchronized institutional cloud directory (`OneDrive - Laureate Mexico`). PowerShell reserves the `&` symbol as a logical execution operator for scripts. Reading this symbol in the middle of a string path caused the terminal parser to collapse.
*   **Resolution:** The active terminal instance in VS Code was switched to a classic **Command Prompt (CMD)** interpreter, which handles string paths containing special characters encapsulated within double quotes smoothly without breaking the Python execution thread.

### Phase 3: Modbus Library Version Breaking Changes
*   **Symptom:** The data block constructor raised numeric value faults (`TypeError: 0 <= address < 65535`) or class inheritance drops when invoking `ModbusSlaveContext`.
*   **Diagnosis:** Modern `pymodbus v3.x` releases restructured the internal codebase, removing module layers entirely and modifying how configuration dictionaries are processed by server and datastore classes.
*   **Resolution:** Rather than patching unstable shifting code, a standard software engineering principle was applied: **environment lock-in**. A controlled downgrade to `pymodbus==2.5.3` was executed, securing seamless backward compatibility with sessional Modbus data acquisition logic.

### Phase 4: Browser Cibersecurity Policies & CORS Cross-Origin Restrictions
*   **Symptom:** When attempting to hook the Frontend to the Backend via relative routes (`'/api/telemetria'`), data fields remained empty (`--`). Web browser inspector tools reported network connection timeouts and unresolved object references.
*   **Diagnosis:** Opening the HTML file via double-click defaults the browser to the secure local `file:///` protocol. Under strict Same-Origin Policies, browsers block relative JavaScript asynchronous calls from local storage to network HTTP servers. Additionally, local network firewalls blocked requests to the script CDN (`jsdelivr.net`), preventing the `Chart` class from being defined and freezing script execution before the `fetch` could happen.
*   **Resolution:** **CORS Middleware** was enabled on the FastAPI core instance to authorize cross-origin requests. On the frontend, the blocked CDN URL was replaced with a Universal Module Definition (**umd**) bundle, and the asynchronous `fetch` was pointed strictly to the absolute local network address (`http://127.0.0`), fixing cross-protocol communications.

---
The final architecture operates under **Industrial Cybersecurity & Air-Gapped Network** standards, ensuring that the tracking system functions completely **offline** without depending on an internet connection on the plant floor.
