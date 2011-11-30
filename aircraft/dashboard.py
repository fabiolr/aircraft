# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'aircraft.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'aircraft.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    columns = 2
    
    #def init_with_context(self, context):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        #site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            u'Avião', ('flight.models.Flight',
                       'flight.models.Outage',
                       ),
            
            ))

        self.children.append(modules.ModelList(
            u'Despesas', ('expense.models.DirectExpense',
                          'expense.models.VariableExpense',
                          'expense.models.FixedExpense',
                          'expense.models.HourlyMantainance',
                          'expense.models.ScheduleMantainance',
                          'expense.models.EventualMantainance',
                          ),
            
            ))
        
        self.children.append(modules.ModelList(
            u'Finanças', ('finance.models.Interpayment',
                          'finance.models.Expense',
                          'finance.models.ExpenseCategory',
                          ),
            
            ))
        
        self.children.append(modules.LinkList(
                u'Relatórios',
                children=(
                    {
                        'title': 'Relatório completo',
                        'url': '/admin/finance/aircraft.xls',
                        'external': False,
                        'description': 'Baixar relatório em excel contendo das as despesas, responsabilidades e pagamentos',
                        },
                    )
                ))

        self.children.append(modules.ModelList(
            _('Administration'), ('django.contrib.auth.models.User',
                                  'flight.models.Person',
                                  ),
            
            ))


        self.children.append(modules.RecentActions(_('Recent Actions'), 15))

        



class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for aircraft.
    """

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        self.children.append(modules.ModelList(self.app_title, self.models))

        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            include_list=self.get_app_content_types(),
            limit=15
            ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
