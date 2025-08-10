import { ILogger } from "../ports/ILogger";
import { IVehicleService } from "../ports/IVehicleService";
import { Vehicle } from "../entities/vehicle.entity";

export class VehicleService implements IVehicleService {
    constructor(private readonly logger: ILogger) {}

    async processVehicles(vehicles: Vehicle[]): Promise<{ status: string; message: string; receivedCount: number }> {
        this.logger.log(`Procesando lote de ${vehicles.length} vehículos.`);

        for (const vehicle of vehicles) {
            this.logger.log('Vehículo recibido:', vehicle);
        }

        const response = {
            status: 'success',
            message: 'Datos de vehículos recibidos y procesados correctamente.',
            receivedCount: vehicles.length
        };
        
        return response;
    }
}