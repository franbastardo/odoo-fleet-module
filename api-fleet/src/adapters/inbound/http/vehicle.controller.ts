import { Request, Response } from 'express';
import { IVehicleService } from '../../../core/ports/IVehicleService';

export class VehicleController {
    constructor(private vehicleService: IVehicleService) {}

    async handlePostVehicles(req: Request, res: Response): Promise<void> {
        try {
            const vehicles = req.body.data;

            // Validación básica de entrada
            if (!Array.isArray(vehicles) || vehicles.length === 0) {
                res.status(204).json({ message: 'No se recibieron vehiculos para procesar.' });
                return;
            }

            const result = await this.vehicleService.processVehicles(vehicles);
            
            res.status(200).json(result);

        } catch (error) {
            const e = error as Error;
            res.status(500).json({ message: 'Error interno del servidor', error: e.message });
        }
    }
}