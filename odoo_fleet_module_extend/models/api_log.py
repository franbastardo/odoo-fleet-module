from odoo import models, fields

class ApiLog(models.Model):
    _name = 'api.log'
    _description = 'Log de Respuestas de API'
    _order = 'response_date desc'

    response_date = fields.Datetime(string='Fecha de Respuesta', readonly=True)
    status = fields.Char(string='Estado', readonly=True)
    response_text = fields.Text(string='Texto de la Respuesta', readonly=True)