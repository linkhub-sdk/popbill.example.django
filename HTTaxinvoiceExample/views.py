# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import HTTaxinvoiceService, PopbillException, JoinForm, CorpInfo, ContactInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 HTTaxinvoiceService 객체 생성
htTaxinvoiceService = HTTaxinvoiceService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
htTaxinvoiceService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
htTaxinvoiceService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
htTaxinvoiceService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
htTaxinvoiceService.UseLocalTimeYN = settings.UseLocalTimeYN

# 홈택스 연동서비스를 이용하기 위해 팝빌에 인증정보를 등록 합니다. (인증방법은 부서사용자 인증 / 인증서 인증 방식이 있습니다.)
# - 팝빌로그인 > [홈택스연동] > [환경설정] > [인증 관리] 메뉴에서 [홈택스 부서사용자 등록] 혹은
#   [홈택스 인증서 등록]을 통해 인증정보를 등록합니다.
# - 홈택스연동 인증 관리 팝업 URL(GetCertificatePopUpURL API) 반환된 URL에 접속 하여
#   [홈택스 부서사용자 등록] 혹은 [홈택스 인증서 등록]을 통해 인증정보를 등록합니다.

def index(request):
    return render(request, 'HTTaxinvoice/Index.html', {})

def requestJob(request):
    """
    홈택스에 신고된 전자세금계산서 매입/매출 내역 수집을 팝빌에 요청합니다. (조회기간 단위 : 최대 3개월)
    - 주기적으로 자체 DB에 세금계산서 정보를 INSERT 하는 경우, 조회할 일자 유형(DType) 값을 "S"로 하는 것을 권장합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#RequestJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자세금계산서  발행유형 [SELL-매출 / BUY-매입 / TRUSTEE-위수탁]
        Type = "SELL"

        # 일자유형, [W-작성일자 / I-발행일자 / S-전송일자]
        DType = "S"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        result = htTaxinvoiceService.requestJob(CorpNum, Type, DType, SDate, EDate)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getJobState(request):
    """
    수집 요청(RequestJob API) 함수를 통해 반환 받은 작업 아이디의 상태를 확인합니다.
    - 수집 결과 조회(Search API) 함수 또는 수집 결과 요약 정보 조회(Summary API) 함수를 사용하기 전에
    수집 작업의 진행 상태, 수집 작업의 성공 여부를 확인해야 합니다.
    - 작업 상태(jobState) = 3(완료)이고 수집 결과 코드(errorCode) = 1(수집성공)이면
    수집 결과 내역 조회(Search) 또는 수집 결과 요약 정보 조회(Summary) 를 해야합니다.
    - 작업 상태(jobState)가 3(완료)이지만 수집 결과 코드(errorCode)가 1(수집성공)이 아닌 경우에는
    오류메시지(errorReason)로 수집 실패에 대한 원인을 파악할 수 있습니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetJobState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob) 호출시 발급받은 작업아이디
        jobID = "019012311000000001"

        response = htTaxinvoiceService.getJobState(CorpNum, jobID, UserID)

        return render(request, 'HTTaxinvoice/GetJobState.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listActiveJob(request):
    """
    전자세금계산서 매입/매출 내역 수집요청에 대한 상태 목록을 확인합니다.
    - 수집 요청 후 1시간이 경과한 수집 요청건은 상태정보가 반환되지 않습니다.
    - https://docs.popbill.com/httaxinvoice/python/api#ListActiveJob
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        list = htTaxinvoiceService.listActiveJob(CorpNum)

        return render(request, 'HTTaxinvoice/ListActiveJob.html', {'list': list})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def search(request):
    """
    수집 상태 확인(GetJobState API) 함수를 통해 상태 정보 확인된 작업아이디를 활용하여 현금영수증 매입/매출 내역을 조회합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집요청(requestJob)시 발급받은 작업아이디
        JobID = "019103015000000002"

        # 문서형태 배열 ("N" 와 "M" 중 선택, 다중 선택 가능)
        # └ N = 일반 , M = 수정
        # - 미입력 시 전체조회
        Type = ["N", "M"]

        # 과세형태 배열 ("T" , "N" , "Z" 중 선택, 다중 선택 가능)
        # └ T = 과세, N = 면세, Z = 영세
        # - 미입력 시 전체조회
        TaxType = ["T", "N", "Z"]

        # 발행목적 배열 ("R" , "C", "N" 중 선택, 다중 선택 가능)
        # └ R = 영수, C = 청구, N = 없음
        # - 미입력 시 전체조회
        PurposeType = ["R", "C", "N"]

        # 종사업장번호 유무 (null , "0" , "1" 중 택 1)
        # - null = 전체 , 0 = 없음, 1 = 있음
        TaxRegIDYN = ""

        # 종사업장번호의 주체 ("S" , "B" , "T" 중 택 1)
        # └ S = 공급자 , B = 공급받는자 , T = 수탁자
        # - 미입력시 전체조회
        TaxRegIDType = "S"

        # 종사업장번호
        # 다수기재시 콤마(",")로 구분하여 구성 ex ) "0001,0002"
        # - 미입력시 전체조회
        TaxRegID = ""

        # 페이지번호
        Page = 1

        # 페이지당 목록개수, 최대값 1000
        PerPage = 10

        # 정렬방향 D-내림차순, A-오름차순
        Order = "D"

        # 거래처 상호 / 사업자번호 (사업자) / 주민등록번호 (개인) / "9999999999999" (외국인) 중 검색하고자 하는 정보 입력
        # - 사업자번호 / 주민등록번호는 하이픈('-')을 제외한 숫자만 입력
        # - 미입력시 전체조회
        SearchString = ""

        response = htTaxinvoiceService.search(CorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType,
            TaxRegIDYN, TaxRegID, Page, PerPage, Order, UserID, SearchString)

        return render(request, 'HTTaxinvoice/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def summary(request):
    """
    수집 상태 확인(GetJobState API) 함수를 통해 상태 정보가 확인된 작업아이디를 활용하여 수집된 현금영수증 매입/매출 내역의 요약 정보를 조회합니다.
    - 요약 정보 : 현금영수증 수집 건수, 공급가액 합계, 세액 합계, 봉사료 합계, 합계 금액
    - https://docs.popbill.com/httaxinvoice/python/api#Summary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수집 요청(requestJob)시 발급받은 작업아이디
        JobID = "019103015000000002"

        # 문서형태 배열 ("N" 와 "M" 중 선택, 다중 선택 가능)
        # └ N = 일반 , M = 수정
        # - 미입력 시 전체조회
        Type = ["N", "M"]

        # 과세형태 배열 ("T" , "N" , "Z" 중 선택, 다중 선택 가능)
        # └ T = 과세, N = 면세, Z = 영세
        # - 미입력 시 전체조회
        TaxType = ["T", "N", "Z"]

        # 발행목적 배열 ("R" , "C", "N" 중 선택, 다중 선택 가능)
        # └ R = 영수, C = 청구, N = 없음
        # - 미입력 시 전체조회
        PurposeType = ["R", "C", "N"]

        # 종사업장번호 유무 (null , "0" , "1" 중 택 1)
        # - null = 전체 , 0 = 없음, 1 = 있음
        TaxRegIDYN = ""

        # 종사업장번호의 주체 ("S" , "B" , "T" 중 택 1)
        # └ S = 공급자 , B = 공급받는자 , T = 수탁자
        # - 미입력시 전체조회
        TaxRegIDType = "S"

        # 종사업장번호
        # 다수기재시 콤마(",")로 구분하여 구성 ex ) "0001,0002"
        # - 미입력시 전체조회
        TaxRegID = ""

        # 거래처 상호 / 사업자번호 (사업자) / 주민등록번호 (개인) / "9999999999999" (외국인) 중 검색하고자 하는 정보 입력
        # - 사업자번호 / 주민등록번호는 하이픈('-')을 제외한 숫자만 입력
        # - 미입력시 전체조회
        SearchString = ""

        response = htTaxinvoiceService.summary(CorpNum, JobID, Type, TaxType, PurposeType,
                                                TaxRegIDType, TaxRegIDYN, TaxRegID, UserID, SearchString)

        return render(request, 'HTTaxinvoice/Summary.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getTaxinvoice(request):
    """
    국세청 승인번호를 통해 수집한 전자세금계산서 1건의 상세정보를 반환합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetTaxinvoice
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자세금계산서 국세청승인번호
        NTSConfirmNum = "20211227410002030000103d"

        taxinvoice = htTaxinvoiceService.getTaxinvoice(CorpNum, NTSConfirmNum)

        return render(request, 'HTTaxinvoice/GetTaxinvoice.html', {'taxinvoice': taxinvoice})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getXML(request):
    """
    국세청 승인번호를 통해 수집한 전자세금계산서 1건의 상세정보를 XML 형태의 문자열로 반환합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetXML
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자세금계산서 국세청승인번호
        NTSConfirmNum = "20211227410002030000103d"

        response = htTaxinvoiceService.getXML(CorpNum, NTSConfirmNum)

        return render(request, 'HTTaxinvoice/GetXML.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPopUpURL(request):
    """
    수집된 전자세금계산서 1건의 상세내역을 확인하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetPopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 조회할 전자세금계산서 국세청 승인번호
        NTSConfirmNum = "20211227410002030000103d"

        url = htTaxinvoiceService.getPopUpURL(CorpNum, NTSConfirmNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPrintURL(request):
    """
    수집된 전자세금계산서 1건의 상세내역을 인쇄하는 페이지의 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자세금계산서 국세청 승인번호
        NTSConfirmNum = "20211227410002030000103d"

        url = htTaxinvoiceService.getPrintURL(CorpNum, NTSConfirmNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getCertificatePopUpURL(request):
    """
    홈택스연동 인증정보를 관리하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetCertificatePopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htTaxinvoiceService.getCertificatePopUpURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getCertificateExpireDate(request):
    """
    팝빌에 등록된 인증서 만료일자를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetCertificateExpireDate
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        expiredate = htTaxinvoiceService.getCertificateExpireDate(CorpNum)

        return render(request, 'HTTaxinvoice/GetCertificateExpireDate.html', {'expiredate': expiredate})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkCertValidation(request):
    """
    팝빌에 등록된 인증서로 홈택스 로그인 가능 여부를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#CheckCertValidation
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
    홈택스연동 인증을 위해 팝빌에 전자세금계산서용 부서사용자 계정을 등록합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#RegistDeptUser
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
    홈택스연동 인증을 위해 팝빌에 등록된 전자세금계산서용 부서사용자 계정을 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#CheckDeptUser
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
    팝빌에 등록된 전자세금계산서용 부서사용자 계정 정보로 홈택스 로그인 가능 여부를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#CheckLoginDeptUser
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
    팝빌에 등록된 홈택스 전자세금계산서용 부서사용자 계정을 삭제합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#DeleteDeptUser
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.deleteDeptUser(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getFlatRatePopUpURL(request):
    """
    홈택스연동 정액제 서비스 신청 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetFlatRatePopUpURL
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
    홈택스연동 정액제 서비스 상태를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetFlatRateState
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        flatRateState = htTaxinvoiceService.getFlatRateState(CorpNum)

        return render(request, 'HTCashbill/GetFlatRateState.html', {'flatRateState': flatRateState})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetBalance
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
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetChargeURL
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

def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htTaxinvoiceService.getPaymentURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = htTaxinvoiceService.getUseHistoryURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetPartnerBalance
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
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetPartnerURL
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
    팝빌 홈택스연동(세금) API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.getChargeInfo(CorpNum)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#CheckIsMember
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
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#CheckID
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
    사용자를 연동회원으로 가입처리합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#JoinMember
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

        response = htTaxinvoiceService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetAccessURL
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

def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = htTaxinvoiceService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#UpdateCorpInfo
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

        response = htTaxinvoiceService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#RegistContact
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

        response = htTaxinvoiceService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = htTaxinvoiceService.getContactInfo(CorpNum, contactID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = htTaxinvoiceService.listContact(CorpNum)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/httaxinvoice/python/api#UpdateContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

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

        response = htTaxinvoiceService.updateContact(CorpNum, updateInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})