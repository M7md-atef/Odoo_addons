# from odoo import http


# class CoreCrm(http.Controller):
#     @http.route('/core_crm/core_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/core_crm/core_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('core_crm.listing', {
#             'root': '/core_crm/core_crm',
#             'objects': http.request.env['core_crm.core_crm'].search([]),
#         })

#     @http.route('/core_crm/core_crm/objects/<model("core_crm.core_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('core_crm.object', {
#             'object': obj
#         })

