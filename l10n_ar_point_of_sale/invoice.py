# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2008-2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields


class invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _description = ""
    _columns = {
        'type': fields.selection([
            ('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ('out_debit','Customer Debit'),
            ('in_debit','Supplier Debit'),
            ],'Type', readonly=True, select=True, change_default=True),
        'pos_ar_id' : fields.many2one('pos.ar','Point of Sale'),
        'denomination_id' : fields.many2one('invoice.denomination','Denomination', readonly=True),
    }
invoice()
