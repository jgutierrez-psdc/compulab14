# -*- coding: utf-8 -*-
from odoo import models, fields, api, osv, tools
from openerp.tools.translate import _
from odoo.exceptions import UserError, ValidationError, Warning
import logging, re
_logger = logging.getLogger(__name__)


TAG_RE = re.compile(r'<[^>]+>')


EMPTY_SEQUENCE = 'Borrador'


NOTE_STATES_LIST = [
    ('draft', 'Borrador'),
    ('sent', 'Enviado por correo electrónico'),
    ('validated','Confirmado'),
    ('canceled', 'Cancelado')
]


class Note(models.Model):
    _name = 'sale_comercial.note'
    _inherit = ['mail.thread']
    _order = 'id desc'
    _rec_name = 'number'
    number = fields.Char(
        string='Código',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: EMPTY_SEQUENCE)
    state = fields.Selection(
        NOTE_STATES_LIST,
        string="Estado",
        default='draft',
        track_visibility='onchange')
    name = fields.Char(
        string='Nombre',
        required=True)
    date = fields.Date(
        string='Fecha de creacion',
        required=True)
    client_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True)
    body = fields.Text(
        string='Introducción',
        required=False)
    contact = fields.Char(
        string='Nombre de contacto',
        required=True)
    contact_mail = fields.Char(
        string='Correo electronico',
        required=True)
    contact_tel = fields.Char(
        string='Teléfono',
        required=True)
    body_ap = fields.Text(
        string='Alcance del proyecto',
        required=False)
    body_rc = fields.Text(
        string='Requerimientos del Cliente',
        required=False)
    body_su = fields.Text(
        string='Supuesto',
        required=False)
    body_anc = fields.Text(
        string='Alcances no contemplados',
        required=False)
    body_tc = fields.Text(
        string='Transferencia de conocimientos',
        required=False)
    body_sg = fields.Text(
        string='Soporte y garantía',
        required=False)
    body_cap = fields.Text(
        string='Capacitación',
        required=False)
    sale_id = fields.Many2one(
        'sale.order',
        string="Presupuesto",
        required=True)
    user_id = fields.Many2one(
        'res.users',
        string="Preventa",
        required=False)
    user_id_ec = fields.Many2one(
        'res.users',
        string="Vendedor",
        required=True)
    user_id_pv = fields.Many2many(
        'res.users',
        string="Post Venta",
        required=False)
    body_anexo = fields.Text(
        string='Anexos',
        required=False)
    check_anexo = fields.Boolean(
        string="Agregar Anexos",
        required=False)
    check_body = fields.Boolean(
        string="Agregar Introducción",
        required=False)
    check_body_ap = fields.Boolean(
        string="Agregar Alcance de proyecto",
        required=False)
    check_body_rc = fields.Boolean(
        string="Agregar Requerimientos del Cliente",
        required=False)
    check_body_su = fields.Boolean(
        string="Agregar Supuesto",
        required=False)
    check_body_anc = fields.Boolean(
        string="Agregar Alcances no contemplados",
        required=False)
    check_body_tc = fields.Boolean(
        string="Agregar Trasnferencia de conocimientos",
        required=False)
    check_body_sg = fields.Boolean(
        string="Agregar Soporte y garantia",
        required=False)
    check_body_cap = fields.Boolean(
        string="Agregar Capacitación",
        required=False)
    extra_text = fields.Char(
        string="Titulo Extra",
        required=False)
    body_extra = fields.Text(
        string='Extras',
        required=False)
    check_extra = fields.Boolean(
        string="Agregar extras",
        required=False)

    def action_validate(self):
        return self.write({'state': 'validated'})

    def action_send(self):
        self.ensure_one()
        template = self.env.ref('sale_comercial.note_email_template', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='sale_comercial.note',
            default_res_id=self.ids[0],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_so_as_sent=True,
            custom_layout="sale_comercial.note_email_notification",
            force_email=True
            )
        self.write({'state': 'sent'})
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_cancel(self):
        return self.write({'state': 'canceled'})

    def action_draft(self):
        return self.write({'state': 'draft'})
    
    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('sale_comercial') or EMPTY_SEQUENCE
        eo = TAG_RE.sub('', vals['body']) if vals['body'] else None
        eo = eo.replace('&nbsp;', '')
        ctx = self._context 
        if ctx.get('active_model') == 'sale.order': 
            vals['client_id'] = self.env['sale.order'].browse(ctx.get('active_ids')[0]).partner_id.id
        #vals['client_id'] = self.env['sale.order'].browse('partner_id')
        if not eo:
            raise ValidationError("Debe agregar un contenido al presupuesto comercial.")
        note = super(Note, self).create(vals)
        return note

    def unlink(self):
        for note in self:
            if not note.state in ['draft', 'canceled']:
                raise UserError("Solo las notas en estado \"Borrador\" pueden ser borradas.")
        return super(Note, self).unlink()
