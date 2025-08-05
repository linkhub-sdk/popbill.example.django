# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r"^$", views.index, name="index"),
    # 전자명세서 발행
    url(r"^CheckMgtKeyInUse$", views.checkMgtKeyInUse, name="CheckMgtKeyInUse"),
    url(r"^RegistIssue$", views.registIssue, name="RegistIssue"),
    url(r"^Register$", views.register, name="Register"),
    url(r"^Update$", views.update, name="Update"),
    url(r"^Issue$", views.issue, name="Issue"),
    url(r"^Cancel$", views.cancel, name="Cancel"),
    url(r"^Delete$", views.delete, name="Delete"),
    # 세금계산서 정보확인
    url(r"^GetInfo$", views.getInfo, name="GetInfo"),
    url(r"^GetInfos$", views.getInfos, name="GetInfos"),
    url(r"^GetDetailInfo$", views.getDetailInfo, name="GetDetailInfo"),
    url(r"^Search$", views.search, name="Search"),
    url(r"^GetLogs$", views.getLogs, name="GetLogs"),
    url(r"^GetURL$", views.getURL, name="GetURL"),
    # 명세서 보기인쇄
    url(r"^GetPopUpURL$", views.getPopUpURL, name="getPopUpURL"),
    url(r"^GetViewURL$", views.getViewURL, name="getViewURL"),
    url(r"^GetPrintURL$", views.getPrintURL, name="GetPrintURL"),
    url(r"^GetEPrintURL$", views.getEPrintURL, name="GetEPrintURL"),
    url(r"^GetMassPrintURL$", views.getMassPrintURL, name="GetMassPrintURL"),
    url(r"^GetMailURL$", views.getMailURL, name="GetMailURL"),
    # 부가 기능
    url(r"^GetAccessURL", views.getAccessURL, name="GetAccessURL"),
    url(r"^GetSealURL", views.getSealURL, name="GetSealURL"),
    url(r"^AttachFile$", views.attachFile, name="AttachFile"),
    url(r"^DeleteFile$", views.deleteFile, name="DeleteFile"),
    url(r"^GetFiles$", views.getFiles, name="GetFiles"),
    url(r"^SendEmail$", views.sendEmail, name="SendEmail"),
    url(r"^SendSMS$", views.sendSMS, name="SendSMS"),
    url(r"^SendFAX$", views.sendFAX, name="SendFAX"),
    url(r"^FAXSend$", views.FAXSend, name="FAXSend"),
    url(r"^AttachStatement$", views.attachStatement, name="AttachStatement"),
    url(r"^DetachStatement$", views.detachStatement, name="DetachStatement"),
    url(r"^ListEmailConfig", views.listEmailConfig, name="ListEmailConfig"),
    url(r"^UpdateEmailConfig", views.updateEmailConfig, name="UpdateEmailConfig"),
    # 포인트 관리
    url(r"^GetUnitCost$", views.getUnitCost, name="GetUnitCost"),
    url(r"^GetChargeInfo$", views.getChargeInfo, name="GetChargeInfo"),
    url(r"^GetBalance$", views.getBalance, name="GetBalance"),
    url(r"^GetChargeURL", views.getChargeURL, name="GetChargeURL"),
    url(r"^PaymentRequest$", views.paymentRequest, name="PaymentRequest"),
    url(r"^GetSettleResult$", views.getSettleResult, name="GetSettleResult"),
    url(r"^GetPaymentHistory$", views.getPaymentHistory, name="GetPaymentHistory"),
    url(r"^GetPaymentURL", views.getPaymentURL, name="GetPaymentURL"),
    url(r"^GetUseHistory$", views.getUseHistory, name="GetUseHistory"),
    url(r"^GetUseHistoryURL", views.getUseHistoryURL, name="GetUseHistoryURL"),
    url(r"^Refund$", views.refund, name="Refund"),
    url(r"^GetRefundHistory$", views.getRefundHistory, name="GetRefundHistory"),
    url(r"^GetPartnerBalance$", views.getPartnerBalance, name="GetPartnerBalance"),
    url(r"^GetPartnerURL$", views.getPartnerURL, name="GetPartnerURL"),
    url(r"^GetRefundInfo$", views.getRefundInfo, name="GetRefundInfo"),
    url(r"^GetRefundableBalance$", views.getRefundableBalance, name="GetRefundableBalance"),
    # 회원정보
    url(r"^CheckIsMember$", views.checkIsMember, name="CheckIsMember"),
    url(r"^CheckID$", views.checkID, name="CheckID"),
    url(r"^JoinMember$", views.joinMember, name="JoinMember"),
    url(r"^GetCorpInfo$", views.getCorpInfo, name="GetCorpInfo"),
    url(r"^UpdateCorpInfo$", views.updateCorpInfo, name="UpdateCorpInfo"),
    url(r"^RegistContact$", views.registContact, name="RegistContact"),
    url(r"^GetContactInfo$", views.getContactInfo, name="GetContactInfo"),
    url(r"^ListContact$", views.listContact, name="ListContact"),
    url(r"^UpdateContact$", views.updateContact, name="UpdateContact"),
    url(r"^DeleteContact$", views.deleteContact, name="DeleteContact"),
    url(r"^QuitMember$", views.quitMember, name="QuitMember"),
]
