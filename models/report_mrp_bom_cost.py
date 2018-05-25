from odoo import api, fields, models


class ReportMRPBoMCost(models.AbstractModel):
    _inherit = 'report.mrp_bom_cost'

    @api.multi
    def get_lines(self, boms):
        product_lines = []
        for bom in boms:
            products = bom.product_id
            if not products:
                products = bom.product_tmpl_id.product_variant_ids
            for product in products:
                attributes = []
                for value in product.attribute_value_ids:
                    attributes += [(value.attribute_id.name, value.name)]
                result, result2 = bom.explode(product, 1)
                product_line = {'bom': bom, 'name': product.name, 'lines': [], 'total': 0.0,
                                'currency': self.env.user.company_id.currency_id,
                                'product_uom_qty': bom.product_qty,
                                'product_uom': bom.product_uom_id,
                                'attributes': attributes}
                total = 0.0
                for bom_line, line_data in result2:
                    total_usd = bom_line.product_id.usd_com + bom_line.product_id.workforce + bom_line.product_id.gif
                    price_uom = bom_line.product_id.uom_id._compute_price(bom_line.product_id.standard_price, bom_line.product_uom_id)
                    line = {
                        'last_purchase_date': self._get_last_purchase_date(bom_line.product_id),
                        'price_unit': price_uom,
                        'product_id': bom_line.product_id,
                        'product_uom_qty': line_data['qty'],  # line_data needed for phantom bom explosion
                        'product_uom': bom_line.product_uom_id,
                        'total_price': price_uom * line_data['qty'],
                        'total_usd': total_usd,
                    }
                    total += line['total_price']
                    product_line['lines'] += [line]
                product_line['total'] = total
                product_lines += [product_line]
        return product_lines

    def _get_last_purchase_date(self, product):
        if product.purchase_ok:
            PurchaseOrderLine = self.env['purchase.order.line']
            domain = [
                ('product_id', '=', product.id),
                ('state', '=', 'purchase'),
            ]
            lines = PurchaseOrderLine.search(domain)
            if lines:
                last_purchase = lines[0].order_id
                for line in lines:
                    if line.order_id.date_approve > last_purchase.date_approve:
                        last_purchase = line.order_id
                return last_purchase.date_approve
        return False
