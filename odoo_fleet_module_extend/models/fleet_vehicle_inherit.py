# models/fleet_vehicle_inherit.py
from odoo import models, fields, api

class FleetVehicle(models.Model):
    """
    Hereda de fleet.vehicle para añadir un campo de imagen específico
    para cada vehículo, en lugar de usar solo la imagen del modelo/marca.
    """
    _inherit = 'fleet.vehicle'

    vehicle_image = fields.Image(string="Foto del Vehículo", required=True)
    
    code_sequence = fields.Char(string='Referencia del Vehículo', required=True, copy=False, readonly=True, index=True, default='New')
    
    # Sobreescribir campos que son requeridos en fleet.vehicle
    license_plate = fields.Char(required=True, index=True)
    
    vin_sn = fields.Char(string='VIN/SN', required=True, index=True)
    
    model_year = fields.Integer(string='Año del Modelo', required=True)
    
    Color = fields.Char(string='Color', required=True)
    
    category_id = fields.Many2one('fleet.vehicle.model.category', 'Category', compute='_compute_model_fields', store=True, readonly=False, required=True)
    
    
    driver_id = fields.Many2one(
        'res.partner', 
        string='Conductor', 
        required=True
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Asignar una secuencia única a cada vehículo.
        """
        for vals in vals_list:
            if vals.get('code_sequence', 'New') == 'New':
                sequence = self.env['ir.sequence'].next_by_code('fleet.vehicle.sequence')
                vals['code_sequence'] = sequence or 'New'
        records = super(FleetVehicle, self).create(vals_list)
        return records