# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger()


class EasySearch(models.AbstractModel):
    _name = "easy.search"
    _description = 'Easy Search'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        fields = self.get_search_fields()
        if fields and name:
            args = []
            for field in fields:
                if field == fields[-1]:
                    args.append(
                        (field.name, 'ilike', name)
                    )
                else:
                    args.append('|')
                    args.append(
                        (field.name, 'ilike', name)
                    )
            name = ''
        _logger.info("Args: {}".format(args))
        return super(EasySearch, self).name_search(name=name, args=args, operator=operator, limit=limit)

    def get_search_fields(self):
        all_config = self.env['easy.search.config'].sudo().search([])
        fields = self.env['ir.model.fields']
        for rec in all_config:
            if rec.model_id.model == self._name:
                for field in rec.field_ids:
                    fields |= field
        return fields


class EasySearchConfig(models.Model):
    _name = 'easy.search.config'
    _rec_name = 'model_id'
    _description = 'Easy Search Config'

    model_id = fields.Many2one(comodel_name="ir.model", string="Model Name", required=True, ondelete="set null")
    field_ids = fields.Many2many(comodel_name="ir.model.fields", string="Fields To Used In Search", required=True)
    type = fields.Selection(string="Type",
                            selection=[
                                ('base', 'Base'),
                                ('sale', 'Sale'),
                                ('crm', 'CRM'),
                                ('purchase', 'Purchase'),
                                ('stock', 'Inventory'),
                                ('account', 'Accounting'),
                            ], required=True, default='base')

    @api.onchange('model_id')
    def onchange_model_id(self):
        return {
            'domain': {
                'field_ids': [('id', 'in', self.model_id.field_id.ids)]
            }
        }
