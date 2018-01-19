# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls import include

from config.views import Index

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^TaxinvoiceExample/', include('TaxinvoiceExample.urls'), name='TaxinvoiceExample'),
    url(r'^StatementExample/', include('StatementExample.urls'), name='StatementExample'),
    url(r'^CashbillExample/', include('CashbillExample.urls'), name='CashbillExample'),
    # url(r'^MessageExample/', include('MessageExample.urls'), name='MessageExample'),
    # url(r'^FaxExample/', include('FaxExample.urls'), name='FaxExample'),
    # url(r'^HTTaxinvoiceExample/', include('HTTaxinvoiceExample.urls'), name='HTTaxinvoiceExample'),
    # url(r'^HTCashbillExample/', include('HTCashbillExample.urls'), name='HTCashbillExample'),
    # url(r'^ClosedownExample/', include('ClosedownExample.urls'), name='ClosedownExample'),
]
