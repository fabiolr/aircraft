# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from finance.report import Report
from finance.models import ExpenseCategory
from expense.models import FixedExpense

from . import set_ammount, dev

class TestDirectExpense(TestCase):

    def test_regression__report_is_properly_built_with_a_lot_of_rows(self):
        #VERY slow (6s). Maybe should be skipped
        category = ExpenseCategory.objects.create(name='category', expense_type=3)

        for i in range(350):
            expense = FixedExpense.objects.create(start=date(2012, 7, 1),
                                                  end=date(2012, 7, 30),
                                                  date=date(2012, 8, 1),
                                                  ammount=1000,
                                                  category=category,
                                                  )
            set_ammount(expense, 1000)

        report = Report()
        report.build()

