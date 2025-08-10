import { Vehicle } from "../entities/vehicle.entity";

export interface IVehicleService {
    processVehicles(vehicles: Vehicle[]): Promise<{ status: string; message: string; receivedCount: number }>;
}