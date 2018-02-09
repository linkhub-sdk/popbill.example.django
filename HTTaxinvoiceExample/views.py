# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import HTTaxinvoiceService, PopbillException, JoinForm, CorpInfo, ContactInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 HTTaxinvoiceService 객체 생성
htTaxinvoiceService = HTTaxinvoiceService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
htTaxinvoiceService.IsTest = settings.IsTest


def index(request):
    return render(request, 'HTTaxinvoice/Index.html', {})


def requestJob(request):
    """
    전자(세금)계산서 매출/매입 내역 수집을 요청합니다
    - 매출/매입 연계 프로세스는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 1.API소개 (프로세스 흐름도)" 를 참고하시기 바랍니다.
    - 수집 요청후 반환받은 작업아이디(JobID)의 유효시간은 1시간 입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자세금계산서  발행유형, [SELL-매출 / BUY-매입 / TRUSTEE-위수탁]
        Type = "SELL"

        # 일자유형, [W-작성일자 / I-발행일자 / S-전송일자]
        DType = "W"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20171201"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20180131"

        result = htTaxinvoiceService.requestJob(CorpNum, Type, DType, SDate, EDate, UserID)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getJobState(request):
    """
    수집 요청 상태를 확인합니다.
    - 응답항목 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼
      > 3.1.2. GetJobState(수집 상태 확인)" 을 참고하시기 바랍니다 .
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob) 호출시 발급받은 작업아이디
        jobID = "018020810000000001"

        response = htTaxinvoiceService.getJobState(CorpNum, jobID, UserID)

        return render(request, 'HTTaxinvoice/GetJobState.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listActiveJob(request):
    """
    수집 요청건들에 대한 상태 목록을 확인합니다.
    - 수집 요청 작업아이디(JobID)의 유효시간은 1시간 입니다.
    - 응답항목에 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 3.1.3. ListActiveJob (수집 상태 목록 확인)" 을 참고하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        list = htTaxinvoiceService.listActiveJob(CorpNum, UserID)

        return render(request, 'HTTaxinvoice/ListActiveJob.html', {'list': list})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 수집결과를 조회합니다.
    - 응답항목에 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 3.2.1. Search (수집 결과 조회)" 을 참고하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "018020810000000001"

        # 문서형태 배열, [N-일반전자세금계산서 / M-수정전자세금계산서]
        Type = ["N", "M"]

        # 과세형태 배열, [T-과세 / N-면세 / Z-영세]
        TaxType = ["T", "N", "Z"]

        # 영수/청구, [R-영수 / C-청구 / N-없음]
        PurposeType = ["R", "C", "N"]

        # 종사업자번호 사업자 유형, [S-공급자 / B-공급받는자 / T-수탁자]
        TaxRegIDType = "S"

        # 종사업장번호 유무, [공백-전체조회 / 0-종사업장번호 없음 / 1-종사업장번호 있음]
        TaxRegIDYN = ""

        # 종사업장번호, 콤마(",")로 구분하여 구성 ex) "0001", "0007"
        TaxRegID = ""

        # 페이지번호
        Page = 1

        # 페이지당 목록개수, 최대값 1000
        PerPage = 10

        # 정렬방향 [D-내림차순 / A-오름차순]
        Order = "D"

        response = htTaxinvoiceService.search(CorpNum, JobID, Type, TaxType, PurposeType,
                                              TaxRegIDType, TaxRegIDYN, TaxRegID, Page, PerPage, Order, UserID)

        return render(request, 'HTTaxinvoice/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def summary(request):
    """
    검색조건을 사용하여 수집 결과 요약정보를 조회합니다.
    - 응답항목에 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 3.2.2. Summary (수집 결과 요약정보 조회)" 을 참고하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집 요청(requestJob)시 발급받은 작업아이디
        JobID = "018020811000000001"

        # 문서형태 배열, [N-일반전자세금계산서 / M-수정전자세금계산서]
        Type = ["N", "M"]

        # 과세형태, [T-과세 / N-면세 / Z-영세]
        TaxType = ["T", "N", "Z"]

        # 영수/청구, [R-영수 / C-청구 / N-없음]
        PurposeType = ["R", "C", "N"]

        # 종사업장번호 사업자유형, [S-공급자 / B-공급받는자 / T-수탁자]
        TaxRegIDType = "S"

        # 종사업장번호 유무, [공백-전체조회 / 0-종사업장번호 없음 / 1-종사업장번호 있음]
        TaxRegIDYN = ""

        # 종사업장번호, 콤마(",")로 구분하여 구성 Ex) "0001,0007"
        TaxRegID = ""

        response = htTaxinvoiceService.summary(CorpNum, JobID, Type, TaxType, PurposeType,
                                               TaxRegIDType, TaxRegIDYN, TaxRegID, UserID)

        return render(request, 'HTTaxinvoice/Summary.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getTaxinvoice(request):
    """
    수집된 전자(세금)계산서 1건의 상세정보를 확인합니다.
    - 응답항목에 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 4.2.2. GetTaxinvoice 응답전문 구성" 을 참고하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자세금계산서 국세청승인번호
        NTSConfirmNum = "20161121410002030000079e"

        taxinvoice = htTaxinvoiceService.getTaxinvoice(CorpNum, NTSConfirmNum, UserID)

        return render(request, 'HTTaxinvoice/GetTaxinvoice.html', {'taxinvoice': taxinvoice})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getXML(request):
    """
    XML형식의 전자(세금)계산서 상세정보를 1건을 확인합니다.
    - 응답항목에 관한 정보는 "[홈택스 전자(세금)계산서 연계 API 연동매뉴얼]
      > 3.2.4. GetXML (상세정보 확인 - XML)" 을 참고하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자세금계산서 국세청승인번호
        NTSConfirmNum = "20161121410002030000079e"

        response = htTaxinvoiceService.getXML(CorpNum, NTSConfirmNum, UserID)

        return render(request, 'HTTaxinvoice/GetXML.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCertificatePopUpURL(request):
    """
    팝빌에 로그인 하지 않고 홈택스 공인인증서를 등록할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 의해 응답된 URL은 30초의 만료시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        url = htTaxinvoiceService.getCertificatePopUpURL(CorpNum)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCertificateExpireDate(request):
    """
    팝빌에 등록되어 있는 홈택스 공인인증서의 만료일시를 확인합니다.
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        expiredate = htTaxinvoiceService.getCertificateExpireDate(CorpNum, UserID)

        return render(request, 'HTTaxinvoice/GetCertificateExpireDate.html', {'expiredate': expiredate})
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

        result = htTaxinvoiceService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
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

        url = htTaxinvoiceService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
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

        result = htTaxinvoiceService.getPartnerBalance(CorpNum)

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

        url = htTaxinvoiceService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 현금영수증 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = htTaxinvoiceService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFlatRatePopUpURL(request):
    """
    정액제 신청 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        url = htTaxinvoiceService.getFlatRatePopUpURL(CorpNum)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFlatRateState(request):
    """
    연동회원의 정액제 서비스 이용상태를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        flatRateState = htTaxinvoiceService.getFlatRateState(CorpNum, UserID)

        return render(request, 'HTTaxinvoice/GetFlatRateState.html', {'flatRateState': flatRateState})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.checkIsMember(CorpNum)

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

        response = htTaxinvoiceService.checkID(memberID)

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

        response = htTaxinvoiceService.joinMember(newMember)

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

        url = htTaxinvoiceService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
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

        response = htTaxinvoiceService.registContact(CorpNum, newContact, UserID)

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

        listContact = htTaxinvoiceService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
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

        response = htTaxinvoiceService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

        response = htTaxinvoiceService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html',
                      {'ceoname': response.ceoname, 'corpName': response.corpName,
                       'addr': response.addr, 'bizType': response.bizType,
                       'bizClass': response.bizClass})
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

        response = htTaxinvoiceService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
