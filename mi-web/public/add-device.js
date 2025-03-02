document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-device-form");
    const mensaje = document.getElementById("mensaje");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const name = document.getElementById("device-name").value;
        const type = document.getElementById("device-type").value;
        const status = document.getElementById("device-status").value;
        // Generar un nivel de batería aleatorio entre 0 y 100
        const battery_level = Math.floor(Math.random() * 101);

        fetch("/api/add_device", {  // Verifica que Flask corre en este puerto
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, type, status, battery_level })  // ID no es necesario porque es autoincrement
        })
            .then(response => response.json())
            .then(data => {
                console.log("Respuesta del servidor:", data);
                mensaje.innerHTML = "Dispositivo agregado con éxito";
                mensaje.style.color = "green";
                form.reset();
                setTimeout(() => mensaje.innerHTML = "", 3000);
            })
            .catch(error => {
                console.error("Error:", error);
                mensaje.innerHTML = "Error al agregar el dispositivo";
                mensaje.style.color = "red";
            });
    });
});
