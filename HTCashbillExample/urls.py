# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r'^$', views.index, name='index'),

    # 홈택스 현금영수증 매입/매출 내역 수집
    url(r'^RequestJob$', views.requestJob, name='RequestJob'),
    url(r'^GetJobState$', views.getJobState, name='GetJobState'),
    url(r'^ListActiveJob$', views.listActiveJob, name='ListActiveJob'),

    # 홈택스 현금영수증 매입/매출 내역 수집 결과 조회
    url(r'^Search$', views.search, name='Search'),
    url(r'^Summary$', views.summary, name='Summary'),
#
    # 홈택스연동 인증 관리
    url(r'^GetCertificatePopUpURL', views.getCertificatePopUpURL, name='GetCertificatePopUpURL'),
    url(r'^GetCertificateExpireDate$', views.getCertificateExpireDate, name='GetCertificateExpireDate'),
    url(r'^CheckCertValidation', views.checkCertValidation, name='CheckCertValidation'),
    url(r'^RegistDeptUser', views.registDeptUser, name='RegistDeptUser'),
    url(r'^CheckDeptUser', views.checkDeptUser, name='CheckDeptUser'),
    url(r'^CheckLoginDeptUser', views.checkLoginDeptUser, name='CheckLoginDeptUser'),
    url(r'^DeleteDeptUser', views.deleteDeptUser, name='DeleteDeptUser'),

    # 포인트 관리 / 정액제 신청
    url(r'^GetBalance$', views.getBalance, name='GetBalance'),
    url(r'^GetPopbillURL_CHRG$', views.getPopbillURL_CHRG, name='GetPopbillURL_CHRG'),
    url(r'^GetPartnerBalance$', views.getPartnerBalance, name='GetPartnerBalance'),
    url(r'^GetPartnerURL$', views.getPartnerURL, name='GetPartnerURL'),
    url(r'^GetChargeInfo$', views.getChargeInfo, name='GetChargeInfo'),
    url(r'^GetFlatRatePopUpURL$', views.getFlatRatePopUpURL, name='GetFlatRatePopUpURL'),
    url(r'^GetFlatRateState$', views.getFlatRateState, name='GetFlatRateState'),

    # 회원정보
    url(r'^CheckIsMember$', views.checkIsMember, name='CheckIsMember'),
    url(r'^CheckID$', views.checkID, name='CheckID'),
    url(r'^JoinMember$', views.joinMember, name='JoinMember'),
    url(r'^GetPopbillURL_LOGIN$', views.getPopbillURL_LOGIN, name='GetPopbillURL_LOGIN'),
    url(r'^GetCorpInfo$', views.getCorpInfo, name='GetCorpInfo'),
    url(r'^UpdateCorpInfo$', views.updateCorpInfo, name='UpdateCorpInfo'),
    url(r'^RegistContact$', views.registContact, name='RegistContact'),
    url(r'^ListContact$', views.listContact, name='ListContact'),
    url(r'^UpdateContact$', views.updateContact, name='UpdateContact'),
]

