// Ejecuta este archivo con Node.js para iniciar el servidor proxy
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Configura el proxy
app.use(
  '/api', // Prefijo de la ruta que quieres proxy
  createProxyMiddleware({
    target: 'http://127.0.0.1:5000', // URL de tu API Flask
    changeOrigin: true, // Necesario para CORS
    pathRewrite: { '^/api': '' }, // Opcional: Elimina '/api' del path
    timeout : 60000,
  })
);

app.use(express.static('C:/Users/marmu/OneDrive/Documentos/TFG/mi-web/public'));

// Inicia el servidor
const port = 3000; // Puedes cambiar el puerto
app.listen(port, () => {
  console.log(`Servidor proxy en ejecución en http://localhost:${port}`);
});