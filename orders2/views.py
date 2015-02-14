from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import datetime

from orders2.models import Order

# Create your views here.

def create_employee_order(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
