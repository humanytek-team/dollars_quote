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
    last_purchase_date = fields.Date(
        compute='_get_last_purchase',
        readonly=True,
        store=True,
    )

    @api.one
    def _get_usd_currency_id(self):
        self.usd_currency_id = self.env.ref('base.USD')

    @api.depends('product_id')
    @api.one
    def _get_last_purchase(self):
        if self.product_id.purchase_ok:
            PurchaseOrderLine = self.env['purchase.order.line']
            domain = [
                ('product_id', '=', self.product_id.id),
                ('state', '=', 'purchase'),
            ]
            lines = PurchaseOrderLine.search(domain)
            if lines:
                last_purchase = lines[0].order_id
                for line in lines:
                    if line.order_id.date_approve > last_purchase.date_approve:
                        last_purchase = line.order_id
                self.last_purchase_date = last_purchase.date_approve
