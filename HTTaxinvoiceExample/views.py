# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import HTTaxinvoiceService, PopbillException, JoinForm, CorpInfo, ContactInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 HTTaxinvoiceService 객체 생성
htTaxinvoiceService = HTTaxinvoiceService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
htTaxinvoiceService.IsTest = settings.IsTest


# 홈택스 연동서비스를 이용하기 위해 인증 처리를 합니다. (인증방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌로그인 > [홈택스연동] > [환경설정] > [인증 관리] 메뉴에서 홈택스 인증 처리를 합니다.
# 2. 홈택스연동 인증 관리 팝업 URL(GetCertificatePopUpURL API) 반환된 URL을 이용하여 홈택스 인증 처리를 합니다.

def index(request):
    return render(request, 'HTTaxinvoice/Index.html', {})


def requestJob(request):
    """
    전자(세금)계산서 매출/매입 내역 수집을 요청합니다
    - 홈택스연동 프로세스는 "[홈택스연동(전자세금계산서계산서) API 연동매뉴얼] >
      1.1. 홈택스연동(전자세금계산서) API 구성" 을 참고하시기 바랍니다.
    - 수집 요청후 반환받은 작업아이디(JobID)의 유효시간은 1시간 입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자세금계산서  발행유형 [SELL-매출 / BUY-매입 / TRUSTEE-위수탁]
        Type = "SELL"

        # 일자유형, [W-작성일자 / I-발행일자 / S-전송일자]
        DType = "W"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20190101"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20190116"

        result = htTaxinvoiceService.requestJob(CorpNum, Type, DType, SDate, EDate, UserID)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getJobState(request):
    """
    수집 요청 상태를 확인합니다.
    - 응답항목 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      3.1.2. GetJobState(수집 상태 확인)" 을 참고하시기 바랍니다.
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
    - 응답항목에 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      3.1.3. ListActiveJob(수집 상태 목록 확인)" 을 참고하시기 바랍니다.
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
    전자세금계산서 매입/매출 내역의 수집 결과를 조회합니다.
    - 응답항목에 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      3.2.1. Search(수집 결과 조회)" 을 참고하시기 바랍니다.
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
    - 응답항목에 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      3.2.2. Summary(수집 결과 요약정보 조회)" 을 참고하시기 바랍니다.
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
    전자세금계산서 1건의 상세정보를 확인합니다.
    - 응답항목에 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      4.1.2. GetTaxinvoice 응답전문 구성" 을 참고하시기 바랍니다.
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
    XML 형식의 전자세금계산서 상세정보를 확인합니다.
    - 응답항목에 관한 정보는 "[홈택스연동 (전자세금계산서계산서) API 연동매뉴얼] >
      3.2.4. GetXML(상세정보 확인 - XML)" 을 참고하시기 바랍니다.
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


def getPopUpURL(request):
    """
    홈택스 전자세금계산서 보기 팝업 URL을 반환 합니다.
    - 보안정책에 의해 응답된 URL은 30초의 만료시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        url = htTaxinvoiceService.getPopUpURL(CorpNum)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCertificatePopUpURL(request):
    """
    홈택스연동 인증관리를 위한 URL을 반환합니다.
    - 인증방식에는 부서사용자/공인인증서 인증 방식이 있습니다.
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


def checkCertValidation(request):
    """
    팝빌에 등록된 공인인증서의 홈택스 로그인을 테스트합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.checkCertValidation(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registDeptUser(request):
    """
    홈택스 전자세금계산서 부서사용자 계정을 등록합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 홈택스 부서사용자 계정아이디
        DeptUserID = "deptuserid"

        # 홈택스 부서사용자 계정비밀번호
        DeptUserPWD = "deptuserpwd"

        response = htTaxinvoiceService.registDeptUser(CorpNum, DeptUserID, DeptUserPWD)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkDeptUser(request):
    """
    팝빌에 등록된 전자세금계산서 부서사용자 아이디를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.checkDeptUser(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkLoginDeptUser(request):
    """
    팝빌에 등록된 전자세금계산서 부서사용자 계정정보를 이용하여 홈택스 로그인을 테스트합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.checkLoginDeptUser(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def deleteDeptUser(request):
    """
    팝빌에 등록된 전자세금계산서 부서사용자 계정정보를 삭제합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.deleteDeptUser(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
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


def getChargeURL(request):
    """
    팝빌 연동회원 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htTaxinvoiceService.getChargeURL(CorpNum, UserID)

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
    연동회원의 홈택스연동 API 서비스 과금정보를 확인합니다.
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

        response = htTaxinvoiceService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htTaxinvoiceService.getAccessURL(CorpNum, UserID)

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

        response = htTaxinvoiceService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
