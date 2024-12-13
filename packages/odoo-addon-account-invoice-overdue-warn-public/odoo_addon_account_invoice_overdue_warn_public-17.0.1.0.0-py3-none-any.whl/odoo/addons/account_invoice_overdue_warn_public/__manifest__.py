# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Overdue Warn Public",
    "summary": "Show overdue warning to all internal users",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-credit-control",
    "author": "Alberto Martínez, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_invoice_overdue_warn",
    ],
    "data": [
        "views/res_partner_views.xml",
    ],
}
