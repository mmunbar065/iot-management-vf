document.addEventListener("DOMContentLoaded", function () {
    loadDevices();
});

document.addEventListener("DOMContentLoaded", function () {
    loadDevices();
});

function loadDevices() {
    const sortBy = document.getElementById("sortSelect").value;
    const order = document.getElementById("orderSelect").value; // Obtener orden (ASC/DESC)

    fetch(`api/devices?sort_by=${sortBy}&order=${order}`) // Ruta y parámetros correctos
        .then(response => response.json())
        .then(data => {
            const devices = data.Devices;
            const gridContainer = document.getElementById("grid-container");
            gridContainer.innerHTML = "";

            devices.forEach(device => {
                const newItem = document.createElement("div");
                newItem.classList.add("col-md-3", "mb-3");

                const iconName = getIconName(device.type);

                // Determinar qué valor mostrar según el tipo de dispositivo
                let extraInfo = "";
                if (device.type === "Sensor de temperatura" && device.temperature !== null) {
                    extraInfo = `<p class="card-text"><strong>Temperatura:</strong> ${device.temperature}°C</p>`;
                } else if (device.type === "Sensor de presión" && device.pressure !== null) {
                    extraInfo = `<p class="card-text"><strong>Presión:</strong> ${device.pressure} hPa</p>`;
                }

                newItem.innerHTML = `
      <div class="card text-bg-light mb-3" style="max-width: 18rem;">
          <img src="images/${iconName}.png" class="card-img-top" onerror="this.onerror=null; this.src='images/default-icon.png';">
          <div class="card-body">
                <h6 class="card-title">${device.name}</h5>
              <p class="card-text"><strong>Tipo:</strong> ${device.type}</p>
              <p class="card-text"><strong>Estado:</strong> ${device.status}</p>
              <p class="card-text"><strong>Temperatura:</strong> ${device.temperature}°C</p>
              <p class="card-text"><strong>Batería:</strong> ${device.battery_level}%</p>
                <p class="card-text"><strong>Presión:</strong> ${device.pressure} hPa</p>
                <p class="card-text"><strong>Humedad:</strong> ${device.humidity}%</p>
            <p class="card-text"><strong>Last update:</strong> ${device.last_update}%</p>
              <button class="btn ${device.status === 'on' ? 'btn-secondary' : 'btn-success'}" 
                      onclick="toggleDevice(${device.id}, '${device.status}')">
                  ${device.status === 'on' ? 'Apagar' : 'Encender'}
              </button>
              <button class="btn btn-danger" onclick="deleteDevice(${device.id})">Eliminar</button>
          </div>
      </div>
                `;
                gridContainer.appendChild(newItem);
            });
        })
        .catch(error => console.error("Error al cargar dispositivos:", error));
}


// Función para obtener el nombre del icono según el tipo de dispositivo
function getIconName(deviceType) {
    switch (deviceType.toLowerCase()) {
        case 'iluminación':
            return 'Luz'; // Reemplaza con el nombre real del icono
        case 'sensor temperatura':
            return 'sensor_temperatura'; // Reemplaza con el nombre real del icono
        case 'sensor de presión':
            return 'sensor_presion'; // Reemplaza con el nombre real del icono
        case 'sensor de movimiento':
            return 'motion_sensor'; // Reemplaza con el nombre real del icono
        default:
            return 'default-icon'; // Icono por defecto si no coincide
    }
}


// Función para eliminar un dispositivo
function deleteDevice(id) {
    if (!confirm("¿Seguro que deseas eliminar este dispositivo?")) return;

    fetch(`api/delete_device/${id}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            console.log("Dispositivo eliminado:", data);
            loadDevices(); // Recargar la lista de dispositivos después de eliminar
        })
        .catch(error => console.error("Error al eliminar el dispositivo:", error));
}
// Función para cambiar el estado de un dispositivo
function toggleDevice(id, currentStatus) {
    const newStatus = currentStatus === "on" ? "off" : "on";

    fetch(`api/update_device/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: newStatus })
    })
        .then(response => response.json())
        .then(data => {
            console.log(`Dispositivo ${id} actualizado:`, data);
            loadDevices(); // Recargar la lista de dispositivos después de cambiar el estado
        })
        .catch(error => console.error("Error al cambiar el estado del dispositivo:", error));
}
