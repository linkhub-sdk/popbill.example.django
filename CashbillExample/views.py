# -*- coding: utf-8 -*-
"""
팝빌 현금영수증 API Python SDK Django Example

Django 연동 튜토리얼 안내 : https://developers.popbill.com/guide/cashbill/python/getting-started/tutorial
연동 기술지원 연락처 : 1600-9854
연동 기술지원 이메일 : code@linkhubcorp.com
"""
from datetime import datetime, timedelta
from django.shortcuts import render
from popbill import (
    Cashbill,
    CashbillService,
    ContactInfo,
    CorpInfo,
    JoinForm,
    PopbillException,
    RefundForm,
    PaymentForm
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 CashbillService 객체 생성
cashbillService = CashbillService(settings.LinkID, settings.SecretKey)

# 연동환경 설정, true-테스트, false-운영(Production), (기본값:true)
cashbillService.IsTest = settings.IsTest

# 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
cashbillService.IPRestrictOnOff = settings.IPRestrictOnOff

# 통신 IP 고정, true-사용, false-미사용, (기본값:false)
cashbillService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, true-사용, false-미사용, (기본값:true)
cashbillService.UseLocalTimeYN = settings.UseLocalTimeYN


def index(request):
    return render(request, "Cashbill/Index.html", {})


def checkMgtKeyInUse(request):
    """
    파트너가 현금영수증 관리 목적으로 할당하는 문서번호 사용여부를 확인합니다.
    - 이미 사용 중인 문서번호는 중복 사용이 불가하며 현금영수증이 삭제된 경우에만 문서번호의 재사용이 가능합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/info#CheckMgtKeyInUse
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        MgtKey = "20220805-001"

        bIsInUse = cashbillService.checkMgtKeyInUse(CorpNum, MgtKey)
        if bIsInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registIssue(request):
    """
    작성된 현금영수증 데이터를 팝빌에 저장과 동시에 발행하여 "발행완료" 상태로 처리합니다.
    - 현금영수증 국세청 전송 정책 : https://developers.popbill.com/guide/cashbill/python/introduction/policy-of-send-to-nts
    - https://developers.popbill.com/reference/cashbill/python/api/issue#RegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 즉시발행 메모
        Memo = "현금영수증 즉시발행 메모"

        # 안내메일 제목, 미기재시 기본양식으로 전송
        EmailSubject = ""

        # 현금영수증 정보
        cashbill = Cashbill(
            # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
            mgtKey="202220805-021",
            # 문서형태, 승인거래 기재
            tradeType="승인거래",
            # 과세형태 (과세, 비과세) 중 기재
            taxationType="과세",
            # 거래유형 (일반, 도서공연, 대중교통) 중 기재
            # - 미입력시 기본값 "일반" 처리
            tradeOpt="일반",
            # 거래구분 (소득공제용, 지출증빙용) 중 기재
            tradeUsage="소득공제용",
            # 식별번호, 거래구분에 따라 작성
            # └ 소득공제용 - 주민등록/휴대폰/카드번호(현금영수증 카드)/자진발급용 번호(010-000-1234) 기재가능
            # └ 지출증빙용 - 사업자번호/주민등록/휴대폰/카드번호(현금영수증 카드) 기재가능
            # └ 주민등록번호 13자리, 휴대폰번호 10~11자리, 카드번호 13~19자리, 사업자번호 10자리 입력 가능
            identityNum="010-000-1234",
            # 공급가액
            supplyCost="10000",
            # 세액
            tax="1000",
            # 봉사료
            serviceFee="0",
            # 거래금액, 공급가액+세액+봉사료
            totalAmount="11000",
            # 가맹점 사업자번호
            franchiseCorpNum=CorpNum,
            # 가맹점 종사업장 식별번호
            franchiseTaxRegID="",
            # 가맹점 상호
            franchiseCorpName="가맹점 상호",
            # 가맹점 대표자성명
            franchiseCEOName="발행 대표자 성명",
            # 가맹점 주소
            franchiseAddr="가맹점 주소",
            # 가맹점 연락처
            franchiseTEL="",
            # 주문자명
            customerName="주문자명",
            # 주문상품명
            itemName="주문상품명",
            # 주문번호
            orderNumber="주문번호",
            # 이메일
            # 팝빌 테스트 환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            email="",
            # 휴대폰
            hp="",
            # 발행시 알림문자 전송여부
            # 문자전송시 포인트가 차감되며 전송실패시 환불처리됨.
            smssendYN=False,
            # 거래일시, 날짜(yyyyMMddHHmmss)
            # 당일, 전일만 가능, 미입력시 기본값 발행일시 처리
            tradeDT="20230320",
        )

        response = cashbillService.registIssue(
            CorpNum, cashbill, Memo, UserID, EmailSubject
        )

        return render(
            request,
            "response.html",
            {
                "code": response.code,
                "message": response.message,
                "confirmNum": response.confirmNum,
                "tradeDate": response.tradeDate,
            },
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def bulkSubmit(request):
    """
    최대 100건의 현금영수증 발행을 한번의 요청으로 접수합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/issue#BulkSubmit
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 제출아이디
        # 최대 36자리 영문, 숫자, '-' 조합으로 구성
        submitID = "PYTHON-DJANGO-BULK"

        # 현금영수증 객체정보 리스트
        cashbillList = []
        for i in range(1, 101):
            cashbillList.append(
                Cashbill(
                    # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
                    mgtKey=submitID + "-" + str(i),
                    # 문서형태, (승인거래, 취소거래) 중 기재
                    tradeType="승인거래",
                    # # [취소거래시 필수] 원본 현금영수증 국세청승인번호
                    # orgConfirmNum="",
                    # # [취소거래시 필수] 원본 현금영수증 거래일자
                    # orgTradeDate="",
                    # 과세형태 (과세, 비과세) 중 기재
                    taxationType="과세",
                    # 거래유형 (일반, 도서공연, 대중교통) 중 기재
                    # - 미입력시 기본값 "일반" 처리
                    tradeOpt="일반",
                    # 거래구분 (소득공제용, 지출증빙용) 중 기재
                    tradeUsage="소득공제용",
                    # 식별번호, 거래구분에 따라 작성
                    # └ 소득공제용 - 주민등록/휴대폰/카드번호(현금영수증 카드)/자진발급용 번호(010-000-1234) 기재가능
                    # └ 지출증빙용 - 사업자번호/주민등록/휴대폰/카드번호(현금영수증 카드) 기재가능
                    # └ 주민등록번호 13자리, 휴대폰번호 10~11자리, 카드번호 13~19자리, 사업자번호 10자리 입력 가능
                    identityNum="010-000-1234",
                    # 공급가액
                    supplyCost="10000",
                    # 세액
                    tax="1000",
                    # 봉사료
                    serviceFee="0",
                    # 거래금액, 공급가액+세액+봉사료
                    totalAmount="11000",
                    # 가맹점 사업자번호
                    franchiseCorpNum=CorpNum,
                    # 가맹점 종사업장 식별번호
                    franchiseTaxRegID="",
                    # 가맹점 상호
                    franchiseCorpName="가맹점 상호",
                    # 가맹점 대표자성명
                    franchiseCEOName="발행 대표자 성명",
                    # 가맹점 주소
                    franchiseAddr="가맹점 주소",
                    # 가맹점 연락처
                    franchiseTEL="",
                    # 주문자명
                    customerName="주문자명",
                    # 주문상품명
                    itemName="주문상품명",
                    # 주문번호
                    orderNumber="주문번호",
                    # 이메일
                    # 팝빌 테스트 환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
                    # 실제 거래처의 메일주소가 기재되지 않도록 주의
                    email="",
                    # 휴대폰
                    hp="",
                    # 발행시 알림문자 전송여부
                    # 문자전송시 포인트가 차감되며 전송실패시 환불처리됨.
                    smssendYN=False,
                    # 거래일시, 날짜(yyyyMMddHHmmss)
                    # 당일, 전일만 가능, 미입력시 기본값 발행일시 처리
                    tradeDT="20221108000000",
                )
            )
        bulkResponse = cashbillService.bulkSubmit(CorpNum, submitID, cashbillList)

        return render(request,"Cashbill/BulkResponse.html",{"code": bulkResponse.code,"message": bulkResponse.message,"receiptID": bulkResponse.receiptID,})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBulkResult(request):
    """
    접수시 기재한 SubmitID를 사용하여 현금영수증 접수결과를 확인합니다.
    - 개별 현금영수증 처리상태는 접수상태(txState)가 완료(2) 시 반환됩니다.
    - https://developers.popbill.com/reference/cashbill/python/api/issue#GetBulkResult
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 제출아이디
        # 최대 36자리 영문, 숫자, '-' 조합으로 구성
        submitID = "PYTHON-DJANGO-BULK"

        bulkCashbillResult = cashbillService.getBulkResult(CorpNum, submitID)

        return render(request,"Cashbill/BulkResult.html",{"bulkCashbillResult": bulkCashbillResult})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def delete(request):
    """
    삭제 가능한 상태의 현금영수증을 삭제합니다.
    - 삭제 가능한 상태: "전송실패"
    - 현금영수증을 삭제하면 사용된 문서번호(mgtKey)를 재사용할 수 있습니다.
    - https://developers.popbill.com/reference/cashbill/python/api/issue#Delete
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        response = cashbillService.delete(CorpNum, MgtKey)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def revokeRegistIssue(request):
    """
    취소 현금영수증 데이터를 팝빌에 저장과 동시에 발행하여 "발행완료" 상태로 처리합니다.
    - 취소 현금영수증의 금액은 원본 금액을 넘을 수 없습니다.
    - 현금영수증 국세청 전송 정책 [https://developers.popbill.com/guide/cashbill/python/introduction/policy-of-send-to-nts]
    - 취소 현금영수증 발행 시 구매자 메일주소로 발행 안내 베일이 전송되니 유의하시기 바랍니다.
    - https://developers.popbill.com/reference/cashbill/python/api/issue#RevokeRegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20220805-002"

        # 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "TB0000176"

        # 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20220802"

        # 발행안내문자 전송여부
        smssendYN = False

        # 즉시발행 메모
        memo = "취소현금영수증 즉시발행 메모"

        response = cashbillService.revokeRegistIssue(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, memo)

        return render(request,"response.html",{"code": response.code,"message": response.message,"confirmNum": response.confirmNum,"tradeDate": response.tradeDate,})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def revokeRegistIssue_part(request):
    """
    작성된 (부분)취소 현금영수증 데이터를 팝빌에 저장과 동시에 발행하여 "발행완료" 상태로 처리합니다.
    - 취소 현금영수증의 금액은 원본 금액을 넘을 수 없습니다.
    - 현금영수증 국세청 전송 정책 [https://developers.popbill.com/guide/cashbill/python/introduction/policy-of-send-to-nts]
    - 취소 현금영수증 발행 시 구매자 메일주소로 발행 안내 베일이 전송되니 유의하시기 바랍니다.
    - https://developers.popbill.com/reference/cashbill/python/api/issue#RevokeRegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20220805-003"

        # 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "TB0000174"

        # 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20220802"

        # 현금영수증 발행시 알림문자 전송여부 : true / false 중 택 1
        # └ true = 전송, false = 미전송
        # └ 원본 현금영수증의 구매자(고객)의 휴대폰번호 문자 전송
        smssendYN = False

        # 현금영수증 상태 이력을 관리하기 위한 메모
        memo = "부분취소 현금영수증 즉시발행 메모"

        # 현금영수증 취소유형 : true / false 중 택 1
        # └ true = 부분 취소, false = 전체 취소
        # - 미입력시 기본값 false 처리
        isPartCancel = True

        # 현금영수증 취소사유 : 1 / 2 / 3 중 택 1
        # └ 1 = 거래취소, 2 = 오류발급취소, 3 = 기타
        # - 미입력시 기본값 1 처리
        cancelType = 1

        # [취소] 공급가액
        # - 현금영수증 취소유형이 true 인 경우 취소할 공급가액 입력
        # - 현금영수증 취소유형이 false 인 경우 미입력
        supplyCost = "1000"

        # [취소] 부가세
        # - 현금영수증 취소유형이 true 인 경우 취소할 부가세 입력
        # - 현금영수증 취소유형이 false 인 경우 미입력
        tax = "100"

        # [취소] 봉사료
        # - 현금영수증 취소유형이 true 인 경우 취소할 봉사료 입력
        # - 현금영수증 취소유형이 false 인 경우 미입력
        serviceFee = "0"

        # [취소] 거래금액 (공급가액+부가세+봉사료)
        # - 현금영수증 취소유형이 true 인 경우 취소할 거래금액 입력
        # - 현금영수증 취소유형이 false 인 경우 미입력
        totalAmount = "1100"

        # 안내메일 제목, 공백처리시 기본양식으로 전송
        emailSubject = "메일제목 테스트"

        # 거래일시, 날짜(yyyyMMddHHmmss)
        # 당일, 전일만 가능, 미입력시 기본값 발행일시 처리
        tradeDT = "20221108000000"

        response = cashbillService.revokeRegistIssue(CorpNum,mgtKey,orgConfirmNum,orgTradeDate,smssendYN,memo,UserID,isPartCancel,cancelType,supplyCost,tax,serviceFee,totalAmount,emailSubject,tradeDT)

        return render(request,"response.html",{"code": response.code,"message": response.message,"confirmNum": response.confirmNum,"tradeDate": response.tradeDate,"tradeDT": response.tradeDT,})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfo(request):
    """
    현금영수증 1건의 상태 및 요약정보를 확인합니다.
    - 리턴값 'CashbillInfo'의 변수 'stateCode'를 통해 현금영수증의 상태코드를 확인합니다.
    - 현금영수증 상태코드 [https://developers.popbill.com/reference/cashbill/python/response-code#state-code]
    - https://developers.popbill.com/reference/cashbill/python/api/info#GetInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        cashbillInfo = cashbillService.getInfo(CorpNum, MgtKey)

        return render(request, "Cashbill/GetInfo.html", {"cashbillInfo": cashbillInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfos(request):
    """
    다수건의 현금영수증 상태 및 요약 정보를 확인합니다. (1회 호출 시 최대 1,000건 확인 가능)
    - 리턴값 'CashbillInfo'의 변수 'stateCode'를 통해 현금영수증의 상태코드를 확인합니다.
    - 현금영수증 상태코드 [https://developers.popbill.com/reference/cashbill/python/response-code#state-code]
    - https://developers.popbill.com/reference/cashbill/python/api/info#GetInfos
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")
        MgtKeyList.append("20220805-003")

        InfoList = cashbillService.getInfos(CorpNum, MgtKeyList)

        return render(request, "Cashbill/GetInfos.html", {"InfoList": InfoList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getDetailInfo(request):
    """
    현금영수증 1건의 상세정보를 조회합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/info#GetDetailInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        cashbill = cashbillService.getDetailInfo(CorpNum, MgtKey)

        return render(request, "Cashbill/GetDetailInfo.html", {"cashbill": cashbill})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    검색조건에 해당하는 현금영수증을 조회합니다. (조회기간 단위 : 최대 6개월)
    - https://developers.popbill.com/reference/cashbill/python/api/info#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 조회 일자유형, [R-등록일자 / T-거래일자 / I-발행일자]
        DType = "R"

        # 시작일자, 표시형식(yyyyMMdd)
        SDate = "20241201"

        # 종료일자, 표시형식(yyyyMMdd)
        EDate = "20241231"

        # 상태코드 배열 (2,3번째 자리에 와일드카드(*) 사용 가능)
        # - 미입력시 전체조회
        State = ["3**"]

        # 문서형태 배열 ("N" , "C" 중 선택, 다중 선택 가능)
        # - N = 일반 현금영수증 , C = 취소 현금영수증
        # - 미입력시 전체조회
        TradeType = ["N", "C"]

        # 거래구분 배열 ("P" , "C" 중 선택, 다중 선택 가능)
        # - P = 소득공제용 , C = 지출증빙용
        # - 미입력시 전체조회
        TradeUsage = ["P", "C"]

        # 과세형태 배열 ("T" , "N" 중 선택, 다중 선택 가능)
        # - T = 과세 , N = 비과세
        # - 미입력시 전체조회
        TaxationType = ["T", "N"]

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향, [D-내림차순 / A-오름차순]
        Order = "D"

        # 현금영수증 식별번호, 미기재시 전체조회
        QString = ""

        # 거래유형 배열 ("N" , "B" , "T" 중 선택, 다중 선택 가능)
        # - N = 일반 , B = 도서공연 , T = 대중교통
        # - 미입력시 전체조회
        TradeOpt = ["N", "B", "T"]

        # 가맹점 종사업장 번호
        # └ 다수건 검색시 콤마(",")로 구분. 예) "1234,1000"
        # └ 미입력시 전제조회
        FranchiseTaxRegID = ""

        response = cashbillService.search(CorpNum,DType,SDate,EDate,State,TradeType,TradeUsage,TaxationType,Page,PerPage,Order,UserID,QString,TradeOpt,FranchiseTaxRegID)

        return render(request, "Cashbill/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getURL(request):
    """
    로그인 상태로 팝빌 사이트의 현금영수증 문서함 메뉴에 접근할 수 있는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/info#GetURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 접근 메뉴 : "TBOX" / "PBOX" / "WRITE" 중 택 1
        # └ TBOX = 임시 문서함, PBOX = 발행 문서함, WRITE = 현금영수증 작성 중 택 1
        TOGO = "WRITE"

        url = cashbillService.getURL(CorpNum, UserID, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPopUpURL(request):
    """
    팝빌 사이트와 동일한 현금영수증 1건의 상세 정보 페이지의 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetPopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        url = cashbillService.getPopUpURL(CorpNum, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getViewURL(request):
    """
    팝빌 사이트와 동일한 현금영수증 1건의 상세 정보 페이지(사이트 상단, 좌측 메뉴 및 버튼 제외)의 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetViewURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        url = cashbillService.getViewURL(CorpNum, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPrintURL(request):
    """
    현금영수증 1건을 인쇄하기 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        url = cashbillService.getPrintURL(CorpNum, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMassPrintURL(request):
    """
    다수건의 현금영수증을 인쇄하기 위한 페이지의 팝업 URL을 반환합니다. (최대 100건)
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetMassPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 문서번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")
        MgtKeyList.append("20220805-003")

        url = cashbillService.getMassPrintURL(CorpNum, MgtKeyList, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMailURL(request):
    """
    현금영수증 안내 메일의 상세보기 링크 URL을 반환합니다.
    - 함수 호출로 반환 받은 URL에는 유효시간이 없습니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetMailURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        url = cashbillService.getMailURL(CorpNum, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPDFURL(request):
    """
    현금영수증 PDF 파일을 다운 받을 수 있는 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/view#GetPDFURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        url = cashbillService.getPDFURL(CorpNum, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendEmail(request):
    """
    현금영수증과 관련된 안내 메일을 재전송 합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/etc#SendEmail
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        # 수신메일주소
        # 팝빌 테스트 환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
        # 실제 거래처의 메일주소가 기재되지 않도록 주의
        Receiver = ""

        response = cashbillService.sendEmail(CorpNum, MgtKey, Receiver)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendSMS(request):
    """
    현금영수증과 관련된 안내 SMS(단문) 문자를 재전송하는 함수로, 팝빌 사이트 [문자·팩스] > [문자] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 메시지는 최대 90byte까지 입력 가능하고, 초과한 내용은 자동으로 삭제되어 전송합니다. (한글 최대 45자)
    - 알림문자 전송시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://developers.popbill.com/reference/cashbill/python/api/etc#SendSMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        # 발신번호
        Sender = ""

        # 수신번호
        Receiver = ""

        # 메시지내용, 메시지 길이가 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "현금영수증 문자메시지 전송 테스트"

        response = cashbillService.sendSMS(CorpNum, MgtKey, Sender, Receiver, Contents)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAX(request):
    """
    현금영수증을 팩스로 전송하는 함수로, 팝빌 사이트 [문자·팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://developers.popbill.com/reference/cashbill/python/api/etc#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20220805-001"

        # 발신번호
        Sender = ""

        # 수신팩스번호
        Receiver = ""

        response = cashbillService.sendFAX(CorpNum, MgtKey, Sender, Receiver)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def assignMgtKey(request):
    """
    팝빌 사이트를 통해 발행하여 문서번호가 할당되지 않은 현금영수증에 문서번호를 할당합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/etc#AssignMgtKey
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 아이템키, 문서 목록조회(Search) API의 반환항목중 ItemKey 참조
        ItemKey = "022071308525600001"

        # 할당할 문서번호, 숫자, 영문 '-', '_' 조합으로 최대 24자리, 사업자번호별 중복없는 고유번호 할당
        MgtKey = "20220805-004"

        response = cashbillService.assignMgtKey(CorpNum, ItemKey, MgtKey)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listEmailConfig(request):
    """
    현금영수증 관련 메일 항목에 대한 발송설정을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/etc#ListEmailConfig
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        EmailConfig = cashbillService.listEmailConfig(CorpNum)

        return render(request, "Cashbill/ListEmailConfig.html", {"EmailConfig": EmailConfig})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateEmailConfig(request):
    """
    현금영수증 관련 메일 항목에 대한 발송설정을 수정합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/etc#UpdateEmailConfig

    메일전송유형
    CSH_ISSUE : 고객에게 현금영수증이 발행 되었음을 알려주는 메일 입니다.
    CSH_CANCEL : 고객에게 현금영수증이 발행취소 되었음을 알려주는 메일 입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 메일 전송 유형
        EmailType = "CSH_ISSUE"

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        response = cashbillService.updateEmailConfig(CorpNum, EmailType, SendYN)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = cashbillService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = cashbillService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = cashbillService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUnitCost(request):
    """
    현금영수증 발행시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        result = cashbillService.getUnitCost(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 현금영수증 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = cashbillService.getChargeInfo(CorpNum)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#PaymentRequest
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

        response = cashbillService.paymentRequest(CorpNum, paymentForm, UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetPaymentHistory
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

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getPaymentHistory(CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetUseHistory
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

        response = cashbillService.getUseHistory(CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#Refund
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

        response =  cashbillService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message, "refundCode": response.refundCode})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/cashbill/python/api/point#GetRefundHistory
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

        response = cashbillService.getRefundHistory(CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = cashbillService.checkIsMember(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = cashbillService.checkID(memberID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#JoinMember
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

        response = cashbillService.joinMember(newMember)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = cashbillService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#UpdateCorpInfo
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

        response = cashbillService.updateCorpInfo(CorpNum, corpInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#RegistContact
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

        response = cashbillService.registContact(CorpNum, newContact)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = cashbillService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = cashbillService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#UpdateContact
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

        response = cashbillService.updateContact(CorpNum, updateInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def quitMember(request):
    """
    가입된 연동회원의 탈퇴를 요청합니다.
    - 회원탈퇴 신청과 동시에 팝빌의 모든 서비스 이용이 불가하며, 관리자를 포함한 모든 담당자 계정도 일괄탈퇴 됩니다.
    - 회원탈퇴로 삭제된 데이터는 복원이 불가능합니다.
    - 관리자 계정만 사용 가능합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/member#QuitMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 탈퇴 사유
        QuitReason = "테스트 탈퇴 사유"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.quitMember(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundInfo(request):
    """
    포인트 환불에 대한 상세정보 1건을 확인합니다.
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetRefundInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 환불코드
        RefundCode = "023040000017"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getRefundInfo(CorpNum,RefundCode,UserID)
        return render(request, 'getRefundInfo.html', {"code": response.code, "response": response})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundableBalance(request):
    """
    환불 가능한 포인트를 확인합니다. (보너스 포인트는 환불가능포인트에서 제외됩니다.)
    - https://developers.popbill.com/reference/cashbill/python/api/point#GetRefundableBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        refundableBalance = cashbillService.getRefundableBalance(CorpNum, UserID)
        return render(request, 'getRefundableBalance.html', {"refundableBalance": refundableBalance})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})