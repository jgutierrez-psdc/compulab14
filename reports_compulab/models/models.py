# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    time_shiping = fields.Many2one(
        'report.compulab',
        string="Tiempo de entrega"
    )
    tecnico = fields.Many2one(
        'res.users',
        string="Asistente",
        domain="[('x_studio_asistente','=',True)]"
    )
    asesor1 = fields.Many2one(
        'res.users',
        string="Asesor 1",
        domain="[('x_studio_asesor','=',True)]"
    )
    asesor2 = fields.Many2one(
        'res.users',
        string="Asesor 2",
        domain="[('x_studio_asesor','=',True)]"
    )
    create_uid = fields.Many2one(
        'res.users',
        readonly=False
    )

class ReportCompulab(models.Model):
    _name = 'report.compulab'

    name = fields.Char(
        string="Nombre",
        required=True
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_uom_qty = fields.Float(string='Cantidad', digits=(12,0), required=True, default=1.0)
    qty_invoiced = fields.Float(
        compute='_get_invoice_qty', string='Facturado', store=True, readonly=True,
        digits=(12,0))

class Account(models.Model):
    _inherit = 'account.move'

    sale_id = fields.Many2one('sale.order', 
        compute='_compute_sale_order', 
        string='Sale Order'
    )

    @api.depends('line_ids')
    def _compute_sale_order(self):
        if self.line_ids:
            for move in self:
                sales = move.line_ids.sale_line_ids.order_id.filtered(lambda r: r.state in ('sale', 'done'))
                move.sale_id = sales