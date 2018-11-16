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

    # 접수번호 관련 기능 (요청번호 미할당)
    url(r'^GetFaxDetail$', views.getFaxDetail, name='GetFaxDetail'),
    url(r'^CancelReserve$', views.cancelReserve, name='CancelReserve'),
    url(r'^ResendFAX$', views.resendFAX, name='ResendFAX'),
    url(r'^ResendFAX_multi$', views.resendFAX_multi, name='resendFAX_multi'),

    # 요청번호 할당 전송건 관련 기능
    url(r'^GetFaxDetailRN$', views.getFaxDetailRN, name='GetFaxDetailRN'),
    url(r'^CancelReserveRN$', views.cancelReserveRN, name='CancelReserveRN'),
    url(r'^ResendFAXRN$', views.resendFAXRN, name='ResendFAXRN'),
    url(r'^ResendFAXRN_multi$', views.resendFAXRN_multi, name='resendFAXRN_multi'),

    # 팩스전송 목록조회
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetSentListURL', views.getSentListURL, name='GetSentListURL'),
    url(r'^GetPreviewURL', views.getPreviewURL, name='GetPreviewURL'),

    # 포인트 관리
    url(r'^GetChargeURL', views.getChargeURL, name='GetChargeURL'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetAccessURL', views.getAccessURL, name='GetAccessURL'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
