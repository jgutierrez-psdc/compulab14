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
    ('validated','Confirmado'),
    ('print', 'Impreso'),
    ('sent', 'Enviado por correo electrónico'),
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
        string='Contenido',
        required=True)

    def action_validate(self):
        return self.write({'state': 'validated'})

    def action_print(self):
        self.write({'state': 'print'})
        return self.env.ref('sale_comercial.action_report_note').report_action(self)

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

    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('sale_comercial') or EMPTY_SEQUENCE
        eo = TAG_RE.sub('', vals['body']) if vals['body'] else None
        eo = eo.replace('&nbsp;', '')
        if not eo:
            raise ValidationError("Debe agregar un contenido al presupuesto comercial.")
        note = super(Note, self).create(vals)
        return note

    def unlink(self):
        for note in self:
            if not note.state in ['draft', 'canceled']:
                raise UserError("Solo las notas en estado \"Borrador\" pueden ser borradas.")
        return super(Note, self).unlink()
