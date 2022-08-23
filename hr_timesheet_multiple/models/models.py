# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_timesheets = fields.One2many('hr.employee.timesheets', 'res_id', string='Hoja de Horas')

class HrEmployeeTimesheets(models.Model):
    _name = 'hr.employee.timesheets'

    res_id = fields.Many2one('hr.employee', 'Empleado')
    analytic_account = fields.Many2one('account.analytic.account', 'Cuenta Analítica', required=True)
    from_date = fields.Date('Desde')
    to_date = fields.Date('Hasta')
    value = fields.Float('Valor Hora', required=True)
    description = fields.Char('Observaciones')

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _timesheet_postprocess_values(self, values):
        """ Get the addionnal values to write on record
            :param dict values: values for the model's fields, as a dictionary::
                {'field_name': field_value, ...}
            :return: a dictionary mapping each record id to its corresponding
                dictionary values to write (may be empty).
        """
        result = {id_: {} for id_ in self.ids}
        sudo_self = self.sudo()  # this creates only one env for all operation that required sudo()
        # (re)compute the amount (depending on unit_amount, employee_id for the cost, and account_id for currency)
        if any(field_name in values for field_name in ['unit_amount', 'employee_id', 'account_id']):
            for timesheet in sudo_self:
                cost = timesheet.employee_id.timesheet_cost or 0.0
                if timesheet.employee_id.hr_timesheets:
                    for hr_timesheet in timesheet.employee_id.hr_timesheets:
                        if hr_timesheet.analytic_account.id == timesheet.account_id.id:
                            if not hr_timesheet.from_date and not hr_timesheet.to_date:
                                cost = hr_timesheet.value
                            if hr_timesheet.from_date and hr_timesheet.to_date:
                                if date.today() >= hr_timesheet.from_date and date.today() <= hr_timesheet.to_date:
                                    cost = hr_timesheet.value
                amount = -timesheet.unit_amount * cost
                amount_converted = timesheet.employee_id.currency_id._convert(
                    amount, timesheet.account_id.currency_id or timesheet.currency_id, self.env.company, timesheet.date)
                result[timesheet.id].update({
                    'amount': amount_converted,
                })
        return result
