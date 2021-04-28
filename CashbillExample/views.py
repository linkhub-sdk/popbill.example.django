# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import CashbillService, PopbillException, Cashbill, ContactInfo, CorpInfo, JoinForm

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 CashbillService 객체 생성
cashbillService = CashbillService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
cashbillService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
cashbillService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부(GA), true-사용, false-미사용, 기본값(false)
cashbillService.UseStaticIP = settings.UseStaticIP

#로컬서버 시간 사용여부, 권장(True)
cashbillService.UseLocalTimeYN = settings.UseLocalTimeYN

def index(request):
    return render(request, 'Cashbill/Index.html', {})


def checkMgtKeyInUse(request):
    """
    현금영수증 문서번호 중복여부를 확인합니다.
    - 문서번호는 1~24자리로 (숫자, 영문 '-', '_') 조합으로 구성할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#CheckMgtKeyInUse
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        MgtKey = "20190116-001"

        bIsInUse = cashbillService.checkMgtKeyInUse(CorpNum, MgtKey)
        if bIsInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registIssue(request):
    """
    1건의 현금영수증을 즉시발행합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#RegistIssue
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

            # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
            mgtKey="20191030-001",

            # [필수] 문서형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [일반 / 도서공연 / 대중교통]
            tradeOpt="일반",

            # [필수] 거래구분, [소득공제용 /지출증빙용]
            tradeUsage="소득공제용",

            # [필수] 거래처 식별번호
            # 거래유형이 '지출증빙용' - [휴대폰/카드/주민등록/사업자] 번호 입력
            # 거래유형이 '소득공제용' - [휴대폰/카드/주민등록] 번호 입력
            # 자진발급 "010-000-1234" 의 경우 "소득공제용"으로만 발급 가능
            identityNum="010-000-1234",

            # [필수] 공급가액
            supplyCost="10000",

            # [필수] 세액
            tax="1000",

            # 봉사료
            serviceFee="0",

            # [필수] 거래금액, 공급가액+세액+봉사료
            totalAmount="11000",

            # 발행자 사업자번호
            franchiseCorpNum=CorpNum,

            # 발행자 상호
            franchiseCorpName="발행자 상호",

            # 발행자 대표자성명
            franchiseCEOName="발행 대표자 성명",

            # 발행자 주소
            franchiseAddr="발행자 주소",

            # 발행자 연락처
            franchiseTEL="07012345678",

            # 주문자명
            customerName="주문자명",

            # 주문상품명
            itemName="주문상품명",

            # 주문번호
            orderNumber="주문번호",

            # 이메일
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            email="test@test.com",

            # 휴대폰
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        response = cashbillService.registIssue(CorpNum, cashbill, Memo, UserID, EmailSubject)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def register(request):
    """
    1건의 현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - https://docs.popbill.com/cashbill/python/api#Register
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 정보
        cashbill = Cashbill(

            # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
            mgtKey="20190116-002",

            # [필수] 문서형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [일반 / 도서공연 / 대중교통]
            tradeOpt="일반",

            # [필수] 거래구분, [소득공제용 /지출증빙용]
            tradeUsage="소득공제용",

            # [필수] 거래처 식별번호
            # 거래유형이 '지출증빙용' - [휴대폰/카드/주민등록/사업자] 번호 입력
            # 거래유형이 '소득공제용' - [휴대폰/카드/주민등록] 번호 입력
            # 자진발급 "010-000-1234" 의 경우 "소득공제용"으로만 발급 가능
            identityNum="010-000-1234",

            # [필수] 공급가액
            supplyCost="10000",

            # 부가세
            tax="1000",

            # 봉사료
            serviceFee="0",

            # [필수] 거래금액, (공급가액+부가세+봉사료)
            totalAmount="11000",

            # 가맹점 사업자번호
            franchiseCorpNum=CorpNum,

            # 가맹점 상호
            franchiseCorpName="가맹점 상호",

            # 가맹점 대표자성명
            franchiseCEOName="발행 대표자 성명",

            # 가맹점 주소
            franchiseAddr="가맹점 주소",

            # 가맹점 연락처
            franchiseTEL="07012345678",

            # 주문자명
            customerName="주문자명",

            # 주문상품명
            itemName="주문상품명",

            # 주문번호
            orderNumber="주문번호",

            # 이메일
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            email="test@test.com",

            # 휴대폰
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        response = cashbillService.register(CorpNum, cashbill)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def update(request):
    """
    1건의 현금영수증을 수정합니다.
    - [임시저장] 상태의 현금영수증만 수정할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#Update
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 수정하고자하는 현금영수증 문서번호
        MgtKey = '20190116-002'

        # 현금영수증 정보
        cashbill = Cashbill(

            # [필수] 문서번호
            mgtKey=MgtKey,

            # [필수] 문서형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [일반 / 도서공연 / 대중교통]
            tradeOpt="일반",

            # [필수] 거래구분, [소득공제용 /지출증빙용]
            tradeUsage="소득공제용",

            # [필수] 거래처 식별번호
            # 거래유형이 '지출증빙용' - [휴대폰/카드/주민등록/사업자] 번호 입력
            # 거래유형이 '소득공제용' - [휴대폰/카드/주민등록] 번호 입력
            # 자진발급 "010-000-1234" 의 경우 "소득공제용"으로만 발급 가능
            identityNum="010-000-1234",

            # [필수] 공급가액
            supplyCost="20000",

            # 부가세
            tax="2000",

            # 봉사료
            serviceFee="0",

            # [필수] 거래금액, (공급가액+부가세+봉사료)
            totalAmount="22000",

            # 가맹점 사업자번호
            franchiseCorpNum="1234567890",

            # 가맹점 상호
            franchiseCorpName="가맹점 상호_수정",

            # 가맹점 대표자성명
            franchiseCEOName="발행 대표자 성명_수정",

            # 가맹점 주소
            franchiseAddr="가맹점 주소",

            # 가맹점 연락처
            franchiseTEL="07012345678",

            # 주문자명
            customerName="주문자명",

            # 주문상품명
            itemName="주문상품명",

            # 주문번호
            orderNumber="주문번호",

            # 이메일
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            email="test@test.com",

            # 휴대폰
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        response = cashbillService.update(CorpNum, MgtKey, cashbill)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def issue(request):
    """
    1건의 임시저장 현금영수증을 발행처리합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#CBIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호
        MgtKey = "20190116-002"

        # 메모
        Memo = "발행 메모"

        response = cashbillService.issue(CorpNum, MgtKey, Memo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelIssue(request):
    """
    [발행완료] 상태의 현금영수증을 [발행취소] 합니다.
    - 발행취소는 국세청 전송전에만 가능합니다.
    - https://docs.popbill.com/cashbill/python/api#CancelIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-002"

        # 메모
        Memo = "발행취소 메모"

        response = cashbillService.cancelIssue(CorpNum, MgtKey, Memo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def delete(request):
    """
    1건의 현금영수증을 삭제합니다.
    - 현금영수증을 삭제하면 사용된 문서번호(mgtKey)를 재사용할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#Delete
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-002"

        response = cashbillService.delete(CorpNum, MgtKey)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def revokeRegistIssue(request):
    """
    1건의 취소현금영수증을 즉시발행합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#RevokeRegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20190116-101"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "158814020"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20190115"

        # 발행안내문자 전송여부
        smssendYN = False

        # 즉시발행 메모
        memo = "현금영수증 즉시발행 메모"

        response = cashbillService.revokeRegistIssue(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, memo,
                                                     UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def revokeRegistIssue_part(request):
    """
    1건의 (부분) 취소현금영수증을 즉시발행합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#RevokeRegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20190116-102"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "158814020"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20190115"

        # 발행안내문자 전송여부
        smssendYN = False

        # 즉시발행 메모
        memo = "현금영수증 즉시발행 메모"

        # 부분취소여부, [True-부분취소 / False-전체취소]
        isPartCancel = True

        # 취소사유, [1-거래취소 /  2-오류발급취소 / 3-기타]
        cancelType = 1

        # [취소] 공급가액
        supplyCost = "10000"

        # [취소] 부가세
        tax = "1000"

        # [취소] 봉사료
        serviceFee = "0"

        # [취소] 합계거래금액, (공급가액+부가세+봉사료)
        # 원본 현금영수증의 공급가액 이하만 가능
        totalAmount = "11000"

        response = cashbillService.revokeRegistIssue(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, memo,
                                                     UserID,
                                                     isPartCancel, cancelType, supplyCost, tax, serviceFee, totalAmount)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def revokeRegister(request):
    """
    1건의 취소현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - https://docs.popbill.com/cashbill/python/api#RevokeRegister
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20190116-103"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "158814020"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20190115"

        # 발행안내문자 전송여부
        smssendYN = False

        response = cashbillService.revokeRegister(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def revokeRegister_part(request):
    """
    1건의 (부분) 취소현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - https://docs.popbill.com/cashbill/python/api#RevokeRegister
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20190123-123"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "760661092"

        # 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20190122"

        # 발행안내문자 전송여부
        smssendYN = False

        # 부분취소여부, [True-부분취소 / False-전체취소]
        isPartCancel = True

        # 취소사유, [1-거래취소 / 2-오류발급취소 / 3-기타]
        cancelType = 1

        # [취소] 공급가액
        supplyCost = "4000"

        # [취소] 부가세
        tax = "400"

        # [취소] 봉사료
        serviceFee = "0"

        # [취소] 합계금액
        totalAmount = "4400"

        response = cashbillService.revokeRegister(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, UserID,
                                                  isPartCancel, cancelType, supplyCost, tax, serviceFee, totalAmount)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfo(request):
    """
    1건의 현금영수증 상태/요약 정보를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#GetInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        cashbillInfo = cashbillService.getInfo(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetInfo.html', {'cashbillInfo': cashbillInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfos(request):
    """
    다수건의 현금영수증 상태/요약 정보를 확인합니다. (최대 1000건)
    - https://docs.popbill.com/cashbill/python/api#GetInfos
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20190116-001")
        MgtKeyList.append("20190116-002")
        MgtKeyList.append("20190116-003")

        InfoList = cashbillService.getInfos(CorpNum, MgtKeyList)

        return render(request, 'Cashbill/GetInfos.html', {'InfoList': InfoList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getDetailInfo(request):
    """
    현금영수증 1건의 상세정보를 조회합니다.
    - https://docs.popbill.com/cashbill/python/api#GetDetailInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        cashbill = cashbillService.getDetailInfo(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetDetailInfo.html', {'cashbill': cashbill})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 현금영수증 목록을 조회합니다.
    - https://docs.popbill.com/cashbill/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 조회 일자유형, [R-등록일자 / T-거래일자 / I-발행일자]
        DType = "R"

        # 시작일자, 표시형식(yyyyMMdd)
        SDate = "20190101"

        # 종료일자, 표시형식(yyyyMMdd)
        EDate = "20190116"

        # 상태코드 배열, 2,3번째 자리에 와일드카드(*) 사용 가능
        State = ["3**", "4**"]

        # 문서형태, [N-일반 현금영수증 / C-취소 현금영수증]
        TradeType = ["N", "C"]

        # 거래구분, [P-소득공제용 / C-지출증빙용]
        TradeUsage = ["P", "C"]

        # 과세형태, [T-과세 / N-비과세]
        TaxationType = ["T", "N"]

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향, [D-내림차순 / A-오름차순]
        Order = "D"

        # 현금영수증 식별번호, 미기재시 전체조회
        QString = ""

        # 거래유형 배열, [N-일반 / B-도서공연 / T-대중교통]
        TradeOpt = ["N", "B", "T"]

        response = cashbillService.search(CorpNum, DType, SDate, EDate, State, TradeType,
                                          TradeUsage, TaxationType, Page, PerPage, Order, UserID, QString, TradeOpt)

        return render(request, 'Cashbill/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getLogs(request):
    """
    현금영수증 상태 변경이력을 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#GetLogs
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        LogList = cashbillService.getLogs(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetLogs.html', {'LogList': LogList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL(request):
    """
    팝빌 현금영수증 관련 문서함 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    - https://docs.popbill.com/cashbill/python/api#GetURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # TBOX : 임시문서함 , PBOX : 발행 문서함 , WRITE : 문서작성
        TOGO = "WRITE"

        url = cashbillService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopUpURL(request):
    """
    1건의 현금영수증 보기 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    - https://docs.popbill.com/cashbill/python/api#GetPopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        url = cashbillService.getPopUpURL(CorpNum, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPDFURL(request):
    """
    1건의 현금영수증 PDF 다운로드 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20200728-02"

        url = cashbillService.getPDFURL(CorpNum, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPrintURL(request):
    """
    1건의 현금영수증 인쇄(공급자) URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/cashbill/python/api#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        url = cashbillService.getPrintURL(CorpNum, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getEPrintURL(request):
    """
    1건의 현금영수증 인쇄(공급받는자) URL을 반환합니다.
    - URL 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/cashbill/python/api#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        url = cashbillService.getEPrintURL(CorpNum, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMassPrintURL(request):
    """
    다수건의 현금영수증 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    - https://docs.popbill.com/cashbill/python/api#GetMassPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20190116-001")
        MgtKeyList.append("20190116-002")
        MgtKeyList.append("20190116-003")

        url = cashbillService.getMassPrintURL(CorpNum, MgtKeyList)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMailURL(request):
    """
    공급받는자 메일링크 URL을 반환합니다.
    - 메일링크 URL은 유효시간이 존재하지 않습니다.
    - https://docs.popbill.com/cashbill/python/api#GetMailURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        url = cashbillService.getMailURL(CorpNum, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/cashbill/python/api#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def assignMgtKey(request):
    """
    팝빌사이트에서 작성된 현금영수증에 파트너 문서번호를 할당합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 아이템키, 문서 목록조회(Search) API의 반환항목중 ItemKey 참조
        ItemKey = '020072815420200001'

        # 할당할 문서번호, 숫자, 영문 '-', '_' 조합으로 최대 24자리, 사업자번호별 중복없는 고유번호 할당
        MgtKey = "20200728-03"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.assignMgtKey(CorpNum, ItemKey, MgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendEmail(request):
    """
    안내 메일을 재전송합니다.
    - https://docs.popbill.com/cashbill/python/api#SendEmail
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        # 수신 메일주소
        Receiver = "test@test.com"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.sendEmail(CorpNum, MgtKey, Receiver, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendSMS(request):
    """
    알림문자를 전송합니다. (단문/SMS- 한글 최대 45자)
    - 알림문자 전송시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [문자] > [전송내역] 탭에서 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#SendSMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        # 발신번호
        Sender = "07012345678"

        # 수신번호
        Receiver = "010111222"

        # 메시지내용, 메시지 길이가 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "현금영수증 문자메시지 전송 테스트"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.sendSMS(CorpNum, MgtKey, Sender, Receiver, Contents, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFAX(request):
    """
    현금영수증을 팩스전송합니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인할 수 있습니다.
    - https://docs.popbill.com/cashbill/python/api#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서번호
        MgtKey = "20190116-001"

        # 발신번호
        Sender = "07012345678"

        # 수신팩스번호
        Receiver = "070111222"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.sendFAX(CorpNum, MgtKey, Sender, Receiver, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listEmailConfig(request):
    """
    현금영수증 관련 메일전송 항목에 대한 전송여부를 목록으로 반환합니다
    - https://docs.popbill.com/cashbill/python/api#ListEmailConfig
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        EmailConfig = cashbillService.listEmailConfig(CorpNum, UserID)

        return render(request, 'Cashbill/ListEmailConfig.html', {'EmailConfig': EmailConfig})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateEmailConfig(request):
    """
    현금영수증 관련 메일전송 항목에 대한 전송여부를 수정합니다.
    - https://docs.popbill.com/cashbill/python/api#UpdateEmailConfig

    메일전송유형
    CSH_ISSUE : 고객에게 현금영수증이 발행 되었음을 알려주는 메일 입니다.
    CSH_CANCEL : 고객에게 현금영수증이 발행취소 되었음을 알려주는 메일 입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 메일 전송 유형
        EmailType = 'CSH_ISSUE'

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.updateEmailConfig(CorpNum, EmailType, SendYN, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금이 아닌 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API)를
      통해 확인하시기 바랍니다.
    - https://docs.popbill.com/cashbill/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = cashbillService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeURL(request):
    """
    팝빌 연동회원 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/cashbill/python/api#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = cashbillService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를
      이용하시기 바랍니다.
    - https://docs.popbill.com/cashbill/python/api#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = cashbillService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/cashbill/python/api#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = cashbillService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    현금영수증 발행단가를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = cashbillService.getUnitCost(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 현금영수증 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#CheckIsMember
    """
    try:
        # 조회할 사업자등록번호, '-' 제외 10자리
        targetCorpNum = "1234567890"

        response = cashbillService.checkIsMember(targetCorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    팝빌 회원아이디 중복여부를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = cashbillService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    파트너의 연동회원으로 회원가입을 요청합니다.
    - 아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    - https://docs.popbill.com/cashbill/python/api#JoinMember
    """
    try:
        # 연동회원 가입정보
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

        response = cashbillService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateCorpInfo(request):
    """
    회사정보를 수정합니다.
    - https://docs.popbill.com/cashbill/python/api#UpdateCorpInfo
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

        response = cashbillService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registContact(request):
    """
    연동회원의 담당자를 신규로 등록합니다.
    - https://docs.popbill.com/cashbill/python/api#RegistContact
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

        response = cashbillService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    """
    연동회원의 담당자 목록을 확인합니다.
    - https://docs.popbill.com/cashbill/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        listContact = cashbillService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/cashbill/python/api#UpdateContact
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

        response = cashbillService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
