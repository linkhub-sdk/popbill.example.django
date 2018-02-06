# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import ClosedownService, PopbillException, JoinForm, ContactInfo, CorpInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 ClosedownService 객체 생성
closedownService = ClosedownService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
closedownService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Closedown/Index.html', {})


def checkCorpNum(request):
    """
    1건의 휴폐업 정보를 조회합니다.
    - 휴폐업조회 항목별 정보는 "[휴폐업조회 AI 연동매뉴얼] > 4.1. 응답전문
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인하고자 하는 사업자번호
        corpNum = "6798700433"

        corpState = closedownService.checkCorpNum(CorpNum, corpNum)

        return render(request, 'Closedown/CheckCorpNum.html', {'corpState': corpState})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkCorpNums(request):
    """
    다수의 휴폐업 정보를 조회합니다. (최대 1000건)
    - 휴폐업조회 항목별 정보는 "[휴폐업조회 AI 연동매뉴얼] > 4.1. 응답전문
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인하고자 하는 사업자번호
        corpNumList = ["4108600477", "1234567890", "8888888888", "4352343543"]

        corpStateList = closedownService.checkCorpNums(CorpNum, corpNumList)

        return render(request, 'Closedown/CheckCorpNums.html', {'corpStateList': corpStateList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopbillURL_CHRG(request):
    """
    팝빌 관련 팝업 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-연동회원 포인트충전
        TOGO = "CHRG"

        url = closedownService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 휴폐업조회 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = closedownService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    휴폐업조회 전송단가를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = closedownService.getUnitCost(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = closedownService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를 이용하시기 바랍니다.
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
    파트너 포인트 충전 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
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


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = closedownService.checkIsMember(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    팝빌 회원아이디 중복여부를 확인합니다.
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
    파트너의 연동회원으로 회원가입을 요청합니다.
    아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    """
    try:
        # 회원정보
        newMember = JoinForm(

            # 회원아이디, 최대 20자
            ID="testkorea",

            # 비밀번호, 최대 20자
            PWD="this_is_password",

            # 사업자번호
            CorpNum="1234567890",

            # 상호
            CorpName="테스트가입상호",

            # 대표자성명
            CEOName="테스트대표자성명",

            # 주소
            Addr="테스트 회사 주소",

            # 업태
            BizType="테스트업태",

            # 종목
            BizClass="테스트업종",

            # 담당자 성명
            ContactName="담당자성명",

            # 담당자 연락처
            ContactTEL="070-4304-2991",

            # 담당자 휴대폰번호
            ContactHP="010-2222-3333",

            # 담당자 팩스번호
            ContactFAX="070-4304-2991",

            # 담당자 메일주소
            ContactEmail="test@test.com"
        )

        response = closedownService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = closedownService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html',
                      {'ceoname': response.ceoname, 'corpName': response.corpName,
                       'addr': response.addr, 'bizType': response.bizType,
                       'bizClass': response.bizClass})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 회사정보
        corpInfo = CorpInfo(

            # 대표자성명
            ceoname="대표자성명",

            # 상호
            corpName="상호",

            # 주소
            addr="주소",

            # 업태
            bizType="업태",

            # 종목
            bizClass="종목"
        )

        response = closedownService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registContact(request):
    """
    연동회원의 담당자를 신규로 등록합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 담당자 정보
        newContact = ContactInfo(

            # 아이디
            id="testkorea_1117",

            # 비밀번호
            pwd="this_is_password",

            # 담당자명
            personName="정대리",

            # 연락처
            tel="010-4304-2991",

            # 휴대폰번호
            hp="010-4304-2991",

            # 팩스번호
            fax="070-4324-2991",

            # 메일주소
            email="dev@linkhub.co.kr",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True
        )

        response = closedownService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    """
    연동회원의 담당자 목록을 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        listContact = closedownService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
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

            # 담당자 성명
            personName="담당자 성명",

            # 연락처
            tel="070-4304-2991",

            # 휴대폰번호
            hp="010-4324-4324",

            # 팩스번호
            fax="070-111-222",

            # 메일주소
            email="dev@linkhub.co.kr",

            # 회사조회 여부, True-회사조회, False-개인조회
            searchAllAllowYN=True
        )

        response = closedownService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopbillURL_LOGIN(request):
    """
    팝빌 관련 팝업 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-연동회원 포인트충전
        TOGO = "LOGIN"

        url = closedownService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
