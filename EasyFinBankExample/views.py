# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from popbill import EasyFinBankService, PopbillException, ContactInfo, JoinForm, CorpInfo, BankAccountInfo

from config import settings


# config/settings.py 작성한 LinkID, SecretKey를 이용해 계좌조회 서비스 객체 생성
easyFinBankService = EasyFinBankService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
easyFinBankService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
easyFinBankService.IPRestrictOnOff = settings.IPRestrictOnOff

def index(request):
    return render(request, 'EasyFinBank/Index.html', {})


def registBankAccount(request):
    """
    팝빌에 계좌정보를 등록합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        infoObj = BankAccountInfo(

            # [필수] 은행코드
            # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
            # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
            # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
            BankCode="",

            # [필수] 계좌번호 하이픈('-') 제외
            AccountNumber="",

            # [필수] 계좌비밀번호
            AccountPWD="",

            # [필수] 계좌유형, "법인" 또는 "개인" 입력
            AccountType="",

            # [필수] 예금주 식별정보 (‘-‘ 제외)
            # 계좌유형이 “법인”인 경우 : 사업자번호(10자리)
            # 계좌유형이 “개인”인 경우 : 예금주 생년월일 (6자리-YYMMDD)
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

        response = easyFinBankService.registBankAccount(CorpNum, infoObj, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateBankAccount(request):
    """
    팝빌에 등록된 계좌정보를 수정합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        infoObj = BankAccountInfo(
            # [필수] 은행코드
            # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
            # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
            # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
            BankCode="",

            # [필수] 계좌번호 하이픈('-') 제외
            AccountNumber="",

            # [필수] 계좌비밀번호
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

        response = easyFinBankService.updateBankAccount(CorpNum, infoObj, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getBankAccountInfo(request):
    """
    계좌 상세정보를 확인합니다.
    """
    try:

        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 은행코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = "";

        # 계좌번호
        AccountNumber = "";

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.getBankAccountInfo(CorpNum, BankCode, AccountNumber, UserID)

        return render(request, 'EasyFinBank/getBankAccountInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def closeBankAccount(request):
    """
    팝빌에 등록된 은행계좌의 정액제 해지를 요청한다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 은행코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # [필수] 계좌번호 하이픈('-') 제외
        AccountNumber = ""

        # 해지유형, "일반", "중도" 중 선택기재
        # 일반해지 - 이용중인 정액제 사용기간까지 이용후 정지
        # 중도해지 - 요청일 기준으로 정지, 정액제 잔여기간은 일할로 계산되어 포인트 환불
        CloseType = "중도"

        response = easyFinBankService.closeBankAccount(CorpNum, BankCode, AccountNumber, CloseType, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def revokeCloseBankAccount(request):
    """
    정액제 해지신청을 취소한다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 은행코드
        # 산업은행-0002 / 기업은행-0003 / 국민은행-0004 /수협은행-0007 / 농협은행-0011 / 우리은행-0020
        # SC은행-0023 / 대구은행-0031 / 부산은행-0032 / 광주은행-0034 / 제주은행-0035 / 전북은행-0037
        # 경남은행-0039 / 새마을금고-0045 / 신협은행-0048 / 우체국-0071 / KEB하나은행-0081 / 신한은행-0088 /씨티은행-0027
        BankCode = ""

        # [필수] 계좌번호 하이픈('-') 제외
        AccountNumber = ""

        response = easyFinBankService.revokeCloseBankAccount(CorpNum, BankCode, AccountNumber, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getBankAccountMgtURL(request):
    """
    계좌 관리 팝업 URL을 반환 합니다.
    - 보안정책에 의해 응답된 URL은 30초의 만료시간을 갖습니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetBankAccountMgtURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        url = easyFinBankService.getBankAccountMgtURL(CorpNum)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listBankAccount(request):
    """
    팝빌에 등록된 계좌 목록을 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#ListBankAccount
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        bankAccountList = easyFinBankService.listBankAccount(CorpNum)

        return render(request, 'EasyFinBank/ListBankAccount.html', {'list': bankAccountList})

    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def requestJob(request):
    """
    계좌 거래내역 수집을 요청합니다
    - https://docs.popbill.com/easyfinbank/python/api#RequestJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 은행코드
        BankCode = "0048"

        # 계좌번호
        AccountNumber = "131020538645"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20191005"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20200103"

        result = easyFinBankService.requestJob(CorpNum, BankCode, AccountNumber,SDate, EDate, UserID)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getJobState(request):
    """
    수집 요청 상태를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetJobState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob) 호출시 발급받은 작업아이디
        jobID = "020010314000000028"

        response = easyFinBankService.getJobState(CorpNum, jobID, UserID)

        return render(request, 'EasyFinBank/GetJobState.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listActiveJob(request):
    """
    수집 요청 목록을 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#ListActiveJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.listActiveJob(CorpNum, UserID)

        return render(request, 'EasyFinBank/ListActiveJob.html', {'list': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    거래내역의 수집 결과를 조회합니다.
    - https://docs.popbill.com/easyfinbank/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "020010314000000035"

        # 거래유형 배열, [I-입금 / O-출금]
        TradeType = ["I", "O"]

        # 조회 검색어, 입금/출금액, 메모, 적요 like 검색
        SearchString = ""

        # 페이지번호
        Page = 1

        # 페이지당 목록개수, 최대값 1000
        PerPage = 10

        # 정렬방향 [D-내림차순 / A-오름차순]
        Order = "D"

        response = easyFinBankService.search(CorpNum, JobID, TradeType, SearchString,
            Page, PerPage, Order, UserID)

        return render(request, 'EasyFinBank/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def summary(request):
    """
    검색조건을 사용하여 수집 결과 요약정보를 조회합니다.
    - https://docs.popbill.com/easyfinbank/python/api#Summary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "020010314000000035"

        # 거래유형 배열, [I-입금 / O-출금]
        TradeType = ["I", "O"]

        # 조회 검색어, 입금/출금액, 메모, 적요 like 검색
        SearchString = ""

        response = easyFinBankService.summary(CorpNum, JobID, TradeType, SearchString, UserID)

        return render(request, 'EasyFinBank/Summary.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def saveMemo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://docs.popbill.com/easyfinbank/python/api#SaveMemo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 거래내역 아이디, Search API 거래내역의 tid 항목
        TID = "01912181100000000120191231000001"

        # 메모
        Memo = "memo"

        response = easyFinBankService.saveMemo(CorpNum, TID, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getFlatRatePopUpURL(request):
    """
    정액제 서비스 신청 팝업 URL을 반환 합니다.
    - 보안정책에 의해 응답된 URL은 30초의 만료시간을 갖습니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetFlatRatePopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        url = easyFinBankService.getFlatRatePopUpURL(CorpNum)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getFlatRateState(request):
    """
    연동회원의 정액제 서비스 이용상태를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetFlatRateState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 은행코드
        BankCode = "0048"

        # 계좌번호
        AccountNumber = "131020538645"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        flatRateState = easyFinBankService.getFlatRateState(CorpNum, BankCode, AccountNumber, UserID)

        return render(request, 'EasyFinBank/GetFlatRateState.html', {'flatRateState': flatRateState})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = easyFinBankService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeURL(request):
    """
    팝빌 연동회원 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를 이용하시기 바랍니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = easyFinBankService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = easyFinBankService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 홈택스연동 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = easyFinBankService.checkIsMember(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    팝빌 회원아이디 중복여부를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = easyFinBankService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    파트너의 연동회원으로 회원가입을 요청합니다.
    - 아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    - https://docs.popbill.com/easyfinbank/python/api#JoinMember
    """
    try:
        # 회원정보
        newMember = JoinForm(

            # 아이디 (6자 이상 50자 미만)
            ID="join_id_test",

            # 비밀번호 (6자 이상 20자 미만)
            PWD="this_is_password",

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
            ContactEmail="test@test.com",

            # 담당자 연락처 (최대 20자)
            ContactTEL="070-111-222",

            # 담당자 휴대폰번호 (최대 20자)
            ContactHP="010-111-222",

            # 담당자 팩스번호 (최대 20자)
            ContactFAX="070-111-222"
        )

        response = easyFinBankService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = easyFinBankService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registContact(request):
    """
    연동회원의 담당자를 신규로 등록합니다.
    - https://docs.popbill.com/easyfinbank/python/api#RegistContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 담당자 정보
        newContact = ContactInfo(

            # 아이디 (6자 이상 50자 미만)
            id="popbill_test_id",

            # 비밀번호 (6자 이상 20자 미만)
            pwd="popbill_test_pwd",

            # 담당자명 (최대 100자)
            personName="담당자명",

            # 담당자 연락처 (최대 20자)
            tel="010-111-222",

            # 담당자 휴대폰번호 (최대 20자)
            hp="010-111-222",

            # 담당자 팩스번호 (최대 20자)
            fax="070-111-222",

            # 담당자 이메일 (최대 100자)
            email="test@test.com",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
        )

        response = easyFinBankService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    """
    연동회원의 담당자 목록을 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        listContact = easyFinBankService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://docs.popbill.com/easyfinbank/python/api#UpdateCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

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
            bizClass="종목"
        )

        response = easyFinBankService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/easyfinbank/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = easyFinBankService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/easyfinbank/python/api#UpdateContact
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
            tel="010-111-111",

            # 담당자 휴대폰번호 (최대 20자)
            hp="010-111-111",

            # 담당자 팩스번호 (최대 20자)
            fax="070-111-222",

            # 담당자 메일주소 (최대 100자)
            email="test@test.com",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
        )

        response = easyFinBankService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
