# from odoo import models, fields, api


# class core_crm(models.Model):
#     _name = 'core_crm.core_crm'
#     _description = 'core_crm.core_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

