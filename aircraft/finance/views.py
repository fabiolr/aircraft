# Create your views here.

from django.http import HttpResponse
from report import Report

def report(request):
    report = Report()
    report.build()
    report.save('/tmp/aircraft.xls')
    return HttpResponse(open('/tmp/aircraft.xls').read(), mimetype='application/vnd.ms-excel')


    
