# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 정발행/역발행/위수탁발행
    url(r'^CheckMgtKeyInUse$', views.checkMgtKeyInUse, name='CheckMgtKeyInUse'),
    url(r'^RegistIssue$', views.registIssue, name='RegistIssue'),
    url(r'^BulkSubmit$', views.bulkSubmit, name='BulkSubmit'),
    url(r'^GetBulkResult$', views.getBulkResult, name='GetBulkResult'),
    url(r'^Register$', views.register, name='Register'),
    url(r'^Update$', views.update, name='Update'),
    url(r'^Issue$', views.issue, name='Issue'),
    url(r'^CancelIssue$', views.cancelIssue, name='CancelIssue'),
    url(r'^Delete$', views.delete, name='Delete'),
    url(r'^RegistRequest$', views.registRequest, name='RegistRequest$'),
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
    url(r'^GetPopUpURL$', views.getPopUpURL, name='GetPopUpURL'),
    url(r'^GetViewURL$', views.getViewURL, name='GetViewURL'),
    url(r'^GetPrintURL$', views.getPrintURL, name='GetPrintURL'),
    url(r'^GetOldPrintURL$', views.getOldPrintURL, name='GetOldPrintURL'),
    url(r'^GetEPrintURL$', views.getEPrintURL, name='GetEPrintURL'),
    url(r'^GetMassPrintURL$', views.getMassPrintURL, name='GetMassPrintURL'),
    url(r'^GetMailURL$', views.getMailURL, name='GetMailURL'),
    url(r'^GetPDFURL$', views.getPDFURL, name='GetPDFURL'),

    # 부가 기능
    url(r'^GetAccessURL', views.getAccessURL, name='GetAccessURL'),
    url(r'^GetSealURL', views.getSealURL, name='GetSealURL'),
    url(r'^AttachFile$', views.attachFile, name='AttachFile'),
    url(r'^DeleteFile$', views.deleteFile, name='DeleteFile'),
    url(r'^GetFiles$', views.getFiles, name='GetFiles'),
    url(r'^SendEmail$', views.sendEmail, name='SendEmail'),
    url(r'^SendSMS$', views.sendSMS, name='SendSMS'),
    url(r'^SendFAX$', views.sendFAX, name='SendFAX'),
    url(r'^AttachStatement$', views.attachStatement, name='AttachStatement'),
    url(r'^DetachStatement$', views.detachStatement, name='DetachStatement'),
    url(r'^GetEmailPublicKeys$', views.getEmailPublicKeys, name='GetEmailPublicKeys'),
    url(r'^AssignMgtKey', views.assignMgtKey, name='AssignMgtKey'),
    url(r'^ListEmailConfig', views.listEmailConfig, name='ListEmailConfig'),
    url(r'^UpdateEmailConfig', views.updateEmailConfig, name='UpdateEmailConfig'),
    url(r'^GetSendToNTSConfig', views.getSendToNTSConfig, name='GetSendToNTSConfig'),

    # 공인인증서 관리
    url(r'^GetTaxCertURL', views.getTaxCertURL, name='GetTaxCertURL'),
    url(r'^GetCertificateExpireDate$', views.getCertificateExpireDate, name='GetCertificateExpireDate'),
    url(r'^CheckCertValidation', views.checkCertValidation, name='CheckCertValidation'),

    # 포인트 관리
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetChargeURL', views.getChargeURL, name='GetChargeURL'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
