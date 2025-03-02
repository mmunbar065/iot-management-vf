# -----------------------------------------------
# SCRIPT PARA INICIAR LA APLICACIÓN IoT MANAGEMENT
# -----------------------------------------------

# Configuración
$mysqlPort = 3306
$mysqlPassword = "" # Considera usar variables de entorno
$mysqlPath = "C:\xampp\mysql\bin\mysql.exe" # Considera usar rutas relativas o variables de entorno
$database = "iot_management"
$apiPath = "C:\Users\marmu\OneDrive\Documentos\TFG\API_REST\app" # Ruta absoluta a la carpeta api
$webPath = "C:\Users\marmu\OneDrive\Documentos\TFG\mi-web\public" # Ruta absoluta a la carpeta web

# Iniciar el servidor Flask
Write-Host "Iniciando el servidor Flask..."
try {
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "$apiPath\app.py"
    Write-Host "Servidor Flask en ejecución."
}
catch {
    Write-Error "Error al iniciar el servidor Flask: $($_.Exception.Message)"
    exit 1
}

## Matar procesos en puerto 3000 (Windows)
Write-Host "Matando procesos en puerto 3000..."
try {
    $portNumber = "3000"
    $portPattern = ":${portNumber}" # Delimitar el patrón
    $portCheck = netstat -ano | Select-String -Pattern $portPattern
    if ($portCheck) {
        Write-Host "Puerto 3000 ya está en uso. Matando procesos..."
        $processIDs = $portCheck | ForEach-Object {
            $_.Line.Split(" ")[-1]
        } | Where-Object { $_ -match "^\d+$" } # Filter out non-numeric PIDs

        foreach ($processID in $processIDs) {
            if ($null -ne $processID) {
                try {
                    taskkill /PID $processID /F | Out-Null
                    Write-Host "Proceso con PID $processID finalizado."
                }
                catch {
                    Write-Warning "Error al finalizar el proceso con PID ${processID}: $($_.Exception.Message)"
                }
            }
        }
    }
    else {
        Write-Host "No se encontraron procesos en el puerto 3000."
    }
}
catch {
    Write-Warning "Error al verificar procesos en el puerto 3000: $($_.Exception.Message)"
}

# Instalar dependencias del proxy
Write-Host "Instalando dependencias del proxy..."
Set-Location proxy
npm install
Set-Location ..

# Iniciar el servidor proxy
Write-Host "Iniciando el servidor proxy..."
Start-Process -NoNewWindow -FilePath "node" -ArgumentList "proxy\server-proxy.js"
Write-Host "Servidor proxy en ejecución en http://localhost:3000"


# Función para verificar y iniciar MySQL
function Test-MySQL {
    if (-not (Get-Process | Where-Object { $_.ProcessName -like "*mysqld*" })) {
        Write-Host "MySQL no está corriendo. Iniciando desde XAMPP..."
        Start-Process -FilePath "C:\xampp\xampp-control.exe"
        Pause
        exit
    }

    try {
        & $mysqlPath -u root --password=$mysqlPassword -h 127.0.0.1 -P $mysqlPort -e "SHOW DATABASES;" | Out-Null
        Write-Host "Conexión a MySQL exitosa."
    }
    catch {
        Write-Error "Error al conectar con MySQL: $($_.Exception.Message)"
        Pause
        exit
    }
}

# Función para crear la base de datos
function Test-Database {
    $createDBScript = @"
CREATE DATABASE IF NOT EXISTS $database;
USE $database;
CREATE TABLE IF NOT EXISTS devices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(255) NOT NULL,
        status ENUM('on', 'off') NOT NULL DEFAULT 'off'
        battery_level TINYINT UNSIGNED DEFAULT NULL
        temperature DECIMAL(5, 2) DEFAULT NULL
        humidity DECIMAL(5, 2) DEFAULT NULL
        pressure DECIMAL(5, 2) DEFAULT NULL
        last_motion TIMESTAMP NULL DEFAULT NULL
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"@

    try {
        $createDBScript | & $mysqlPath -h localhost -u root --password=$mysqlPassword | Out-Null
        Write-Host "Base de datos y tabla listas."
    }
    catch {
        Write-Error "Error al crear la base de datos: $($_.Exception.Message)"
        Pause
        exit
    }
}

# Verifica si pip está instalado
if (-Not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "pip no está instalado. Asegúrate de tener Python instalado y agregado al PATH." -ForegroundColor Red
    exit
}

# Función para verificar si un paquete de Python está instalado
function Test-PythonPackage {
    param (
        [string]$PackageName
    )

    try {
        pip show $PackageName | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Instalar dependencias de Python
Write-Host "Instalando dependencias de Python..."
try {
    pip install -r "$apiPath\requirements.txt"
    Write-Host "Dependencias de Python instaladas."
}
catch {
    Write-Error "Error al instalar dependencias de Python: $($_.Exception.Message)"
    exit 1
}

# Verificar e instalar Flask y Flask-CORS
if (-not (Test-PythonPackage flask)) {
    Write-Host "Instalando Flask..."
    pip install flask
}
else {
    Write-Host "Flask ya está instalado."
}

if (-not (Test-PythonPackage flask-cors)) {
    Write-Host "Instalando Flask-CORS..."
    pip install flask-cors
}
else {
    Write-Host "Flask-CORS ya está instalado."
}

Write-Host "Verificación e instalación de Python completadas." -ForegroundColor Green

# Inicio del script
Write-Host "Iniciando la aplicación IoT Management..."

Test-MySQL
Test-Database



Write-Host "Abriendo la interfaz en el navegador..."
Start-Process "http://localhost:3000"

Write-Host "¡Todo listo! Prueba agregar dispositivos desde add-device.html"