# Copyright 2011-2012 Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.addons import base
if 'geoengine' not in base.models.ir_actions.VIEW_TYPES:
    base.models.ir_actions.VIEW_TYPES.append(('geoengine', 'Geoengine'))

GEO_TYPES = [('geo_polygon', 'geo_polygon'),
             ('geo_multi_polygon', 'geo_multi_polygon'),
             ('geo_point', 'geo_point'),
             ('geo_multi_point', 'geo_multi_point'),
             ('geo_line', 'geo_line'),
             ('geo_multi_line', 'geo_multi_line')]

POSTGIS_GEO_TYPES = [('POINT', 'POINT'),
                     ('MULTIPOINT', 'MULTIPOINT'),
                     ('LINESTRING', 'LINESTRING'),
                     ('MULTILINESTRING', 'MULTILINESTRING'),
                     ('POLYGON', 'POLYGON'),
                     ('MULTIPOLYGON', 'MULTIPOLYGON')]


class IrModelField(models.Model):
    _inherit = 'ir.model.fields'

    @api.model
    def _get_fields_type(self):
        cr = self._cr
        cr.execute('SELECT DISTINCT ttype,ttype from ir_model_fields')
        res = cr.fetchall()
        to_return = list(set(res+GEO_TYPES))
        to_return.sort()
        return to_return

    srid = fields.Integer(
        'srid',
        required=False
    )
    geo_type = fields.Selection(
        POSTGIS_GEO_TYPES,
        string="PostGIs type"
    )
    dim = fields.Selection(
        [(2, '2'), (3, '3'), (4, '4')],
        string="PostGIs Dimension",
    )
    gist_index = fields.Boolean(
        'Create gist index'
    )
    ttype = fields.Selection(
        '_get_fields_type',
        'Field Type',
        required=True
    )
