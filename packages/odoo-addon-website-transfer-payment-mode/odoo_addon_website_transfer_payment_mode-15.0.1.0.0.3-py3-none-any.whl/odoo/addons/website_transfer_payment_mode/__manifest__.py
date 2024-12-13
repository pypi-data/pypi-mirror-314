# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Transfer Payment Mode",
    "version": "15.0.1.0.0",
    "author": "Sygel",
    "category": "Web",
    "summary": "Transfer payment mode from website to SO.",
    "website": "https://github.com/sygel-technology/sy-e-commerce",
    "depends": [
        "sale",
        "account_payment_sale",
        "payment",
    ],
    "data": [
        "views/payment_views.xml",
    ],
}
