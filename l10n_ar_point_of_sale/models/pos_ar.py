##############################################################################
#   Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosAr(models.Model):

    _name = "pos.ar"
    _description = "Point of Sale for Argentina"

    name = fields.Char(string='Number', required=True)
    number = fields.Integer(
        string='Number',
        compute="_calc_number",
    )
    desc = fields.Char(string='Description', required=False, size=100)
    priority = fields.Integer(string='Priority', required=True, size=6)
    shop_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        required=True,
    )
    denomination_ids = fields.Many2many(
        comodel_name='invoice.denomination',
        relation='posar_denomination_rel',
        column1='pos_ar_id',
        column2='denomination_id',
        string='Denominations',
    )
    show_in_reports = fields.Boolean('Show in reports?', default=True)
    activity_start_date = fields.Date(
        string="Activity Start Date",
        required=True,
    )
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        required=True,
    )
    image = fields.Binary("Image", attachment=True)

    @api.multi
    def name_get(self):
        res = []
        for pos in self:
            if pos.desc:
                name = '{} ({})'.format(pos.name, pos.desc)
            else:
                name = pos.name

            res.append((pos.id, name))

        return res

    @api.depends("name")
    def _calc_number(self):
        for pos in self:
            try:
                number = int(pos.name)
            except ValueError:
                number = 0

            pos.number = number

    @api.constrains('name')
    def _check_pos_name(self):
        """Checks that names are digits between [1, 99999]."""

        # Matches all-digits name from 1 to 99999
        valid_pos_name = re.compile("^\d{1,5}$")
        for pos in self:
            if not re.match(valid_pos_name, pos.name):
                err = _("Error!\nThe PoS Name should be a 4-5 digit number!")
                raise ValidationError(err)

            #if len(pos.name) < 4:
            #    pos.name = pos.name.zfill(4)

    @api.onchange("number")
    def onchange_number(self):
        name = str(self.number).zfill(4)
        self.name = name
