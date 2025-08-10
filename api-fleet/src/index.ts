import express, { Application, Request, Response } from 'express';
import * as dotenv from 'dotenv';

// Importación de componentes de la arquitectura
import { ConsoleLogger } from './adapters/outbound/log/console.logger';
import { VehicleService } from './core/domain/vehicle.service';
import { VehicleController } from './adapters/inbound/http/vehicle.controller';
import { apiKeyAuth } from './adapters/inbound/http/middleware/auth.middleware';

// --- Configuración Inicial ---
dotenv.config(); // Carga las variables de .env

const app: Application = express();
const port = process.env.PORT || 3000;

app.use(express.json()); 

const logger = new ConsoleLogger();

const vehicleService = new VehicleService(logger);

const vehicleController = new VehicleController(vehicleService);

// --- Definición de Rutas ---
// La ruta usa el middleware de autenticación y luego llama al método del controlador
app.post('/api/vehicles', apiKeyAuth, (req: Request, res: Response) => 
    vehicleController.handlePostVehicles(req, res)
);

// Ruta de bienvenida para verificar que la API está funcionando
app.get('/', (req: Request, res: Response) => {
    res.send('API de Flota funcionando. Lista para recibir datos de Odoo en POST /api/vehicles');
});

// --- Arranque del Servidor ---
app.listen(port, () => {
    logger.log(`Servidor iniciado en http://localhost:${port}`);
});