# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 플러스친구 계정관리
    url('^GetURL_PLUSFRIEND$', views.getURL_PLUSFRIEND, name='GetURL_plusfriend'),
    url('^ListPlusFriendID$', views.listPlusFriendID, name='ListPlusFriendID'),

    # 발신번호 관리
    url('^GetURL_SENDER$', views.getURL_SENDER, name='GetURL_sender'),
    url('^GetSenderNumberList$', views.getSenderNumberList, name='GetSenderNumberLis'),

    # 알림톡 템플릿관리
    url('^GetURL_TEMPLATE$', views.getURL_TEMPLATE, name='GetURL_template'),
    url('^ListATSTemplate$', views.listATStemplate, name='ListATStemplate'),

    # 카카오톡 전송
    url('^SendATS_one$', views.sendATS_one, name='SendATS_one'),
    url('^SendATS_same$', views.sendATS_same, name='SendATS_same'),
    url('^SendATS_multi$', views.sendATS_multi, name='SendATS_multi'),
    url('^SendFTS_one$', views.sendFTS_one, name='SendFTS_one'),
    url('^SendFTS_same$', views.sendFTS_same, name='SendFTS_same'),
    url('^SendFTS_multi$', views.sendFTS_multi, name='SendFTS_multi'),
    url('^SendFMS_one$', views.sendFMS_one, name='SendFMS_one'),
    url('^SendFMS_same$', views.sendFMS_same, name='SendFMS_same'),
    url('^SendFMS_multi$', views.sendFMS_multi, name='SendFMS_multi'),
    url('^CancelReserve$', views.cancelReserve, name='CancelReserve'),

    # 정보확인
    url(r'^GetMessages$', views.getMessages, name='GetMessages'),
    url(r'^Search$', views.search, name='Search'),
    url(r'^GetURL_BOX$', views.getURL_BOX, name='GetURL_BOX'),

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
