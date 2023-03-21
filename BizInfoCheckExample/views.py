# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import (
    BizInfoCheckService,
    ContactInfo,
    CorpInfo,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 BizInfoCheckService 객체 생성
bizInfoCheckService = BizInfoCheckService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
bizInfoCheckService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
bizInfoCheckService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
bizInfoCheckService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, 권장(True)
bizInfoCheckService.UseLocalTimeYN = settings.UseLocalTimeYN


def index(request):
    return render(request, "BizInfoCheck/Index.html", {})


def checkBizInfo(request):
    """
    사업자번호 1건에 대한 기업정보를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/check#CheckBizInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 조회 사업자번호
        targetCorpNum = "1234567890"

        bizCheckInfo = bizInfoCheckService.checkBizInfo(CorpNum, targetCorpNum)

        return render(
            request, "BizInfoCheck/CheckBizInfo.html", {"bizCheckInfo": bizCheckInfo}
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = bizInfoCheckService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = bizInfoCheckService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = bizInfoCheckService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = bizInfoCheckService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = bizInfoCheckService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = bizInfoCheckService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getUnitCost(request):
    """
    휴폐업 조회시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        result = bizInfoCheckService.getUnitCost(CorpNum)

        return render(request, "result.html", {"result": result})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getChargeInfo(request):
    """
    팝빌 휴폐업조회 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = bizInfoCheckService.getChargeInfo(CorpNum)

        return render(request, "getChargeInfo.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#PaymentRequest
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 무통장입금 요청 객체
        paymentForm = PaymentForm(
            # 담당자명
            settlerName = "담당자 이름",
            # 담당자 이메일
            settlerEmail = "popbill_django_test@email.com",
            # 담당자 휴대폰
            notifyHP = "01012341234",
            # 입금자명
            paymentName = "입금자",
            # 결제금액
            settleCost = "10000",
        )
        # 팝빌회원 아이디
        UserID = settings.testUserID
        response = bizInfoCheckService.paymentRequest(CorpNum, paymentForm , UserID)
        return render(request, "paymentResponse.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 정산코드
        SettleCode = "202303070000000052"
        # 팝빌회원 아이디
        UserID = settings.testUserID
        response = bizInfoCheckService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetPaymentHistory
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 조회 기간의 시작일자 (형식 : yyyyMMdd)
        SDate = "20230101"
        # 조회 기간의 종료일자 (형식 : yyyyMMdd)
        EDate = "20230131"
        # 목록 페이지번호 (기본값 1)
        Page = 1
        # 페이지당 표시할 목록 개수 (기본값 500, 최대 1,000)
        PerPage = 500
        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = bizInfoCheckService.getPaymentHistory(
            CorpNum, SDate, EDate, Page, PerPage, UserID
        )
        return render(request, "paymentHistoryResult.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetUseHistory
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 조회 기간의 시작일자 (형식 : yyyyMMdd)
        SDate = "20230101"
        # 조회 기간의 종료일자 (형식 : yyyyMMdd)
        EDate = "20230110"
        # 목록 페이지번호 (기본값 1)
        Page = 1
        # 페이지당 표시할 목록 개수 (기본값 500, 최대 1,000)
        PerPage = 500
        # 거래일자를 기준으로 하는 목록 정렬 방향 : "D" / "A" 중 택 1
        Order = "D"
        # 팝빌회원 아이디
        UserID = settings.testUserID
        response = bizInfoCheckService.getUseHistory(
            CorpNum, SDate, EDate, Page, PerPage, Order, UserID
        )
        return render(request, "useHistoryResult.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/point#Refund
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 환불신청 객체정보
        refundForm = RefundForm(
            # 담당자명
            contactname="환불신청테스트",
            # 담당자 연락처
            tel="01077777777",
            # 환불 신청 포인트
            requestpoint="10",
            # 은행명
            accountbank="국민",
            # 계좌번호
            accountnum="123123123-123",
            # 예금주명
            accountname="예금주",
            # 환불사유
            reason="테스트 환불 사유",
        )
        # 팝빌회원 아이디
        UserID = settings.testUserID
        response = bizInfoCheckService.refund(CorpNum, refundForm, UserID)
        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/bizinfocheck/python/api/point#GetRefundHistory
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        # 목록 페이지번호 (기본값 1)
        Page = 1
        # 페이지당 표시할 목록 개수 (기본값 500, 최대 1,000)
        PerPage = 500
        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = bizInfoCheckService.getRefundHistory(CorpNum, Page, PerPage, UserID)
        return render(request, "refundHistoryResult.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = bizInfoCheckService.checkIsMember(CorpNum)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = bizInfoCheckService.checkID(memberID)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#JoinMember
    """
    try:
        # 회원정보
        newMember = JoinForm(
            # 아이디 (6자 이상 50자 미만)
            ID="join_id_test",
            # 비밀번호 (8자 이상 20자 미만)
            # 영문, 숫자, 특수문자 조합
            Password="password123!@#",
            # 사업자번호 "-" 제외
            CorpNum="0000000000",
            # 대표자성명 (최대 100자)
            CEOName="테스트대표자성명",
            # 상호 (최대 200자)
            CorpName="테스트가입상호",
            # 주소 (최대 300자)
            Addr="테스트회사주소",
            # 업태 (최대 100자)
            BizType="테스트업태",
            # 종목 (최대 100자)
            BizClass="테스트업종",
            # 담당자 성명 (최대 100자)
            ContactName="담당자성명",
            # 담당자 이메일주소 (최대 100자)
            ContactEmail="",
            # 담당자 연락처 (최대 20자)
            ContactTEL="",
        )

        response = bizInfoCheckService.joinMember(newMember)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = bizInfoCheckService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = bizInfoCheckService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#UpdateCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 회사정보
        corpInfo = CorpInfo(
            # 대표자 성명 (최대 100자)
            ceoname="대표자_성명",
            # 상호 (최대 200자)
            corpName="상호",
            # 주소 (최대 300자)
            addr="주소",
            # 업태 (최대 100자)
            bizType="업태",
            # 종목 (최대 100자)
            bizClass="종목",
        )

        response = bizInfoCheckService.updateCorpInfo(CorpNum, corpInfo)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#RegistContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 정보
        newContact = ContactInfo(
            # 아이디 (6자 이상 50자 미만)
            id="popbill_test_id",
            # 비밀번호 (8자 이상 20자 미만)
            # 영문, 숫자, 특수문자 조합
            Password="password123!@#",
            # 담당자명 (최대 100자)
            personName="담당자명",
            # 담당자 연락처 (최대 20자)
            tel="",
            # 담당자 이메일 (최대 100자)
            email="",
            # 담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1,
        )

        response = bizInfoCheckService.registContact(CorpNum, newContact)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = bizInfoCheckService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = bizInfoCheckService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/bizinfocheck/python/api/member#UpdateContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 담당자 정보
        updateInfo = ContactInfo(
            # 담당자 아이디
            id=UserID,
            # 담당자 성명 (최대 100자)
            personName="담당자_성명",
            # 담당자 연락처 (최대 20자)
            tel="",
            # 담당자 메일주소 (최대 100자)
            email="",
            # 담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1,
        )

        response = bizInfoCheckService.updateContact(CorpNum, updateInfo)

        return render(
            request,
            "response.html",
            {"code": response.code, "message": response.message},
        )
    except PopbillException as PE:
        return render(
            request, "exception.html", {"code": PE.code, "message": PE.message}
        )
