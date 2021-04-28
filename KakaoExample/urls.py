# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 플러스친구 계정관리
    url(r'^GetPlusFriendMgtURL', views.getPlusFriendMgtURL, name='GetPlusFriendMgtURL'),
    url(r'^ListPlusFriendID$', views.listPlusFriendID, name='ListPlusFriendID'),

    # 발신번호 관리
    url(r'^GetSenderNumberMgtURL', views.getSenderNumberMgtURL, name='GetSenderNumberMgtURL'),
    url(r'^GetSenderNumberList$', views.getSenderNumberList, name='GetSenderNumberLis'),

    # 알림톡 템플릿관리
    url(r'^GetATSTemplateMgtURL', views.getATSTemplateMgtURL, name='GetATSTemplateMgtURL'),
    url(r'^GetATSTemplate', views.getATSTemplate, name='GetATSTemplate'),
    url(r'^ListATSTemplate$', views.listATStemplate, name='ListATStemplate'),

    # 카카오톡 전송
    url(r'^SendATS_one$', views.sendATS_one, name='SendATS_one'),
    url(r'^SendATS_same$', views.sendATS_same, name='SendATS_same'),
    url(r'^SendATS_multi$', views.sendATS_multi, name='SendATS_multi'),
    url(r'^SendFTS_one$', views.sendFTS_one, name='SendFTS_one'),
    url(r'^SendFTS_same$', views.sendFTS_same, name='SendFTS_same'),
    url(r'^SendFTS_multi$', views.sendFTS_multi, name='SendFTS_multi'),
    url(r'^SendFMS_one$', views.sendFMS_one, name='SendFMS_one'),
    url(r'^SendFMS_same$', views.sendFMS_same, name='SendFMS_same'),
    url(r'^SendFMS_multi$', views.sendFMS_multi, name='SendFMS_multi'),
    url(r'^CancelReserve$', views.cancelReserve, name='CancelReserve'),
    url(r'^CancelReserveRN$', views.cancelReserveRN, name='CancelReserveRN'),

    # 정보확인
    url(r'^GetMessages$', views.getMessages, name='GetMessages'),
    url(r'^GetMessagesRN$', views.getMessagesRN, name='GetMessagesRN'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetSentListURL', views.getSentListURL, name='GetSentListURL'),

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
