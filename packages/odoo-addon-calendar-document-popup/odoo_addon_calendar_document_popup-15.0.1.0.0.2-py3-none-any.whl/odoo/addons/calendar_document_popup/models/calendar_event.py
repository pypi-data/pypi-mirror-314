# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.http import request


class Meeting(models.Model):
    _inherit = "calendar.event"

    documents_link = fields.Char(
        compute="get_documents_link", string="Documents", store=True
    )

    @api.depends("res_model", "res_id")
    def get_documents_link(self):
        url_base = request.env["ir.config_parameter"].get_param("web.base.url")
        for record in self:
            res = ""
            if record.res_model and record.res_id:
                res = url_base
                res += "/web#id={}&view_type=form&model={}".format(
                    record.res_id, record.res_model
                )
            record.documents_link = res
