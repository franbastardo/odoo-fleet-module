import { Request, Response, NextFunction } from 'express';

export const apiKeyAuth = (req: Request, res: Response, next: NextFunction) => {
    const apiKey = req.headers['x-api-key'];
    if (!apiKey || apiKey !== process.env.ODOO_API_KEY) {
        return res.status(401).json({ message: 'Acceso no autorizado' });
    }
    next();
};