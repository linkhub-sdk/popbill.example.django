# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # Index Page
    url(r"^$", views.index, name="index"),
    # 사업자등록상태조회 (휴폐업조회)
    url(r"^CheckCorpNum$", views.checkCorpNum, name="CheckCorpNum"),
    url(r"^CheckCorpNums$", views.checkCorpNums, name="CheckCorpNums"),
    # 포인트 관리 / 정액제 신청
    url(r"^GetBalance$", views.getBalance, name="GetBalance"),
    url(r"^GetChargeURL", views.getChargeURL, name="GetChargeURL"),
    url(r"^GetPaymentURL", views.getPaymentURL, name="GetPaymentURL"),
    url(r"^GetUseHistoryURL", views.getUseHistoryURL, name="GetUseHistoryURL"),
    url(r"^GetPartnerBalance$", views.getPartnerBalance, name="GetPartnerBalance"),
    url(r"^GetPartnerURL$", views.getPartnerURL, name="GetPartnerURL"),
    url(r"^GetUnitCost$", views.getUnitCost, name="GetUnitCost"),
    url(r"^GetChargeInfo$", views.getChargeInfo, name="GetChargeInfo"),
    url(r"^PaymentRequest$", views.paymentRequest, name="PaymentRequest"),
    url(r"^GetSettleResult$", views.getSettleResult, name="GetSettleResult"),
    url(r"^GetPaymentHistory$", views.getPaymentHistory, name="GetPaymentHistory"),
    url(r"^GetUseHistory$", views.getUseHistory, name="GetUseHistory"),
    url(r"^Refund$", views.refund, name="Refund"),
    url(r"^GetRefundHistory$", views.getRefundHistory, name="GetRefundHistory"),
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
    url(r"^GetAccessURL", views.getAccessURL, name="GetAccessURL"),
    url(r"^QuitMember$", views.quitMember, name="QuitMember"),
]
