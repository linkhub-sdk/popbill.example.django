# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 발신번호 사전등록
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
    url(r'^GetFaxDetail$', views.getFaxDetail, name='GetFaxDetail'),
    url(r'^GetFaxDetailRN$', views.getFaxDetailRN, name='GetFaxDetailRN'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetSentListURL', views.getSentListURL, name='GetSentListURL'),
    url(r'^GetPreviewURL', views.getPreviewURL, name='GetPreviewURL'),

    # 포인트 관리
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetChargeURL', views.getChargeURL, name='GetChargeURL'),
    url(r'^GetPaymentURL', views.getPaymentURL, name='GetPaymentURL'),
    url(r'^GetUseHistoryURL', views.getUseHistoryURL, name='GetUseHistoryURL'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),

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
