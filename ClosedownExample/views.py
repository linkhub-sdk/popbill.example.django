# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import ClosedownService, PopbillException, JoinForm, ContactInfo, CorpInfo, RefundForm

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 ClosedownService 객체 생성
closedownService = ClosedownService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
closedownService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
closedownService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
closedownService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
closedownService.UseLocalTimeYN = settings.UseLocalTimeYN

def index(request):
    return render(request, 'Closedown/Index.html', {})


def checkCorpNum(request):
    """
    사업자번호 1건에 대한 휴폐업정보를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/check#CheckCorpNum
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 조회 사업자번호
        targetCorpNum = "6798700433"

        corpState = closedownService.checkCorpNum(CorpNum, targetCorpNum)

        return render(request, 'Closedown/CheckCorpNum.html', {'corpState': corpState})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkCorpNums(request):
    """
    다수건의 사업자번호에 대한 휴폐업정보를 확인합니다. (최대 1,000건)
    - https://developers.popbill.com/reference/closedown/python/api/check#CheckCorpNums
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인하고자 하는 사업자번호 (최대 1000건)
        targetCorpNumList = ["1231212312", "1234567890", "6798700433"]

        corpStateList = closedownService.checkCorpNums(CorpNum, targetCorpNumList)

        return render(request, 'Closedown/CheckCorpNums.html', {'corpStateList': corpStateList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = closedownService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = closedownService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = closedownService.getPaymentURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = closedownService.getUseHistoryURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = closedownService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = closedownService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUnitCost(request):
    """
    휴폐업 조회시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        result = closedownService.getUnitCost(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeInfo(request):
    """
    팝빌 휴폐업조회 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = closedownService.getChargeInfo(CorpNum)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = closedownService.checkIsMember(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def paymentRequest(request):
    """
        연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
        - https://developers.popbill.com/reference/closedown/python/api/point#PaymentRequest
    """
    try:
        CorpNum = settings.testCorpNum
        UserID = settings.testUserID
        response = closedownService.paymentRequest(CorpNum, UserID)
        return render(request, 'paymentResponse.html', {'response':response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})

def getSettleResult(request):
    """
        연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
        - https://developers.popbill.com/reference/closedown/python/api/point#GetSettleResult
    """
    try:
        CorpNum = settings.testCorpNum
        UserID = settings.testUserID
        response = closedownService.getSettleResult(CorpNum, UserID)

        return render(request, 'paymentHistory.html', {'response':response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})

def getPaymentHistory(request):
    """
        연동회원의 포인트 결제내역을 확인합니다.
        - https://developers.popbill.com/reference/closedown/python/api/point#GetPaymentHistory
    """
    try:
        CorpNum = settings.testCorpNum
        SDate	= "20230101"
        EDate =	"20230110"
        Page	= 1
        PerPage	= 500
        UserID = settings.testUserID

        response = closedownService.getPaymentHistory(CorpNum, SDate,EDate,Page,PerPage, UserID)
        return render(request, 'paymentHistoryResult.html', {'response':response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})

def getUseHistory(request):
    """
        연동회원의 포인트 사용내역을 확인합니다.
        - https://developers.popbill.com/reference/closedown/python/api/point#GetUseHistory
    """
    try:
        CorpNum = settings.testCorpNum
        SDate	= "20230101"
        EDate =	"20230110"
        Page	= 1
        PerPage	= 500
        Order	= "D"
        UserID = settings.testUserID
        response =        CorpNum = settings.testCorpNum
        UserID = settings.testUserID
        response = closedownService.getUseHistory(CorpNum,SDate,EDate,Page,PerPage,Order, UserID)
        return render(request, 'useHistoryResult.html', {'response':response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})

def refund(request):
    """
        연동회원 포인트를 환불 신청합니다.
        - https://developers.popbill.com/reference/closedown/python/api/point#Refund
    """
    try:
        CorpNum = settings.testCorpNum
        refundForm = RefundForm(
            contactname="환불신청테스트",
            tel="01077777777",
            requestpoint="10",
            accountbank="국민",
            accountnum="123123123-123",
            accountname="예금주",
            reason="테스트 환불 사유",
        )
        UserID = settings.testUserID
        response = closedownService.refund(CorpNum, refundForm, UserID)
        return render(request, 'response.html', {'response':response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})

def getRefundHistory(request):
    """
        연동회원의 포인트 환불신청내역을 확인합니다.
        - - https://developers.popbill.com/reference/closedown/python/api/point#GetRefundHistory
    """
    try:
        CorpNum = settings.testCorpNum
        Page = 1
        PerPage = 500
        UserID = settings.testUserID

        response = closedownService.getRefundHistory(CorpNum, Page, PerPage, UserID)
        return render(request, 'refundHistoryResult.html', {'response':response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code':PE.code, 'message':PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = closedownService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#JoinMember
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
            ContactTEL=""
        )

        response = closedownService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = closedownService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = closedownService.getCorpInfo(CorpNum)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#UpdateCorpInfo
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
            bizClass="종목"
        )

        response = closedownService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#RegistContact
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

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = closedownService.registContact(CorpNum, newContact)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = closedownService.getContactInfo(CorpNum, contactID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = closedownService.listContact(CorpNum)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/closedown/python/api/member#UpdateContact
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

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = closedownService.updateContact(CorpNum, updateInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})