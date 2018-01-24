# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 휴폐업조회
    url(r'^CheckCorpNum$', views.checkCorpNum, name='CheckCorpNum'),
    url(r'^CheckCorpNums$', views.checkCorpNums, name='CheckCorpNums'),

    # 포인트 관리 / 정액제 신청
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetPopbillURL_CHRG$', views.getPopbillURL_CHRG, name='GetPopbillURL_CHRG'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetUnitCost$', views.getUnitCost, name='GetUnitCost$'),
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
    url(r'^GetPopbillURL_LOGIN$', views.getPopbillURL_LOGIN, name='getPopbillURL_LOGIN'),
]

