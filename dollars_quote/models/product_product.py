from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    usd_com = fields.Monetary(
        currency_field='usd_currency_id',
        string='USD Cost of Materials',
    )
    workforce = fields.Monetary(
        currency_field='usd_currency_id',
    )
    gif = fields.Monetary(
        currency_field='usd_currency_id',
        string='GIF',
    )
    usd_currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_get_usd_currency_id',
    )

    @api.one
    def _get_usd_currency_id(self):
        self.usd_currency_id = self.env.ref('base.USD')
