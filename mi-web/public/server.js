require("dotenv").config();
const express = require("express");
const mysql = require("mysql");
const cors = require("cors");
const corsOptions ={
  origin:'*', 
  credentials:true,            //access-control-allow-credentials:true
  optionSuccessStatus:200,
}

const app = express();
app.use(cors(corsOptions));
app.use(express.json()); // Para manejar JSON en las solicitudes

// Configurar la conexión a MySQL
const db = mysql.createConnection({
  host: "localhost",
  user: "root", // Cambia esto si tienes otro usuario
  password: "", // Agrega tu contraseña si es necesaria
  database: "iot_management"
});


// Conectar a la base de datos
db.connect((err) => {
  if (err) {
    console.error("Error al conectar a la BD:", err);
  } else {
    console.log("Conectado a la base de datos MySQL.");
  }
});

// **Ruta para obtener dispositivos**
app.get("/devices", (req, res) => {
  db.query("SELECT * FROM devices", (err, results) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(results);
    }
  });
});


// **Ruta para añadir un nuevo dispositivo**
app.post("/devices", (req, res) => {
  console.log("Datos recibidos en /devices:", req.body);

  const { name, type, status } = req.body;

  console.log("Datos capturados:");
  console.log("Nombre:", name); 
  console.log("Tipo:", type);
  console.log("Estado:", status);

  db.query(
    "INSERT INTO devices (name, type, status) VALUES (?, ?, ?)",
    [name, type, status],
    (err, result) => {
      if (err) {
        res.status(500).json({ error: err.message });
      } else {
        res.json({ message: "Dispositivo agregado con éxito", id: result.insertId });
      }
    }
  );
});

// Iniciar servidor en el puerto 3000
app.listen(3000, () => {
  console.log("Servidor corriendo en http://localhost:3000");
});
