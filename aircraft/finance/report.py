# -*- coding: utf-8 -*-

from datetime import date
from xlwt import Workbook, XFStyle, Pattern, Alignment, Formula, easyxf
from finance.models import Expense, Interpayment
from flight.models import Person

class Report(object):

    def __init__(self):
        self.wb = Workbook()
        self.style = Style()

    def build(self):
        self.generate_expenses()
        self.generate_responsibilities()
        self.generate_interpayments()
        self.generate_results()
        
    def generate_expenses(self):
        self.expenses = self.wb.add_sheet(u'Despesas')

        self._build_header(self.expenses,
                           (u'Data', u'Tipo', u'Categoria', u'Despesa', u'Pago por', u'Valor'))

        for expense in Expense.objects.all().order_by('date'):
            for payment in expense.payment_set.all():
                if expense.calculated:
                    self._write_line(self.expenses, (expense.date,
                                                     expense.child().__class__.__name__,
                                                     expense.category.name,
                                                     unicode(expense.child()),
                                                     payment.paid_by.name,
                                                     payment.ammount))
                else:
                    self._write_line(self.expenses, (expense.date,
                                                     expense.child().__class__.__name__,
                                                     expense.category.name,
                                                     unicode(expense.child()),
                                                     payment.paid_by.name,
                                                     '',
                                                     (payment.ammount, self.style.attention),
                                                     ))
                    
                    
                    

    def generate_responsibilities(self):
        self.responsibilities = self.wb.add_sheet(u'Responsabilidades')

        self._build_header(self.responsibilities,
                           (u'Data', u'Tipo', u'Categoria', u'Despesa', u'Responsável', u'Valor'))

        for expense in Expense.objects.filter(calculated=True).order_by('date'):
            for resp in expense.responsibility_set.all():
                self._write_line(self.responsibilities, (expense.date,
                                                         expense.child().__class__.__name__,
                                                         expense.category.name,
                                                         unicode(expense.child()),
                                                         resp.owner.name,
                                                         resp.ammount))

    def generate_interpayments(self):
        self.interpayments = self.wb.add_sheet(u'Interpagamentos')

        self._build_header(self.interpayments,
                           (u'Data', u'De', u'Para', u'Valor'))

        for interpayment in Interpayment.objects.filter(paid=True):
            self._write_line(self.interpayments, (interpayment.date,
                                                  interpayment.by.name,
                                                  interpayment.to.name,
                                                  interpayment.ammount))

    def generate_results(self):
        self.results = self.wb.add_sheet(u'Totais')

        self._build_header(self.results,
                           (u'Pessoa', u'Responsabilidade', u'Despesas pagas',
                            u'Interpagamentos feitos', u'Interpagamentos recebidos', u'Total'))

        for person in Person.objects.all():
            self._write_line(self.results,
                             (person.name,
                              Formula('Sumif(Responsabilidades!E2:E%d, Totais!A%d, Responsabilidades!F2:F%d)' %
                                      (self.responsibilities.line,
                                       self.results.line+1,
                                       self.responsibilities.line),
                                      ),
                              Formula('Sumif(Despesas!E2:E%d, Totais!A%d, Despesas!F2:F%d)' %
                                      (self.expenses.line,
                                       self.results.line+1,
                                       self.expenses.line),
                                      ),

                              Formula('Sumif(Interpagamentos!B2:B%d, Totais!A%d, Interpagamentos!D2:D%d)' %
                                      (self.interpayments.line,
                                       self.results.line+1,
                                       self.interpayments.line),
                                      ),  
                              
                              Formula('Sumif(Interpagamentos!C2:C%d, Totais!A%d, Interpagamentos!D2:D%d)' %
                                      (self.interpayments.line,
                                       self.results.line+1,
                                       self.interpayments.line),
                                      ),


                              Formula('-B%d + C%d + D%d - E%d' % ((self.results.line+1,)*4)),
                              )
                             )
                             

    def _build_header(self, sheet, header):
        for i, col in enumerate(header):
            sheet.write(0, i, col, self.style.header)
            width = self.style.width(col, 275)
            if width > sheet.col(i).width:
                sheet.col(i).width = width
        sheet.line = 1
        
    def _write_line(self, sheet, line):
        for i, col in enumerate(line):
            if isinstance(col, tuple):
                value = col[0]
                style = col[1]
            else:
                value = col
                style = self.style.guess(col)
            sheet.write(sheet.line, i, value, style)
            width = self.style.width(col, 260)
            if width > sheet.col(i).width:
                sheet.col(i).width = width
        sheet.line += 1

    def save(self, filename='/tmp/aircraft.xls'):
        self.wb.save(filename)
        

class Style():

    def __init__(self):
        self.date = self.base()
        self.date.num_format_str = r'DD/MM/YY'
        self.date.alignment.horz = Alignment.HORZ_CENTER

        self.money = self.base()
        self.money.num_format_str = '[$R$-416] #,##0.00'

        self.plain = self.base()

    def guess(self, value):
        if isinstance(value, date):
            return self.date
        elif isinstance(value, float) or isinstance(value, Formula):
            return self.money
        return self.plain

    def width(self, value, step):
        if isinstance(value, date):
            return 2000
        if isinstance(value, float) or isinstance(value, Formula):
            return 4000
        return step * len(value)

    def base(self):
        style = XFStyle()
        style.borders.top = 1
        style.borders.right = 1
        style.borders.left = 1
        style.borders.bottom = 1

        style.pattern.pattern = Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = 9 

        style.alignment.vert = Alignment.VERT_CENTER

        return style

    @property
    def header(self):
        style = self.base()
        style.font.bold = True
        style.alignment.horz = Alignment.HORZ_CENTER
        
        style.pattern.pattern = Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = 32

        style.font.colour_index = 9

        return style

    @property
    def attention(self, style=None):
        return easyxf(
            'pattern: pattern solid, back_colour red;',
            num_format_str = '[$R$-416] #,##0.00'
            )

if __name__ == '__main__':
    report = Report()
    report.build()
    report.save()
