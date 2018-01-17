# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 정발행/역발행/위수탁발행
    url(r'^CheckMgtKeyInUse$', views.checkMgtKeyInUse, name='CheckMgtKeyInUse'),
    url(r'^RegistIssue$', views.registIssue, name='RegistIssue'),
    url(r'^Register$', views.register, name='Register'),
    url(r'^Update$', views.update, name='Update'),
    url(r'^Issue$', views.issue, name='Issue'),
    url(r'^CancelIssue$', views.cancelIssue, name='CancelIssue'),
    url(r'^Send$', views.send, name='Send'),
    url(r'^CancelSend$', views.cancelSend, name='CancelSend'),
    url(r'^Accept$', views.accept, name='Accept'),
    url(r'^Deny$', views.deny, name='Deny'),
    url(r'^Delete$', views.delete, name='Delete'),
    url(r'^Request$', views.request, name='Request'),
    url(r'^CancelRequest$', views.cancelRequest, name='CancelRequest'),
    url(r'^Refuse$', views.refuse, name='Refuse'),

    # 국세청 즉시 전송
    url(r'^SendToNTS$', views.sendToNTS, name='SendToNTS'),

    # 세금계산서 정보확인
    url(r'^GetInfo$', views.getInfo, name='GetInfo'),
    url(r'^GetInfos$', views.getInfos, name='GetInfos'),
    url(r'^GetDetailInfo$', views.getDetailInfo, name='GetDetailInfo'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetLogs$', views.getLogs, name='GetLogs'),
    url(r'^GetURL$', views.getURL, name='GetURL'),

    # 세금계산서 보기인쇄
    url(r'^GetPrintURL$', views.getPrintURL, name='GetPrintURL'),
    url(r'^GetEPrintURL$', views.getEPrintURL, name='GetEPrintURL'),
    url(r'^GetMassPrintURL$', views.getMassPrintURL, name='GetMassPrintURL'),
    url(r'^GetMailURL$', views.getMailURL, name='GetMailURL'),

    # 부가 기능
    url(r'^GetPopbillURL_LOGIN$', views.getPopbillURL_LOGIN, name='GetPopUpURL_LOGIN'),
    url(r'^GetPopbillURL_SEAL$', views.getPopbillURL_SEAL, name='GetPopUpURL_SEAL'),
    url(r'^AttachFile$', views.attachFile, name='AttachFile'),
    url(r'^DeleteFile$', views.deleteFile, name='DeleteFile'),
    url(r'^GetFiles$', views.getFiles, name='GetFiles'),
    url(r'^SendEmail$', views.sendEmail, name='SendEmail'),
    url(r'^SendSMS$', views.sendSMS, name='SendSMS'),
    url(r'^SendFAX$', views.sendFAX, name='SendFAX'),
    url(r'^AttachStatement$', views.attachStatement, name='AttachStatement'),
    url(r'^DetachStatement$', views.detachStatement, name='DetachStatement'),
    url(r'^GetEmailPublicKeys$', views.getEmailPublicKeys, name='GetEmailPublicKeys'),

    # 공인인증서 관리
    url(r'^GetPopbillURL_CERT$', views.getPopbillURL_CERT, name='getPopbillURL_CERT'),
    url(r'^GetCertificateExpireDate$', views.getCertificateExpireDate, name='GetCertificateExpireDate'),


    # 포인트 관리
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^getPopbillURL_CHRG$', views.getPopbillURL_CHRG, name='GetPopUpURL_CHRG'),
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

