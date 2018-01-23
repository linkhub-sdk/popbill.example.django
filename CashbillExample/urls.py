# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 현금영수증 발행
    url(r'^CheckMgtKeyInUse$', views.checkMgtKeyInUse, name='CheckMgtKeyInUse'),
    url(r'^RegistIssue$', views.registIssue, name='RegistIssue'),
    url(r'^Register$', views.register, name='Register'),
    url(r'^Update$', views.update, name='Update'),
    url(r'^Issue$', views.issue, name='Issue'),
    url(r'^CancelIssue$', views.cancelIssue, name='CancelIssue'),
    url(r'^Delete$', views.delete, name='Delete'),

    # 취소현금영수증 발행
    url(r'^RevokeRegistIssue$', views.revokeRegistIssue, name='RevokeRegistIssue'),
    url(r'^RevokeRegistIssue_part$', views.revokeRegistIssue_part, name='RevokeRegistIssue_part'),
    url(r'^RevokeRegister$', views.revokeRegister, name='RevokeRegister'),
    url(r'^RevokeRegister_part$', views.revokeRegister_part, name='RevokeRegister_part'),

    # 현금영수증 정보확인
    url(r'^GetInfo$', views.getInfo, name='GetInfo'),
    url(r'^GetInfos$', views.getInfos, name='GetInfos'),
    url(r'^GetDetailInfo$', views.getDetailInfo, name='GetDetailInfo'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetLogs$', views.getLogs, name='GetLogs'),
    url(r'^GetURL$', views.getURL, name='GetURL'),

    # 현금영수증 보기/인쇄
    url(r'^GetPrintURL$', views.getPrintURL, name='GetPrintURL'),
    url(r'^GetEPrintURL$', views.getEPrintURL, name='GetEPrintURL'),
    url(r'^GetMassPrintURL$', views.getMassPrintURL, name='GetMassPrintURL'),
    url(r'^GetMailURL$', views.getMailURL, name='GetMailURL'),

    # 부가 기능
    url(r'^GetPopbillURL_LOGIN$', views.getPopbillURL_LOGIN, name='getPopbillURL_LOGIN'),
    url(r'^SendEmail$', views.sendEmail, name='SendEmail'),
    url(r'^SendSMS$', views.sendSMS, name='SendSMS'),
    url(r'^SendFAX$', views.sendFAX, name='SendFAX'),

    # 포인트 관리
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetPopbillURL_CHRG$', views.getPopbillURL_CHRG, name='getPopbillURL_CHRG'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='checkIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
