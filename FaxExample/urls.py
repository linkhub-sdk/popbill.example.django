# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 발신번호 사전등록
    url(r'^CheckSenderNumber', views.checkSenderNumber, name='CheckSenderNumber'),
    url(r'^GetSenderNumberMgtURL', views.getSenderNumberMgtURL, name='GetSenderNumberMgtURL'),
    url(r'^GetSenderNumberList$', views.getSenderNumberList, name='GetSenderNumberList'),

    # 팩스 전송
    url(r'^SendFAX$', views.sendFAX, name='SendFAX'),
    url(r'^SendFAX_multi$', views.sendFAX_multi, name='SendSMS_multi'),
    url(r'^SendFAXBinary$', views.sendFAXBinary, name='SendFAXBinary'),
    url(r'^SendFAXBinary_multi$', views.sendFAXBinary_multi, name='SendFAXBinary_multi'),
    url(r'^ResendFAX$', views.resendFAX, name='ResendFAX'),
    url(r'^ResendFAXRN$', views.resendFAXRN, name='ResendFAXRN'),
    url(r'^ResendFAX_multi$', views.resendFAX_multi, name='resendFAX_multi'),
    url(r'^ResendFAXRN_multi$', views.resendFAXRN_multi, name='resendFAXRN_multi'),
    url(r'^CancelReserve$', views.cancelReserve, name='CancelReserve'),
    url(r'^CancelReserveRN$', views.cancelReserveRN, name='CancelReserveRN'),

    # 팩스전송 목록조회
    url(r'^GetFaxResult$', views.getFaxResult, name='GetFaxResult'),
    url(r'^GetFaxResultRN$', views.getFaxResultRN, name='GetFaxResultRN'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetSentListURL', views.getSentListURL, name='GetSentListURL'),
    url(r'^GetPreviewURL', views.getPreviewURL, name='GetPreviewURL'),

    # 포인트 관리
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetChargeURL', views.getChargeURL, name='GetChargeURL'),
    url(r'^PaymentRequest$', views.paymentRequest, name='PaymentRequest'),
    url(r'^GetSettleResult$', views.getSettleResult, name='GetSettleResult'),
    url(r'^GetPaymentHistory$', views.getPaymentHistory, name='GetPaymentHistory'),
    url(r'^GetPaymentURL', views.getPaymentURL, name='GetPaymentURL'),
    url(r'^GetUseHistory$', views.getUseHistory, name='GetUseHistory'),
    url(r'^GetUseHistoryURL', views.getUseHistoryURL, name='GetUseHistoryURL'),
    url(r'^Refund$', views.refund, name='Refund'),
    url(r'^GetRefundHistory$', views.getRefundHistory, name='GetRefundHistory'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetAccessURL', views.getAccessURL, name='GetAccessURL'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^GetContactInfo$', views.getContactInfo, name='GetContactInfo'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
