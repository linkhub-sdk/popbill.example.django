# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import (
    ContactInfo,
    CorpInfo,
    HTCashbillService,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 HTCashbillService 객체 생성
htCashbillService = HTCashbillService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
htCashbillService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
htCashbillService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
htCashbillService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, 권장(True)
htCashbillService.UseLocalTimeYN = settings.UseLocalTimeYN

# 홈택스 연동서비스를 이용하기 위해 팝빌에 인증정보를 등록 합니다. (인증방법은 부서사용자 인증 / 인증서 인증 방식이 있습니다.)
# - 팝빌로그인 > [홈택스연동] > [환경설정] > [인증 관리] 메뉴에서 [홈택스 부서사용자 등록] 혹은
#   [홈택스 인증서 등록]을 통해 인증정보를 등록합니다.
# - 홈택스연동 인증 관리 팝업 URL(GetCertificatePopUpURL API) 반환된 URL에 접속 하여
#   [홈택스 부서사용자 등록] 혹은 [홈택스 인증서 등록]을 통해 인증정보를 등록합니다.


def index(request):
    return render(request, "HTCashbill/Index.html", {})


def requestJob(request):
    """
    홈택스에 신고된 현금영수증 매입/매출 내역 수집을 팝빌에 요청합니다. (조회기간 단위 : 최대 3개월)
    - https://developers.popbill.com/reference/htcashbill/python/api/job#RequestJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 유형, [SELL-매출 현금영수증 / BUY-매입 현금영수증]
        Type = "SELL"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        result = htCashbillService.requestJob(CorpNum, Type, SDate, EDate)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getJobState(request):
    """
    수집 요청(RequestJob API) 함수를 통해 반환 받은 작업 아이디의 상태를 확인합니다.
    - 수집 결과 조회(Search API) 함수 또는 수집 결과 요약 정보 조회(Summary API) 함수를 사용하기 전에
    수집 작업의 진행 상태, 수집 작업의 성공 여부를 확인해야 합니다.
    - 작업 상태(jobState) = 3(완료)이고 수집 결과 코드(errorCode) = 1(수집성공)이면
    수집 결과 조회(Search) 또는 수집 결과 요약 정보 조회(Summary) 를 해야합니다.
    - 작업 상태(jobState)가 3(완료)이지만 수집 결과 코드(errorCode)가 1(수집성공)이 아닌 경우에는
    오류메시지(errorReason)로 수집 실패에 대한 원인을 파악할 수 있습니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/job#GetJobState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob) 호출시 발급받은 작업아이디
        jobID = "019012312000000001"

        response = htCashbillService.getJobState(CorpNum, jobID)

        return render(request, "HTCashbill/GetJobState.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listActiveJob(request):
    """
    현금영수증 매입/매출 내역 수집요청에 대한 상태 목록을 확인합니다.
    - 수집 요청 후 1시간이 경과한 수집 요청건은 상태정보가 반환되지 않습니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/job#ListActiveJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        list = htCashbillService.listActiveJob(CorpNum)

        return render(request, "HTCashbill/ListActiveJob.html", {"list": list})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    수집 상태 확인(GetJobState API) 함수를 통해 상태 정보 확인된 작업아이디를 활용하여 현금영수증 매입/매출 내역을 조회합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/search#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "019012312000000001"

        # 문서형태 배열 ("N" 와 "C" 중 선택, 다중 선택 가능)
        # └ N = 일반 현금영수증 , C = 취소현금영수증
        # - 미입력 시 전체조회
        TradeType = ["N", "C"]

        # 거래구분 배열 ("P" 와 "C" 중 선택, 다중 선택 가능)
        # └ P = 소득공제용 , C = 지출증빙용
        # - 미입력 시 전체조회
        TradeUsage = ["P", "C"]

        # 페이지번호
        Page = 1

        # 페이지당 목록개수, 최대값 1000
        PerPage = 10

        # 정렬방향 D-내림차순, A-오름차순
        Order = "D"

        response = htCashbillService.search(CorpNum, JobID, TradeType, TradeUsage, Page, PerPage, Order)

        return render(request, "HTCashbill/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def summary(request):
    """
    수집 상태 확인(GetJobState API) 함수를 통해 상태 정보가 확인된 작업아이디를 활용하여 수집된 현금영수증 매입/매출 내역의 요약 정보를 조회합니다.
    - 요약 정보 : 현금영수증 수집 건수, 공급가액 합계, 세액 합계, 봉사료 합계, 합계 금액
    - https://developers.popbill.com/reference/htcashbill/python/api/search#Summary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "019012312000000001"

        # 문서형태 배열 ("N" 와 "C" 중 선택, 다중 선택 가능)
        # └ N = 일반 현금영수증 , C = 취소현금영수증
        # - 미입력 시 전체조회
        TradeType = ["N", "C"]

        # 거래구분 배열 ("P" 와 "C" 중 선택, 다중 선택 가능)
        # └ P = 소득공제용 , C = 지출증빙용
        # - 미입력 시 전체조회
        TradeUsage = ["P", "C"]

        response = htCashbillService.summary(CorpNum, JobID, TradeType, TradeUsage)

        return render(request, "HTCashbill/Summary.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCertificatePopUpURL(request):
    """
    홈택스연동 인증정보를 관리하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#GetCertificatePopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getCertificatePopUpURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCertificateExpireDate(request):
    """
    팝빌에 등록된 인증서 만료일자를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#GetCertificateExpireDate
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        expiredate = htCashbillService.getCertificateExpireDate(CorpNum)

        return render(request,"HTCashbill/GetCertificateExpireDate.html",{"expiredate": expiredate})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkCertValidation(request):
    """
    팝빌에 등록된 인증서로 홈택스 로그인 가능 여부를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#CheckCertValidation
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.checkCertValidation(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registDeptUser(request):
    """
    홈택스연동 인증을 위해 팝빌에 현금영수증 자료조회 부서사용자 계정을 등록합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#RegistDeptUser
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 홈택스 부서사용자 계정아이디
        DeptUserID = "deptuserid"

        # 홈택스 부서사용자 계정비밀번호
        DeptUserPWD = "deptuserpwd"

        response = htCashbillService.registDeptUser(CorpNum, DeptUserID, DeptUserPWD)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkDeptUser(request):
    """
    홈택스연동 인증을 위해 팝빌에 등록된 현금영수증 자료조회 부서사용자 계정을 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#CheckDeptUser
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.checkDeptUser(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkLoginDeptUser(request):
    """
    팝빌에 등록된 현금영수증 자료조회 부서사용자 계정 정보로 홈택스 로그인 가능 여부를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#CheckLoginDeptUser
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.checkLoginDeptUser(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def deleteDeptUser(request):
    """
    팝빌에 등록된 홈택스 현금영수증 자료조회 부서사용자 계정을 삭제합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/cert#DeleteDeptUser
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.deleteDeptUser(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFlatRatePopUpURL(request):
    """
    홈택스연동 정액제 서비스 신청 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetFlatRatePopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getFlatRatePopUpURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFlatRateState(request):
    """
    홈택스연동 정액제 서비스 상태를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetFlatRateState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        flatRateState = htCashbillService.getFlatRateState(CorpNum)

        return render(request,"HTCashbill/GetFlatRateState.html",{"flatRateState": flatRateState})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = htCashbillService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = htCashbillService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = htCashbillService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 홈택스연동(현금) API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = htCashbillService.getChargeInfo(CorpNum)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#PaymentRequest
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

        response = htCashbillService.paymentRequest(CorpNum, paymentForm, UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = htCashbillService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetPaymentHistory
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

        response = htCashbillService.getPaymentHistory(CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#GetUseHistory
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

        response = htCashbillService.getUseHistory(CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/point#Refund
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

        response =  htCashbillService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/htcashbill/python/api/point#GetRefundHistory
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

        response = htCashbillService.getRefundHistory(CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.checkIsMember(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = htCashbillService.checkID(memberID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#JoinMember
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

        response = htCashbillService.joinMember(newMember)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htCashbillService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htCashbillService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#UpdateCorpInfo
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

        response = htCashbillService.updateCorpInfo(CorpNum, corpInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#RegistContact
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

        response = htCashbillService.registContact(CorpNum, newContact)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = htCashbillService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = htCashbillService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#UpdateContact
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

        response = htCashbillService.updateContact(CorpNum, updateInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def QuitRequest(request):
    """
    - https://developers.popbill.com/reference/htcashbill/python/api/member#QuitRequest
    """
    try:
        CorpNum = settings.testCorpNum
        QuitReason = ""
        UserID = settings.testUserID

        response = htCashbillService.QuitRequest(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def GetRefundResult(request):
    """
    환불 요청의 결과를 조회합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#GetRefundResult
    """
    try:
        CorpNum = settings.testCorpNum
        RefundCode = ""
        UserID = settings.testUserID

        response = htCashbillService.GetRefundableResult(CorpNum,RefundCode,UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def GetRefundablePoint(request):
    """
    회원 탈퇴 시, 환불 가능한 포인트를 확인합니다.
    - https://developers.popbill.com/reference/htcashbill/python/api/member#GetRefundablePoint
    """
    try:
        CorpNum = settings.testCorpNum
        UserID = settings.testUserID

        response = htCashbillService.GetRefundablePoint(CorpNum, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})