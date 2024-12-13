# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar Document Popup",
    "summary": "Display Documents in Calendar Popup",
    "version": "15.0.1.0.0",
    "category": "Calendar",
    "website": "https://github.com/sygel-technology/sy-calendar",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "calendar",
    ],
    "data": ["views/calendar_views.xml"],
}
