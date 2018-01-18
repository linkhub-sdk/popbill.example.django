# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import CashbillService, PopbillException, Cashbill, ContactInfo, CorpInfo, JoinForm

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 CashbillService 객체 생성
cashbillService = CashbillService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
cashbillService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Cashbill/Index.html', {})


def checkMgtKeyInUse(request):
    """
    현금영수증 관리번호 중복여부를 확인합니다.
    - 관리번호는 1~24자리로 숫자, 영문 '-', '_' 조합으로 구성할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 공급자별 고유번호 생성
        MgtKey = "20161122-01"

        bIsInUse = cashbillService.checkMgtKeyInUse(CorpNum, MgtKey)
        if bIsInUse:
            result = "사용중"
        else:
            result = "미사용중"
        return render(request, 'Cashbill/CheckMgtKeyInUse.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'Cashbill/CheckMgtKeyInUse.html', {'code': PE.code, 'message': PE.message})


def registIssue(request):
    try:
        """
        1건의 현금영수증을 즉시발행합니다.
        - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
        - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.3. 국세청 전송정책"을
          참조하시기 바랍니다.
        - 취소현금영수증 작성방법 안내 - http://blog.linkhub.co.kr/702
        """
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 즉시발행 메모
        Memo = "현금영수증 즉시발행 메모"

        # 현금영수증 정보
        cashbill = Cashbill(

            # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
            mgtKey="20180118-001",

            # [필수] 현금영수증 형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [소득공제용 /지출증빙용]
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
            franchiseCorpNum="1234567890",

            # 발행자 상호
            franchiseCorpName="발행자 상호",

            # 발행자 대표자성명
            franchiseCEOName="발행 대표자 성명",

            # 발행자 주소
            franchiseAddr="발행자 주소",

            # 발행자 연락처
            franchiseTEL="07012345678",

            # 고객명
            customerName="고객명",

            # 상품명
            itemName="상품명",

            # 주문번호
            orderNumber="주문번호",

            # 고객 메일주소
            email="test@test.com",

            # 고객 휴대폰번호
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        result = cashbillService.registIssue(CorpNum, cashbill, Memo, UserID)

        return render(request, 'Cashbill/RegistIssue.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RegistIssue.html', {'code': PE.code, 'message': PE.message})


def register(request):
    """
    1건의 현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책"을
      참조하시기 바랍니다.
    - 취소현금영수증 작성방법 안내 - http://blog.linkhub.co.kr/702
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 정보
        cashbill = Cashbill(

            # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 공급자별 고유번호 생성
            mgtKey="20180118-114",

            # [필수] 현금영수증 형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [소득공제용 /지출증빙용]
            tradeUsage="소득공제용",

            # [필수] 거래처 식별번호
            # 거래유형이 '지출증빙용' - [휴대폰/카드/주민등록/사업자] 번호 입력
            # 거래유형이 '소득공제용' - [휴대폰/카드/주민등록] 번호 입력
            # 자진발급 "010-000-1234" 의 경우 "소득공제용"으로만 발급 가능
            identityNum="010-000-1234",

            # [필수] 공급가액
            supplyCost="10000",

            # 세액
            tax="1000",

            # 봉사료
            serviceFee="0",

            # [필수] 거래금액, 공급가액+세액+봉사료
            totalAmount="11000",

            # 발행자 사업자번호
            franchiseCorpNum="1234567890",

            # 발행자 상호
            franchiseCorpName="발행자 상호",

            # 발행자 대표자성명
            franchiseCEOName="발행 대표자 성명",

            # 발행자 주소
            franchiseAddr="발행자 주소",

            # 발행자 연락처
            franchiseTEL="07012345678",

            # 고객명
            customerName="고객명",

            # 상품명
            itemName="상품명",

            # 주문번호
            orderNumber="주문번호",

            # 고객 메일주소
            email="test@test.com",

            # 고객 휴대폰번호
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        result = cashbillService.register(CorpNum, cashbill)

        return render(request, 'Cashbill/Register.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/Register.html', {'code': PE.code, 'message': PE.message})


def update(request):
    """
    1건의 현금영수증을 수정합니다.
    - [임시저장] 상태의 현금영수증만 수정할 수 있습니다.
    - 국세청에 신고된 현금영수증은 수정할 수 없으며, 취소 현금영수증을 발행하여 취소처리 할 수 있습니다.
    - 취소현금영수증 작성방법 안내 - http://blog.linkhub.co.kr/702
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 수정하고자하는 현금영수증 문서관리번호
        MgtKey = '20180118-003'

        # 현금영수증 정보
        cashbill = Cashbill(

            # [필수] 문서관리번호
            mgtKey=MgtKey,

            # [필수] 현금영수증 형태, [승인거래 / 취소거래]
            tradeType="승인거래",

            # [취소거래시 필수] 원본 현금영수증 국세청승인번호
            orgConfirmNum="",

            # [취소거래시 필수] 원본 현금영수증 거래일자
            orgTradeDate="",

            # [필수] 과세형태, [과세 / 비과세]
            taxationType="과세",

            # [필수] 거래유형, [소득공제용 /지출증빙용]
            tradeUsage="소득공제용",

            # [필수] 거래처 식별번호
            # 거래유형이 '지출증빙용' - [휴대폰/카드/주민등록/사업자] 번호 입력
            # 거래유형이 '소득공제용' - [휴대폰/카드/주민등록] 번호 입력
            # 자진발급 "010-000-1234" 의 경우 "소득공제용"으로만 발급 가능
            identityNum="010-000-1234",

            # [필수] 공급가액
            supplyCost="20000",

            # 세액
            tax="2000",

            # 봉사료
            serviceFee="0",

            # [필수] 거래금액, 공급가액+세액+봉사료
            totalAmount="22000",

            # 발행자 사업자번호
            franchiseCorpNum="1234567890",

            # 발행자 상호
            franchiseCorpName="발행자 상호_수정",

            # 발행자 대표자성명
            franchiseCEOName="발행 대표자 성명_수정",

            # 발행자 주소
            franchiseAddr="발행자 주소",

            # 발행자 연락처
            franchiseTEL="07012345678",

            # 고객명
            customerName="고객명",

            # 상품명
            itemName="상품명",

            # 주문번호
            orderNumber="주문번호",

            # 고객 메일주소
            email="test@test.com",

            # 고객 휴대폰번호
            hp="010111222",

            # 발행안내문자 전송여부
            smssendYN=False
        )

        result = cashbillService.update(CorpNum, MgtKey, cashbill)

        return render(request, 'Cashbill/Update.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/Update.html', {'code': PE.code, 'message': PE.message})


def issue(request):
    """
    1건의 임시저장 현금영수증을 발행처리합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자버놓
        CorpNum = settings.testCorpNum

        # 문서관리번호
        MgtKey = "20180118-004"

        # 메모
        Memo = "발행 메모"

        result = cashbillService.issue(CorpNum, MgtKey, Memo)

        return render(request, 'Cashbill/Issue.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/Issue.html', {'code': PE.code, 'message': PE.message})


def cancelIssue(request):
    """
    [발행완료] 상태의 현금영수증을 [발행취소] 합니다.
    - 발행취소는 국세청 전송전에만 가능합니다.
    - 발행취소된 형금영수증은 국세청에 전송되지 않습니다.
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-004"

        # 메모
        Memo = "발행취소 메모"

        result = cashbillService.cancelIssue(CorpNum, MgtKey, Memo)

        return render(request, 'Cashbill/CancelIssue.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/CancelIssue.html', {'code': PE.code, 'message': PE.message})


def delete(request):
    """
    1건의 현금영수증을 삭제합니다.
    - 현금영수증을 삭제하면 사용된 문서관리번호(mgtKey)를 재사용할 수 있습니다.
    - 삭제가능한 문서 상태 : [임시저장], [발행취소]
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-004"

        result = cashbillService.delete(CorpNum, MgtKey)

        return render(request, 'Cashbill/Delete.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/Delete.html', {'code': PE.code, 'message': PE.message})


def revokeRegistIssue(request):
    """
    1건의 취소현금영수증을 즉시발행합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책"을
      참조하시기 바랍니다.
    - 취소현금영수증 작성방법 안내 - http://blog.linkhub.co.kr/702
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20180118-005"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "315234938"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20180117"

        # 발행안내문자 전송여부
        smssendYN = False

        # 즉시발행 메모
        memo = "현금영수증 즉시발행 메모"

        result = cashbillService.revokeRegistIssue(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, memo,
                                                   UserID)

        return render(request, 'Cashbill/RevokeRegistIssue.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RevokeRegistIssue.html', {'code': PE.code, 'message': PE.message})


def revokeRegistIssue_part(request):
    """
    1건의 (부분) 취소현금영수증을 즉시발행합니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책"을
      참조하시기 바랍니다.
    - 취소현금영수증 작성방법 안내 - http://blog.linkhub.co.kr/702
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20180118-019"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "315234938"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20180117"

        # 발행안내문자 전송여부
        smssendYN = False

        # 즉시발행 메모
        memo = "현금영수증 즉시발행 메모"

        # 부분취소여부, true-부분취소 / false-전체취소
        isPartCancel = True

        # 취소사유, 1-거래취소, 2-오류발급취소, 3-기타
        cancelType = 1

        # [취소] 공급가액
        supplyCost = "10000"

        # [취소] 세액
        tax = "1000"

        # [취소] 봉사료
        serviceFee = "0"

        # [취소] 합계거래금액, 공급가액+세액+봉사료
        # 원본 현금영수증의 공급가액 이하만 가능
        totalAmount = "11000"

        result = cashbillService.revokeRegistIssue(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, memo,
                                                   UserID,
                                                   isPartCancel, cancelType, supplyCost, tax, serviceFee, totalAmount)

        return render(request, 'Cashbill/RevokeRegistIssue_part.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RevokeRegistIssue_part.html', {'code': PE.code, 'message': PE.message})


def revokeRegister(request):
    """
    1건의 취소현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 공급자별 고유번호 생성
        mgtKey = "20180118-43A"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "315234938"

        # [필수] 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20180117"

        # 발행안내문자 전송여부
        smssendYN = False

        result = cashbillService.revokeRegister(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, UserID)

        return render(request, 'Cashbill/RevokeRegister.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RevokeRegister.html', {'code': PE.code, 'message': PE.message})


def revokeRegister_part(request):
    """
    1건의 (부분) 취소현금영수증을 임시저장 합니다.
    - [임시저장] 상태의 현금영수증은 발행(Issue API)을 호출해야만 국세청에 전송됩니다.
    - 발행일 기준 오후 5시 이전에 발행된 현금영수증은 다음날 오후 2시에 국세청 전송결과를 확인할 수 있습니다.
    - 현금영수증 국세청 전송 정책에 대한 정보는 "[현금영수증 API 연동매뉴얼] > 1.4. 국세청 전송정책"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별 고유번호 생성
        mgtKey = "20180118-1233"

        # [필수] 원본현금영수증 국세청승인번호, 문서정보확인(GetInfo API)로 확인가능
        orgConfirmNum = "315234938"

        # 원본현금영수증 거래일자, 문서정보확인(GetInfo API)로 확인가능
        orgTradeDate = "20180117"

        # 발행안내문자 전송여부
        smssendYN = False

        # 부분취소여부, true-부분취소 / false-전체취소
        isPartCancel = True

        # 취소사유, 1-거래취소, 2-오류발급취소, 3-기타
        cancelType = 1

        # [취소] 공급가액
        supplyCost = "4000"

        # [취소] 세액
        tax = "400"

        # [취소] 봉사료
        serviceFee = "0"

        # [취소] 합계금액
        totalAmount = "4400"

        result = cashbillService.revokeRegister(CorpNum, mgtKey, orgConfirmNum, orgTradeDate, smssendYN, UserID,
                                                isPartCancel, cancelType, supplyCost, tax, serviceFee, totalAmount)

        return render(request, 'Cashbill/RevokeRegister_part.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RevokeRegister_part.html', {'code': PE.code, 'message': PE.message})


def getInfo(request):
    """
    1건의 현금영수증 상태/요약 정보를 확인합니다.
    - 응답항목에 대한 자세한 정보는 "[현금영수증 API 연동매뉴얼] > 4.2. 현금영수증 상태정보 구성"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180104001"

        cashbillInfo = cashbillService.getInfo(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetInfo.html', {'cashbillInfo': cashbillInfo})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetInfo.html', {'code': PE.code, 'message': PE.message})


def getInfos(request):
    """
    다수건의 현금영수증 상태/요약 정보를 확인합니다. (최대 1000건)
    - 응답항목에 대한 자세한 정보는 "[현금영수증 API 연동매뉴얼] > 4.2.
      현금영수증 상태정보 구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20170718-04")
        MgtKeyList.append("20161118-02")
        MgtKeyList.append("20161118-03")

        InfoList = cashbillService.getInfos(CorpNum, MgtKeyList)

        return render(request, 'Cashbill/Getinfos.html', {'InfoList': InfoList})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetInfos.html', {'code': PE.code, 'message': PE.message})


def getDetailInfo(request):
    """
    현금영수증 1건의 상세정보를 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[현금영수증 API 연동매뉴얼] > 4.1. 현금영수증 구성" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-019"

        cashbill = cashbillService.getDetailInfo(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetDetailInfo.html', {'cashbill': cashbill})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetDetailInfo.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 현금영수증 목록을 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[현금영수증 API 연동매뉴얼] > 4.2. 현금영수증 상태정보 구성" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 조회 일자유형, R-등록일자, T-거래일자, I-발행일자
        DType = "R"

        # 시작일자, 표시형식(yyyyMMdd)
        SDate = "20171201"

        # 종료일자, 표시형식(yyyyMMdd)
        EDate = "20180131"

        # 상태코드 배열, 2,3번째 자리에 와일드카드(*) 사용 가능
        State = ["3**", "4**"]

        # 현금영수증 형태, N-일반 현금영수증, C-취소 현금영수증
        TradeType = ["N", "C"]

        # 거래용도 배열, P-소득공제용, C-지출증빙용
        TradeUsage = ["P", "C"]

        # 과세형태 배열, T-과세, N-비과세
        TaxationType = ["T", "N"]

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향, D-내림차순, A-오름차순
        Order = "D"

        # 현금영수증 식별번호, 미기재시 전체조회
        QString = ""

        response = cashbillService.search(CorpNum, DType, SDate, EDate, State, TradeType,
                                          TradeUsage, TaxationType, Page, PerPage, Order, UserID, QString)

        return render(request, 'Cashbill/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'Cashbill/Search.html', {'code': PE.code, 'message': PE.message})


def getLogs(request):
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180104001"

        LogList = cashbillService.getLogs(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetLogs.html', {'LogList': LogList})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetLogs.html', {'code': PE.code, 'message': PE.message})


def getURL(request):
    """
    팝빌 현금영수증 관련 문서함 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # SBOX : 매출문서함, PBOX : 매입문서함 , TBOX : 임시문서함 , WRITE : 문서작성
        TOGO = "WRITE"

        url = cashbillService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'Cashbill/GetURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetURL.html', {'code': PE.code, 'message': PE.message})


def getPopUpURL(request):
    """
    1건의 현금영수증 보기 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180104001"

        url = cashbillService.getPopUpURL(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetPopUpURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPopUpURL.html', {'code': PE.code, 'message': PE.message})


def getPrintURL(request):
    """
    1건의 현금영수증 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180104001"

        url = cashbillService.getPrintURL(CorpNum, MgtKey)

        return render(request, 'Cashbill/GetPrintURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPrintURL.html', {'code': PE.code, 'message': PE.message})


def getEPrintURL(request):
    """
    현금영수증 인쇄(공급받는자) URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20150326-01"

        url = cashbillService.getEPrintURL(CorpNum, MgtKey)
        return render(request, 'Cashbill/GetEPrintURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetEPrintURL.html', {'code': PE.code, 'message': PE.message})


def getMassPrintURL(request):
    """
    다수건의 현금영수증 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서관리번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20180118-019")
        MgtKeyList.append("20180118-005")
        MgtKeyList.append("20180116-03")

        url = cashbillService.getMassPrintURL(CorpNum, MgtKeyList)
        return render(request, 'Cashbill/GetMassPrintURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetMassPrintURL.html', {'code': PE.code, 'message': PE.message})


def getMailURL(request):
    """
    공급받는자 메일링크 URL을 반환합니다.
    - 메일링크 URL은 유효시간이 존재하지 않습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-019"

        url = cashbillService.getMailURL(CorpNum, MgtKey)
        return render(request, 'Cashbill/GetMailURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetMailURL.html', {'code': PE.code, 'message': PE.message})

def getPopbillURL_LOGIN(request):
    """
    팝빌 관련 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-포인트충전
        TOGO = "LOGIN"

        url = cashbillService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'Cashbill/GetPopbillURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPopbillURL.html', {'code': PE.code, 'message': PE.message})


def sendEmail(request):
    """
    발행 안내메일을 재전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-019"

        # 수신 메일주소
        Receiver = "test@test.com"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = cashbillService.sendEmail(CorpNum, MgtKey, Receiver, UserID)

        return render(request, 'Cashbill/SendEmail.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/SendEmail.html', {'code': PE.code, 'message': PE.message})


def sendSMS(request):
    """
    알림문자를 전송합니다. (단문/SMS- 한글 최대 45자)
    - 알림문자 전송시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [전송내역] 탭에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-019"

        # 발신번호
        Sender = "07012345678"

        # 수신번호
        Receiver = "010111222"

        # 메시지내용, 메시지 길이가 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "현금영수증 문자메시지 전송 테스트"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = cashbillService.sendSMS(CorpNum, MgtKey, Sender, Receiver, Contents, UserID)

        return render(request, 'Cashbill/SendSMS.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/SendSMS.html', {'code': PE.code, 'message': PE.message})


def sendFAX(request):
    """
    현금영수증을 팩스전송합니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 현금영수증 문서관리번호
        MgtKey = "20180118-019"

        # 발신번호
        Sender = "07012345678"

        # 수신팩스번호
        Receiver = "070111222"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = cashbillService.sendFAX(CorpNum, MgtKey, Sender, Receiver, UserID)
        return render(request, 'Cashbill/SendFAX.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/SendFAX.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금이 아닌 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API)를
      통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        balance = cashbillService.getBalance(CorpNum)

        return render(request, 'Cashbill/GetBalance.html', {'balance': balance})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetBalance.html', {'code': PE.code, 'message': PE.message})


def getPopbillURL_CHRG(request):
    """
    팝빌 관련 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-포인트충전
        TOGO = "CHRG"

        url = cashbillService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'Cashbill/GetPopbillURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPopbillURL.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를
      이용하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        balance = cashbillService.getPartnerBalance(CorpNum)

        return render(request, 'Cashbill/GetPartnerBalance.html', {'balance': balance})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPartnerBalance.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-포인트충전
        TOGO = "CHRG"

        url = cashbillService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'Cashbill/GetPartnerURL.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetPartnerURL.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    현금영수증 발행단가를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        unitCost = cashbillService.getUnitCost(CorpNum)

        return render(request, 'Cashbill/GetUnitCost.html', {'unitCost': unitCost})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetUnitCost.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 현금영수증 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getChargeInfo(CorpNum, UserID)

        return render(request, 'Cashbill/GetChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetChargeInfo.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 조회할 사업자등록번호, '-' 제외 10자리
        targetCorpNum = "1234567890"

        result = cashbillService.checkIsMember(targetCorpNum)

        return render(request, 'Cashbill/CheckIsMember.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/CheckIsMember.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    팝빌 회원아이디 중복여부를 확인합니다.
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = cashbillService.checkID(memberID)

        return render(request, 'Cashbill/CheckID.html', {'response': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/CheckID.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    팝빌 연동회원 가입을 요청합니다.
    """
    try:
        # 회원정보
        newMember = JoinForm(

            # 회원아이디, 최대 20자
            ID="testkorea1123",

            # 비밀번호, 최대 20자
            PWD="testpasswodrd",

            # 사업자번호
            CorpNum="0000000102",

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
            ContactTEL="070-1111-1234",

            # 담당자 휴대폰번호
            ContactHP="010-2222-3333",

            # 담당자 팩스번호
            ContactFAX="070-4304-2991",

            # 담당자 메일주소
            ContactEmail="test@test.com"
        )

        result = cashbillService.joinMember(newMember)

        return render(request, 'Cashbill/JoinMember.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/JoinMember.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.getCorpInfo(CorpNum, UserID)

        return render(request, 'Cashbill/GetCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'Cashbill/GetCorpInfo.html', {'code': PE.code, 'message': PE.message})


def updateCorpInfo(request):
    """
    회사정보를 수정합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 회사정보
        corpInfo = CorpInfo(

            # 대표자성명
            ceoname="대표자성명_수정",

            # 상호
            corpName="상호_수정",

            # 주소
            addr="주소_수정",

            # 업태
            bizType="업태_수정",

            # 종목
            bizClass="종목_수"
        )

        result = cashbillService.updateCorpInfo(CorpNum, corpInfo, UserID)
        return render(request, 'Cashbill/UpdateCorpInfo.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/UpdateCorpInfo.html', {'code': PE.code, 'message': PE.message})


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
            id="testkorea_cash",

            # 비밀번호
            pwd="thisispassword_cash",

            # 담당자명
            personName="신규담당자",

            # 연락처
            tel="010-1234-1234",

            # 휴대폰번호
            hp="010-1234-1234",

            # 팩스번호
            fax="070-1234-1234",

            # 메일주소
            email="test@test.comr",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True
        )

        result = cashbillService.registContact(CorpNum, newContact, UserID)

        return render(request, 'Cashbill/RegistContact.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/RegistContact.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = cashbillService.listContact(CorpNum, UserID)

        return render(request, 'Cashbill/Listcontact.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'Cashbill/ListContact.html', {'code': PE.code, 'message': PE.message})


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
            id="testkorea_cash",

            # 담당자 성명
            personName="담당자 성명_수정",

            # 연락처
            tel="010-1234-1234",

            # 휴대폰번호
            hp="010-8888-7777",

            # 팩스번호
            fax="070-1234-1234",

            # 메일주소
            email="test@test.com",

            # 회사조회 여부, True-회사조회, False-개인조회
            searchAllAllowYN=True
        )

        result = cashbillService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'Cashbill/UpdateContact.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'Cashbill/UpdateContact.html', {'code': PE.code, 'message': PE.message})
