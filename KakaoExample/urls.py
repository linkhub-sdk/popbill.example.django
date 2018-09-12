# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 플러스친구 계정관리
    url(r'^GetURL_PLUSFRIEND$', views.getURL_PLUSFRIEND, name='GetURL_plusfriend'),
    url(r'^ListPlusFriendID$', views.listPlusFriendID, name='ListPlusFriendID'),

    # 발신번호 관리
    url(r'^GetURL_SENDER$', views.getURL_SENDER, name='GetURL_sender'),
    url(r'^GetSenderNumberList$', views.getSenderNumberList, name='GetSenderNumberLis'),

    # 알림톡 템플릿관리
    url(r'^GetURL_TEMPLATE$', views.getURL_TEMPLATE, name='GetURL_template'),
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

    # 정보확인
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetURL_BOX$', views.getURL_BOX, name='GetURL_BOX'),

    # 접수번호 관련 기능 (요청번호 미할당)
    url(r'^GetMessages$', views.getMessages, name='GetMessages'),
    url(r'^CancelReserve$', views.cancelReserve, name='CancelReserve'),

    # 요청번호 할당 전송건 관련 기능
    url(r'^GetMessagesRN$', views.getMessagesRN, name='GetMessagesRN'),
    url(r'^CancelReserveRN$', views.cancelReserveRN, name='CancelReserveRN'),

    # 포인트 관리
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetPopbillURL_CHRG$', views.getPopbillURL_CHRG, name='GetPopbillURL_CHRG'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetPopbillURL_LOGIN$', views.getPopbillURL_LOGIN, name='GetPopbillURL_LOGIN'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]
