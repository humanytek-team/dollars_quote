from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    usd_com = fields.Monetary(
        related='product_id.usd_com',
    )
    usd_currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_get_usd_currency_id',
    )

    @api.depends('usd_com')
    @api.one
    def _get_usd_currency_id(self):
        self.usd_currency_id = self.env.ref('base.USD')
