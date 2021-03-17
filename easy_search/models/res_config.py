# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sales_easy_search = fields.Boolean(string="Sales", )
    module_purchase_easy_search = fields.Boolean(string="Purchase", )
    module_crm_easy_search = fields.Boolean(string="CRM", )
    module_stock_easy_search = fields.Boolean(string="Inventory", )
    module_account_easy_search = fields.Boolean(string="Accounting", )
