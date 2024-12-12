# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Old Migration Fields",
    "summary": "Product Old Migration Fields",
    "version": "16.0.1.0.1",
    "category": "Inventory",
    "website": "https://github.com/sygel-technology/sy-product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "base_old_migration_fields"],
    "data": ["views/product_views.xml", "views/product_category_views.xml"],
}
