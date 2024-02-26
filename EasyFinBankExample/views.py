"""
팝빌 계좌조회 API Python SDK Django Example

Django 연동 튜토리얼 안내 : https://developers.popbill.com/guide/easyfinbank/python/getting-started/tutorial
연동 기술지원 연락처 : 1600-9854
연동 기술지원 이메일 : code@linkhubcorp.com
"""
# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import (
    BankAccountInfo,
    ContactInfo,
    CorpInfo,
    EasyFinBankService,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 계좌조회 서비스 객체 생성
easyFinBankService = EasyFinBankService(settings.LinkID, settings.SecretKey)

# 연동환경 설정, true-테스트, false-운영(Production), (기본값:true)
easyFinBankService.IsTest = settings.IsTest

# 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
easyFinBankService.IPRestrictOnOff = settings.IPRestrictOnOff

# 통신 IP 고정, true-사용, false-미사용, (기본값:false)
easyFinBankService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, true-사용, false-미사용, (기본값:true)
easyFinBankService.UseLocalTimeYN = settings.UseLocalTimeYN


def index(request):
    return render(request, "EasyFinBank/Index.html", {})


def registBankAccount(request):
    """
    팝빌에 계좌정보를 등록합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#RegistBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        infoObj = BankAccountInfo(
            # 기관코드
            # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
            # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
            # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
            BankCode="",

            # 계좌번호 하이픈('-') 제외
            AccountNumber="",

            # 계좌비밀번호
            AccountPWD="",

            # 계좌유형, "법인" 또는 "개인" 입력
            AccountType="",

            # 예금주 식별정보 ('-' 제외)
            # 계좌유형이 "법인"인 경우 : 사업자번호(10자리)
            # 계좌유형이 "개인"인 경우 : 예금주 생년월일 (6자리-YYMMDD)
            IdentityNumber="",

            # 계좌 별칭
            AccountName="",

            # 인터넷뱅킹 아이디 (국민은행 필수)
            BankID="",

            # 조회전용 계정 아이디 (대구은행, 신협, 신한은행 필수)
            FastID="",

            # 조회전용 계정 비밀번호 (대구은행, 신협, 신한은행 필수
            FastPWD="",

            # 결제기간(개월), 1~12 입력가능, 미기재시 기본값(1) 처리
            # - 파트너 과금방식의 경우 입력값에 관계없이 1개월 처리
            UsePeriod="1",

            # 메모
            Memo="",
        )

        response = easyFinBankService.registBankAccount(CorpNum, infoObj)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateBankAccount(request):
    """
    팝빌에 등록된 계좌정보를 수정합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#UpdateBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        infoObj = BankAccountInfo(
            # 기관코드
            # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
            # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
            # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
            BankCode="",

            # 계좌번호 하이픈('-') 제외
            AccountNumber="",

            # 계좌비밀번호
            AccountPWD="",

            # 계좌 별칭
            AccountName="",

            # 인터넷뱅킹 아이디 (국민은행 필수)
            BankID="",

            # 조회전용 계정 아이디 (대구은행, 신협, 신한은행 필수)
            FastID="",

            # 조회전용 계정 비밀번호 (대구은행, 신협, 신한은행 필수
            FastPWD="",

            # 메모
            Memo="",
        )

        response = easyFinBankService.updateBankAccount(CorpNum, infoObj)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBankAccountInfo(request):
    """
    팝빌에 등록된 계좌정보를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#GetBankAccountInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # 계좌번호
        AccountNumber = ""

        response = easyFinBankService.getBankAccountInfo(CorpNum, BankCode, AccountNumber)

        return render(request, "EasyFinBank/GetBankAccountInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listBankAccount(request):
    """
    팝빌에 등록된 계좌 목록을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#ListBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        bankAccountList = easyFinBankService.listBankAccount(CorpNum)

        return render(request, "EasyFinBank/ListBankAccount.html", {"list": bankAccountList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBankAccountMgtURL(request):
    """
    계좌 관리 팝업 URL을 반환 합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#GetBankAccountMgtURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getBankAccountMgtURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def closeBankAccount(request):
    """
    계좌의 정액제 해지를 요청합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#CloseBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # 계좌번호 하이픈('-') 제외
        AccountNumber = ""

        # 해지유형, "일반", "중도" 중 택 1
        # - 일반(일반해지) - 해지 요청일이 포함된 정액제 이용기간 만료 후 해지
        # - 중도(중도해지) - 해지 요청시 즉시 정지되고 팝빌 담당자가 승인시 해지
        # └ 중도일 경우, 정액제 잔여기간은 일할로 계산되어 포인트 환불(무료 이용기간에 해지하면 전액 환불)
        CloseType = "중도"

        response = easyFinBankService.closeBankAccount(CorpNum, BankCode, AccountNumber, CloseType)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def revokeCloseBankAccount(request):
    """
    신청한 정액제 해지요청을 취소합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#RevokeCloseBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # 계좌번호 하이픈('-') 제외
        AccountNumber = ""

        response = easyFinBankService.revokeCloseBankAccount(CorpNum, BankCode, AccountNumber)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def deleteBankAccount(request):
    """
    종량제 이용시 등록된 계좌를 삭제합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/manage#DeleteBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # 계좌번호 하이픈('-') 제외
        AccountNumber = ""

        response = easyFinBankService.deleteBankAccount(CorpNum, BankCode, AccountNumber)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def requestJob(request):
    """
    계좌 거래내역을 확인하기 위해 팝빌에 수집요청을 합니다. (조회기간 단위 : 최대 1개월)
    - 조회일로부터 최대 3개월 이전 내역까지 조회할 수 있습니다.
    - 반환 받은 작업아이디는 함수 호출 시점부터 1시간 동안 유효합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/job#RequestJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        BankCode = ""

        # 계좌번호
        AccountNumber = ""

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        result = easyFinBankService.requestJob(CorpNum, BankCode, AccountNumber, SDate, EDate)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getJobState(request):
    """
    수집 요청(RequestJob API) 함수를 통해 반환 받은 작업 아이디의 상태를 확인합니다.
    - 거래 내역 조회(Search API) 함수 또는 거래 요약 정보 조회(Summary API) 함수를 사용하기 전에
    수집 작업의 진행 상태, 수집 작업의 성공 여부를 확인해야 합니다.
    - 작업 상태(jobState) = 3(완료)이고 수집 결과 코드(errorCode) = 1(수집성공)이면
    거래 내역 조회(Search) 또는 거래 요약 정보 조회(Summary) 를 해야합니다.
    - 작업 상태(jobState)가 3(완료)이지만 수집 결과 코드(errorCode)가 1(수집성공)이 아닌 경우에는
    오류메시지(errorReason)로 수집 실패에 대한 원인을 파악할 수 있습니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/job#GetJobState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob) 호출시 발급받은 작업아이디
        jobID = "022080515000000594"

        response = easyFinBankService.getJobState(CorpNum, jobID)

        return render(request, "EasyFinBank/GetJobState.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listActiveJob(request):
    """
    수집 요청(RequestJob API) 함수를 통해 반환 받은 작업아이디의 목록을 확인합니다.
    - 수집 요청 후 1시간이 경과한 수집 요청건은 상태정보가 반환되지 않습니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/job#ListActiveJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = easyFinBankService.listActiveJob(CorpNum)

        return render(request, "EasyFinBank/ListActiveJob.html", {"list": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    수집 상태 확인(getJobState API) 함수를 통해 상태 정보가 확인된 작업아이디를 활용하여 계좌 거래 내역을 조회합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/search#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "022080515000000594"

        # 거래유형 배열 ("I" 와 "O" 중 선택, 다중 선택 가능)
        # └ I = 입금 , O = 출금
        # - 미입력 시 전체조회
        TradeType = ["I", "O"]

        # "입·출금액" / "메모" / "비고" 중 검색하고자 하는 값 입력
        # - 메모 = 거래내역 메모저장(SaveMemo)을 사용하여 저장한 값
        # - 비고 = EasyFinBankSearchDetail의 remark1, remark2, remark3 값
        # - 미입력시 전체조회
        SearchString = ""

        # 페이지번호
        Page = 1

        # 페이지당 목록개수, 최대값 1000
        PerPage = 10

        # 정렬방향 [D-내림차순 / A-오름차순]
        Order = "D"

        response = easyFinBankService.search(CorpNum, JobID, TradeType, SearchString, Page, PerPage, Order)

        return render(request, "EasyFinBank/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def summary(request):
    """
    수집 상태 확인(GetJobState API) 함수를 통해 상태 정보가 확인된 작업아이디를 활용하여 계좌 거래내역의 요약 정보를 조회합니다.
    - 요약 정보 : 입·출 금액 합계, 입·출 거래 건수
    - https://developers.popbill.com/reference/easyfinbank/python/api/search#Summary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "022080515000000594"

        # 거래유형 배열 ("I" 와 "O" 중 선택, 다중 선택 가능)
        # └ I = 입금 , O = 출금
        # - 미입력 시 전체조회
        TradeType = ["I", "O"]

        # "입·출금액" / "메모" / "비고" 중 검색하고자 하는 값 입력
        # - 메모 = 거래내역 메모저장(SaveMemo)을 사용하여 저장한 값
        # - 비고 = EasyFinBankSearchDetail의 remark1, remark2, remark3 값
        # - 미입력시 전체조회
        SearchString = ""

        response = easyFinBankService.summary(CorpNum, JobID, TradeType, SearchString)

        return render(request, "EasyFinBank/Summary.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def saveMemo(request):
    """
    한 건의 거래 내역에 메모를 저장합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/search#SaveMemo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 거래내역 아이디, Search API 거래내역의 tid 항목
        TID = "02208051200000000120220804000001"

        # 메모
        Memo = "saveMemo TEST"

        response = easyFinBankService.saveMemo(CorpNum, TID, Memo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFlatRatePopUpURL(request):
    """
    정액제 서비스 신청 팝업 URL을 반환 합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetFlatRatePopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getFlatRatePopUpURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFlatRateState(request):
    """
    계좌조회 정액제 서비스 상태를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetFlatRateState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 기관코드
        BankCode = ""

        # 계좌번호
        AccountNumber = ""

        flatRateState = easyFinBankService.getFlatRateState(CorpNum, BankCode, AccountNumber)

        return render(request,"EasyFinBank/GetFlatRateState.html",{"flatRateState": flatRateState})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = easyFinBankService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = easyFinBankService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = easyFinBankService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 계좌조회 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = easyFinBankService.getChargeInfo(CorpNum)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#PaymentRequest
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

        response = easyFinBankService.paymentRequest(CorpNum,paymentForm, UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetPaymentHistory
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

        response = easyFinBankService.getPaymentHistory(CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetUseHistory
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

        response = easyFinBankService.getUseHistory(CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#Refund
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 환불신청 객체정보
        refundForm = RefundForm(
            # 담당자명
            ContactName="환불신청테스트",

            # 담당자 연락처
            TEL="01077777777",

            # 환불 신청 포인트
            RequestPoint="10",

            # 은행명
            AccountBank="국민",

            # 계좌번호
            AccountNum="123123123-123",

            # 예금주명
            AccountName="예금주",

            # 환불사유
            Reason="테스트 환불 사유",
        )

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response =  easyFinBankService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message, "refundCode": response.refundCode})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetRefundHistory
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

        response = easyFinBankService.getRefundHistory(CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = easyFinBankService.checkIsMember(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = easyFinBankService.checkID(memberID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#JoinMember
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

        response = easyFinBankService.joinMember(newMember)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = easyFinBankService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#UpdateCorpInfo
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

        response = easyFinBankService.updateCorpInfo(CorpNum, corpInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#RegistContact
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

        response = easyFinBankService.registContact(CorpNum, newContact)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = easyFinBankService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = easyFinBankService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#UpdateContact
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

        response = easyFinBankService.updateContact(CorpNum, updateInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def quitMember(request):
    """
    가입된 연동회원의 탈퇴를 요청합니다.
    - 회원탈퇴 신청과 동시에 팝빌의 모든 서비스 이용이 불가하며, 관리자를 포함한 모든 담당자 계정도 일괄탈퇴 됩니다.
    - 회원탈퇴로 삭제된 데이터는 복원이 불가능합니다.
    - 관리자 계정만 사용 가능합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/member#QuitMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum
        # 탈퇴 사유
        QuitReason = "테스트 탈퇴 사유"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.quitMember(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundInfo(request):
    """
    포인트 환불에 대한 상세정보 1건을 확인합니다.
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetRefundInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 환불코드
        RefundCode = "023040000017"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.getRefundInfo(CorpNum,RefundCode,UserID)
        return render(request, 'getRefundInfo.html', {"code": response.code, "response": response})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundableBalance(request):
    """
    환불 가능한 포인트를 확인합니다. (보너스 포인트는 환불가능포인트에서 제외됩니다.)
    - https://developers.popbill.com/reference/easyfinbank/python/api/point#GetRefundableBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        refundableBalance = easyFinBankService.getRefundableBalance(CorpNum, UserID)
        return render(request, 'getRefundableBalance.html', {"refundableBalance": refundableBalance})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})