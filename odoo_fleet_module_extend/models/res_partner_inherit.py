# models/res_partner_inherit.py
import requests
import json
from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many(
        'fleet.vehicle',
        'driver_id',
        string='Vehículos Asociados'
    )

    vehicle_count = fields.Integer(
        string='Cantidad de Vehículos',
        compute='_compute_vehicle_count',
        store=True,
        help="Cantidad de vehículos asociados a este contacto."
    )

    @api.depends('vehicle_ids')
    def _compute_vehicle_count(self):
        for partner in self:
            partner.vehicle_count = len(partner.vehicle_ids)
            
    def action_view_vehicles(self):
        """Acción para el smart button: muestra los vehículos de este contacto."""
        self.ensure_one()
        # Reutilizamos la acción de vehículos de flota, pero con un dominio específico
        action = self.env['ir.actions.act_window']._for_xml_id('fleet.fleet_vehicle_action')
        action['domain'] = [('driver_id', '=', self.id)]
        action['context'] = {'default_driver_id': self.id}
        return action

    def action_send_vehicles_to_api(self):
        """Acción para el botón de envío a la API."""
        self.ensure_one()
        if not self.vehicle_ids:
            raise UserError("Este conductor no tiene vehículos asociados para enviar.")
        
        config_params = self.env['ir.config_parameter'].sudo().search([])

        api_url = config_params.get_param('custom_fleet.api_endpoint')
        api_key = config_params.get_param('custom_fleet.api_key')
        
        if not api_url or not api_key:
            raise UserError("La configuración de la API no está completa. "
                            "Por favor, vaya a Ajustes > Técnico > Parámetros del Sistema "
                            "y configure 'custom_fleet.api_endpoint' y 'custom_fleet.api_key'.")


        payload = []
        for vehicle in self.vehicle_ids:
            payload.append({
                'license_plate': vehicle.license_plate,
                'make': vehicle.model_id.brand_id.name, # Campo relacionado
                'model': vehicle.model_id.name,       # Campo relacionado
                'year': vehicle.model_year,
                'vin_sn': vehicle.vin_sn,
                'driver_name': self.name,
            })
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key 
        }
        log_vals = {
            'response_date': fields.Datetime.now(),
        }

        try:
            response = requests.post(api_url, data=json.dumps({"data": payload}), headers=headers, timeout=10)
            log_vals['status'] = str(response.status_code)
            log_vals['response_text'] = response.text
        except requests.exceptions.RequestException as e:
            log_vals['status'] = 'Error de Conexión'
            log_vals['response_text'] = str(e)
        
        self.env['api.log'].create(log_vals)
        
        return {
           'type': 'ir.actions.client',
           'tag': 'display_notification',
           'params': {
               'title': 'Envío a API',
               'message': 'Proceso de envío finalizado. Revise los logs para más detalles.',
               'sticky': False,
           }
        }