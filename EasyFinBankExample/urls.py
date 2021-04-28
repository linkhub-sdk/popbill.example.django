# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    url(r'^registBankAccount$', views.registBankAccount, name='RegistBankAccount'),
    url(r'^updateBankAccount$', views.updateBankAccount, name='UpdateBankAccount'),
    url(r'^closeBankAccount$', views.closeBankAccount, name='CloseBankAccount'),
    url(r'^revokeCloseBankAccount$', views.revokeCloseBankAccount, name='RevokeCloseBankAccount'),
    url(r'^deleteBankAccount$', views.deleteBankAccount, name='DeleteBankAccount'),
    url(r'^getBankAccountInfo$', views.getBankAccountInfo, name='GetBankAccountInfo'),
    url(r'^getBankAccountMgtURL$', views.getBankAccountMgtURL, name='GetBankAccountMgtURL'),
    url(r'^listBankAccount$', views.listBankAccount, name='ListBankAccount'),

    url(r'^requestJob$', views.requestJob, name='RequestJob'),
    url(r'^getJobState$', views.getJobState, name='GetJobState'),
    url(r'^listActiveJob$', views.listActiveJob, name='ListActiveJob'),

    url(r'^search$', views.search, name='Search'),
    url(r'^summary$', views.summary, name='Summary'),
    url(r'^saveMemo$', views.saveMemo, name='SaveMemo'),

    url(r'^getFlatRatePopUpURL$', views.getFlatRatePopUpURL, name='GetFlatRatePopUpURL'),
    url(r'^getFlatRateState$', views.getFlatRateState, name='GetFlatRateState'),
    url(r'^getBalance$', views.getBalance, name='GetBalance'),
    url(r'^getChargeURL$', views.getChargeURL, name='GetChargeURL'),
    url(r'^GetPaymentURL', views.getPaymentURL, name='GetPaymentURL'),
    url(r'^GetUseHistoryURL', views.getUseHistoryURL, name='GetUseHistoryURL'),
    url(r'^getPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^getPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^getChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),

    url(r'^getAccessURL', views.getAccessURL, name='GetAccessURL'),
    url(r'^checkIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^checkID$', views.checkID, name='CheckID'),
    url(r'^joinMember$', views.joinMember, name='JoinMember'),
    url(r'^getCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^updateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^registContact$', views.registContact, name='RegistContact'),
    url(r'^GetContactInfo$', views.getContactInfo, name='GetContactInfo'),
    url(r'^listContact$', views.listContact, name='ListContact'),
    url(r'^updateContact$', views.updateContact, name='UpdateContact'),


]
