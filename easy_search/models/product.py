# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'easy.search']


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'easy.search']


class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'easy.search']


class ProductSupplierInfo(models.Model):
    _name = 'product.supplierinfo'
    _inherit = ['product.supplierinfo', 'easy.search']
