# -*- coding: utf-8 -*-
# from odoo import http


# class HrTimesheetMultiple(http.Controller):
#     @http.route('/hr_timesheet_multiple/hr_timesheet_multiple/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_timesheet_multiple/hr_timesheet_multiple/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_timesheet_multiple.listing', {
#             'root': '/hr_timesheet_multiple/hr_timesheet_multiple',
#             'objects': http.request.env['hr_timesheet_multiple.hr_timesheet_multiple'].search([]),
#         })

#     @http.route('/hr_timesheet_multiple/hr_timesheet_multiple/objects/<model("hr_timesheet_multiple.hr_timesheet_multiple"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_timesheet_multiple.object', {
#             'object': obj
#         })
