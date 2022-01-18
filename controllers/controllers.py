# -*- coding: utf-8 -*-
from odoo import http

# class SampleTransport(http.Controller):
#     @http.route('/sample_transport/sample_transport/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sample_transport/sample_transport/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sample_transport.listing', {
#             'root': '/sample_transport/sample_transport',
#             'objects': http.request.env['sample_transport.sample_transport'].search([]),
#         })

#     @http.route('/sample_transport/sample_transport/objects/<model("sample_transport.sample_transport"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sample_transport.object', {
#             'object': obj
#         })