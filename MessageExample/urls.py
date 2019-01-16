# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 발신번호 사전등록
    url(r'^GetSenderNumberMgtURL', views.getSenderNumberMgtURL, name='GetSenderNumberMgtURL'),
    url(r'^GetSenderNumberList$', views.getSenderNumberList, name='GetSenderNumberList'),

    # 문자전송
    url(r'^SendSMS$', views.sendSMS, name='SendSMS'),
    url(r'^SendSMS_multi$', views.sendSMS_multi, name='SendSMS_multi'),
    url(r'^SendLMS$', views.sendLMS, name='SendLMS'),
    url(r'^SendLMS_multi$', views.sendLMS_multi, name='SendLMS_multi'),
    url(r'^SendMMS$', views.sendMMS, name='SendMMS'),
    url(r'^SendMMS_multi$', views.sendMMS_multi, name='SendMMS_multi'),
    url(r'^SendXMS$', views.sendXMS, name='SendXMS'),
    url(r'^SendXMS_multi$', views.sendXMS_multi, name='SendXMS_multi'),
    url(r'^CancelReserve$', views.cancelReserve, name='CancelReserve'),
    url(r'^CancelReserveRN$', views.cancelReserveRN, name='CancelReserveRN'),

    # 정보확인
    url(r'^GetMessages$', views.getMessages, name='GetMessages'),
    url(r'^GetMessagesRN$', views.getMessagesRN, name='GetMessagesRN'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetStates$', views.getStates, name='GetStates$'),
    url(r'^GetSentListURL', views.getSentListURL, name='GetSentListURL'),
    url(r'^GetAutoDenyList$', views.getAutoDenyList, name='GetAutoDenyList'),

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
    url(r'^GetAccessURL', views.getAccessURL, name='GetAccessURL'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
