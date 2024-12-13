# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Overdue Warn Sale Public",
    "summary": "Show overdue warning on sale to all internal users",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-credit-control",
    "author": "Alberto Martínez, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_invoice_overdue_warn_sale",
    ],
    "data": ["views/sale_order_views.xml"],
}
