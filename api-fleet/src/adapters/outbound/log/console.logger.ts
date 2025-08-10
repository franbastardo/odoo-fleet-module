import { ILogger } from "../../../core/ports/ILogger";

export class ConsoleLogger implements ILogger {
    log(message: string, data?: any): void {
        console.log(`[INFO] ${message}`, data || '');
    }

    error(message: string, error?: any): void {
        console.error(`[ERROR] ${message}`, error || '');
    }
}