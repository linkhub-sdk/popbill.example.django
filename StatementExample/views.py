# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import (
    ContactInfo,
    CorpInfo,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
    Statement,
    StatementDetail,
    StatementService,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 StatementService 객체 생성
statementService = StatementService(settings.LinkID, settings.SecretKey)

# 연동환경 설정, 개발용(True), 상업용(False)
statementService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
statementService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
statementService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, 권장(True)
statementService.UseLocalTimeYN = settings.UseLocalTimeYN


def index(request):
    return render(request, "Statement/Index.html", {})


def checkMgtKeyInUse(request):
    """
    파트너가 전자명세서 관리 목적으로 할당하는 문서번호의 사용여부를 확인합니다.
    - 이미 사용 중인 문서번호는 중복 사용이 불가하고, 전자명세서가 삭제된 경우에만 문서번호의 재사용이 가능합니다.
    - https://developers.popbill.com/reference/statement/python/api/info#CheckMgtKeyInUse
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 발신자별 고유번호 생성
        MgtKey = "20220805-001"

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        bIsInUse = statementService.checkMgtKeyInUse(CorpNum, ItemCode, MgtKey)
        if bIsInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registIssue(request):
    """
    작성된 전자명세서 데이터를 팝빌에 저장과 동시에 발행하여, "발행완료" 상태로 처리합니다.
    - 팝빌 사이트 [전자명세서] > [환경설정] > [전자명세서 관리] 메뉴의 발행시 자동승인 옵션 설정을 통해
        전자명세서를 "발행완료" 상태가 아닌 "승인대기" 상태로 발행 처리 할 수 있습니다.
    - 전자명세서 발행 함수 호출시 수신자에게 발행 안내 메일이 발송됩니다.
    - https://developers.popbill.com/reference/statement/python/api/issue#RegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 메모
        Memo = "즉시발행 메모"

        # 안내메일 제목, 미기재시 기본양식으로 전송
        EmailSubject = ""

        # 전자명세서 정보
        statement = Statement(
            # 작성일자 yyyyMMdd
            writeDate="20220805",
            # [영수 / 청구 / 없음] 중 기재
            purposeType="영수",
            # 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",
            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",
            # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,
            # 전자명세서 문서번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20220805-002",
            # 발신자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,
            # 발신자 상호
            senderCorpName="발신자 상호",
            # 발신자 주소
            senderAddr="발신자 주소",
            # 발신자 대표자 성명
            senderCEOName="발신자 대표자 성명",
            # 발신자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",
            # 발신자 종목
            senderBizClass="종목",
            # 발신자 업태
            senderBizType="업태",
            # 발신자 담당자 성명
            senderContactName="발신자 담당자명",
            # 발신자 메일주소
            senderEmail="",
            # 발신자 연락처
            senderTEL="",
            # 발신자 휴대폰번호
            senderHP="",
            # 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",
            # 수신자 상호
            receiverCorpName="수신자 상호",
            # 수신자 대표자 성명
            receiverCEOName="수신자 대표자 성명",
            # 수신자 주소
            receiverAddr="수신자 주소",
            # 수신자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",
            # 수신자 종목
            receiverBizClass="수신자 종목",
            # 수신자 업태
            receiverBizType="수신자 업태",
            # 수신자 담당자 성명
            receiverContactName="수신자 담당자명",
            # 수신자 메일주소
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            receiverEmail="",
            # 수신자 연락처
            receiverTEL="",
            # 수신자 휴대폰번호
            receiverHP="",
            # 공급가액 합계
            supplyCostTotal="20000",
            # 세액 합계
            taxTotal="2000",
            # 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",
            # 기재 상 '일련번호' 항목
            serialNum="123",
            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            "Balance": "20000",  # 전잔액
            "Deposit": "5000",  # 입금액
            "CBalance": "25000",  # 현잔액
        }

        Memo = ""

        response = statementService.registIssue(
            CorpNum, statement, Memo, UserID,  EmailSubject
        )

        return render(
            request,
            "response.html",
            {
                "code": response.code,
                "message": response.message,
                "invoiceNum": response.invoiceNum,
            },
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def register(request):
    """
    작성된 전자명세서 데이터를 팝빌에 저장합니다.
    - "임시저장" 상태의 전자명세서는 발행(Issue API) 함수를 호출하여 "발행완료" 처리한 경우에만 수신자에게 발행 안내 메일이 발송됩니다.
    - https://developers.popbill.com/reference/statement/python/api/issue#Register
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자명세서 정보
        statement = Statement(
            # 작성일자 yyyyMMdd
            writeDate="20220805",
            # [영수 / 청구 / 없음] 중 기재
            purposeType="영수",
            # 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",
            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",
            # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,
            # 전자명세서 문서번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20222805-001",
            # 발신자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,
            # 발신자 상호
            senderCorpName="발신자 상호",
            # 발신자 주소
            senderAddr="발신자 주소",
            # 발신자 대표자 성명
            senderCEOName="발신자 대표자 성명",
            # 발신자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",
            # 발신자 종목
            senderBizClass="종목",
            # 발신자 업태
            senderBizType="업태",
            # 발신자 담당자 성명
            senderContactName="발신자 담당자명",
            # 발신자 메일주소
            senderEmail="",
            # 발신자 연락처
            senderTEL="",
            # 발신자 휴대폰번호
            senderHP="",
            # 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",
            # 수신자 상호
            receiverCorpName="수신자 상호",
            # 수신자 대표자 성명
            receiverCEOName="수신자 대표자 성명",
            # 수신자 주소
            receiverAddr="수신자 주소",
            # 수신자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",
            # 수신자 종목
            receiverBizClass="수신자 종목",
            # 수신자 업태
            receiverBizType="수신자 업태",
            # 수신자 담당자 성명
            receiverContactName="수신자 담당자명",
            # 수신자 메일주소
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            receiverEmail="",
            # 수신자 연락처
            receiverTEL="",
            # 수신자 휴대폰번호
            receiverHP="",
            # 공급가액 합계
            supplyCostTotal="20000",
            # 세액 합계
            taxTotal="2000",
            # 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",
            # 기재 상 '일련번호' 항목
            serialNum="123",
            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            "Balance": "20000",  # 전잔액
            "Deposit": "5000",  # 입금액
            "CBalance": "25000",  # 현잔액
        }

        response = statementService.register(CorpNum, statement)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def update(request):
    """
    "임시저장" 상태의 전자명세서를 수정합니다.
    - https://developers.popbill.com/reference/statement/python/api/issue#Update
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 수정할 전자명세서 문서번호
        mgtKey = "20220805-001"

        # 전자명세서 정보
        statement = Statement(
            # 작성일자 yyyyMMdd
            writeDate="20220805",
            # [영수 / 청구 / 없음] 중 기재
            purposeType="영수",
            # 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",
            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",
            # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=ItemCode,
            # 전자명세서 문서번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey=mgtKey,
            # 발신자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,
            # 발신자 상호
            senderCorpName="발신자 상호_수정",
            # 발신자 주소
            senderAddr="발신자 주소",
            # 발신자 대표자 성명
            senderCEOName="발신자 대표자 성명",
            # 발신자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",
            # 발신자 종목
            senderBizClass="종목",
            # 발신자 업태
            senderBizType="업태",
            # 발신자 담당자 성명
            senderContactName="발신자 담당자명",
            # 발신자 메일주소
            senderEmail="",
            # 발신자 연락처
            senderTEL="",
            # 발신자 휴대폰번호
            senderHP="",
            # 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",
            # 수신자 상호
            receiverCorpName="수신자 상호",
            # 수신자 대표자 성명
            receiverCEOName="수신자 대표자 성명",
            # 수신자 주소
            receiverAddr="수신자 주소",
            # 수신자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",
            # 수신자 종목
            receiverBizClass="수신자 종목",
            # 수신자 업태
            receiverBizType="수신자 업태",
            # 수신자 담당자 성명
            receiverContactName="수신자 담당자명",
            # 수신자 메일주소
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            receiverEmail="",
            # 수신자 연락처
            receiverTEL="",
            # 수신자 휴대폰번호
            receiverHP="",
            # 공급가액 합계
            supplyCostTotal="20000",
            # 세액 합계
            taxTotal="2000",
            # 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",
            # 기재 상 '일련번호' 항목
            serialNum="123",
            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20220805",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000",  # 세액
                remark="비고",  # 비고
                spare1="여분1",  # 여분1
                spare2="여분2",  # 여분2
                spare3="여분3",  # 여분3
                spare4="여분4",  # 여분4
                spare5="여분5",  # 여분5
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            "Balance": "20000",  # 전잔액
            "Deposit": "5000",  # 입금액
            "CBalance": "25000",  # 현잔액
        }

        response = statementService.update(CorpNum, ItemCode, mgtKey, statement)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def issue(request):
    """
    "임시저장" 상태의 전자명세서를 발행하여, "발행완료" 상태로 처리합니다.
    - 팝빌 사이트 [전자명세서] > [환경설정] > [전자명세서 관리] 메뉴의 발행시 자동승인 옵션 설정을 통해
        전자명세서를 "발행완료" 상태가 아닌 "승인대기" 상태로 발행 처리 할 수 있습니다.
    - 전자명세서 발행 함수 호출시 수신자에게 발행 안내 메일이 발송됩니다.
    - https://developers.popbill.com/reference/statement/python/api/issue#Issue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20222805-001"

        # 전자명세서 발행 안내메일 제목
        EmailSubject = ""

        # 전자명세서 상태 이력을 관리하기 위한 메모
        Memo = ""

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.issue(CorpNum, ItemCode, MgtKey,  Memo, EmailSubject, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def cancel(request):
    """
    발신자가 발행한 전자명세서를 발행취소합니다.
    - "발행취소" 상태의 전자명세서를 삭제(Delete API) 함수를 이용하면, 전자명세서 관리를 위해 부여했던 문서번호를 재사용 할 수 있습니다.
    - https://developers.popbill.com/reference/statement/python/api/issue#Cancel
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 메모
        Memo = "발행취소 메모"

        response = statementService.cancel(CorpNum, ItemCode, MgtKey, Memo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def delete(request):
    """
    삭제 가능한 상태의 전자명세서를 삭제합니다.
    - 삭제 가능한 상태: "임시저장", "취소", "승인거부", "발행취소"
    - https://developers.popbill.com/reference/statement/python/api/issue#Delete
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        response = statementService.delete(CorpNum, ItemCode, MgtKey)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfo(request):
    """
    전자명세서의 1건의 상태 및 요약정보 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/info#GetInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        statementInfo = statementService.getInfo(CorpNum, ItemCode, MgtKey)

        return render(
            request, "Statement/GetInfo.html", {"statementInfo": statementInfo}
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfos(request):
    """
    다수건의 전자명세서 상태/요약 정보를 확인합니다. (1회 호출 시 최대 1,000건 확인 가능)
    - https://developers.popbill.com/reference/statement/python/api/info#GetInfos
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 문서번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")

        InfoList = statementService.getInfos(CorpNum, ItemCode, MgtKeyList)

        return render(request, "Statement/GetInfos.html", {"InfoList": InfoList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getDetailInfo(request):
    """
    전자명세서 1건의 상세정보 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/info#GetDetailInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        statement = statementService.getDetailInfo(CorpNum, ItemCode, MgtKey)

        return render(request, "Statement/GetDetailInfo.html", {"statement": statement})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    검색조건에 해당하는 세금계산서를 조회합니다. (조회기간 단위 : 최대 6개월)
    - https://developers.popbill.com/reference/statement/python/api/info#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 일자유형, R-등록일시, W-작성일자, I-발행일시 중 택 1
        DType = "W"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        # 전자명세서 상태코드 배열 (2,3번째 자리에 와일드카드(*) 사용 가능)
        # - 미입력시 전체조회
        State = ["2**", "3**"]

        # 전자명세서 문서유형 배열 (121 , 122 , 123 , 124 , 125 , 126 중 선택. 다중 선택 가능)
        # 121 = 명세서 , 122 = 청구서 , 123 = 견적서
        # 124 = 발주서 , 125 = 입금표 , 126 = 영수증
        ItemCode = ["121", "122", "123", "124", "125", "126"]

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향 D-내림차순, A-오름차순
        Order = "D"

        # 통합검색어, 거래처 상호명 또는 거래처 사업자번호로 조회
        # - 미입력시 전체조회
        QString = ""

        response = statementService.search(CorpNum,DType,SDate,EDate,State,ItemCode,Page,PerPage,Order,UserID,QString)

        return render(request, "Statement/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getLogs(request):
    """
    전자명세서의 상태에 대한 변경이력을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/info#GetLogs
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        LogList = statementService.getLogs(CorpNum, ItemCode, MgtKey)

        return render(request, "Statement/GetLogs.html", {"LogList": LogList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getURL(request):
    """
    로그인 상태로 팝빌 사이트의 전자명세서 문서함 메뉴에 접근할 수 있는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/info#GetURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # TBOX-임시 문서함, SBOX-발행 문서함
        TOGO = "TBOX"

        url = statementService.getURL(CorpNum, UserID, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPopUpURL(request):
    """
    전자명세서 1건의 상세 정보 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetPopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        url = statementService.getPopUpURL(CorpNum, ItemCode, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getViewURL(request):
    """
    전자명세서 1건의 보기 팝업 URL을 반환합니다. (팝빌 사이트의 상단, 좌측 메뉴 및 버튼 제외)
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetViewURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        url = statementService.getViewURL(CorpNum, ItemCode, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPrintURL(request):
    """
    전자명세서 1건을 인쇄하기 위한 페이지의 팝업 URL을 반환하며, 페이지내에서 인쇄 설정값을 "공급자" / "공급받는자" / "공급자+공급받는자"용 중 하나로 지정할 수 있습니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        url = statementService.getPrintURL(CorpNum, ItemCode, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getEPrintURL(request):
    """
    "공급받는자" 용 전자명세서 1건을 인쇄하기 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - 전자명세서의 공급받는자는 "수신자"를 나타내는 용어입니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetEPrintURL
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        url = statementService.getEPrintURL(CorpNum, ItemCode, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMassPrintURL(request):
    """
    다수건의 전자명세서를 인쇄하기 위한 페이지의 팝업 URL을 반환합니다. (최대 100건)
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetMassPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 인쇄할 문서번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")

        url = statementService.getMassPrintURL(CorpNum, ItemCode, MgtKeyList, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMailURL(request):
    """
    전자명세서 안내메일의 상세보기 링크 URL을 반환합니다.
    - 함수 호출로 반환 받은 URL에는 유효시간이 없습니다.
    - https://developers.popbill.com/reference/statement/python/api/view#GetMailURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        url = statementService.getMailURL(CorpNum, ItemCode, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌 사이트에 로그인 상태로 접근할 수 있는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSealURL(request):
    """
    전자명세서에 첨부할 인감, 사업자등록증, 통장사본을 등록하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#GetSealURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getSealURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def attachFile(request):
    """
    "임시저장" 상태의 명세서에 1개의 파일을 첨부합니다. (최대 5개)
    - https://developers.popbill.com/reference/statement/python/api/etc#AttachFile
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 파일경로
        FilePath = "./StatementExample/static/image/attachfile.png"

        response = statementService.attachFile(CorpNum, ItemCode, MgtKey, FilePath)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def deleteFile(request):
    """
    "임시저장" 상태의 전자명세서에 첨부된 1개의 파일을 삭제합니다.
    - 파일을 식별하는 파일아이디는 첨부파일 목록(GetFiles API) 의 응답항목 중 파일아이디(AttachedFile) 값을 통해 확인할 수 있습니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#DeleteFile
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 삭제할 FileID, 첨부파일목록(getFiles API) 응답 전문의 attachedFile 값
        FileID = "0DD20B73-5654-488E-A683-0ABED95C7D07.PBF"

        response = statementService.deleteFile(CorpNum, ItemCode, MgtKey, FileID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFiles(request):
    """
    전자명세서에 첨부된 파일목록을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#GetFiles
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        fileList = statementService.getFiles(CorpNum, ItemCode, MgtKey)

        return render(request, "Statement/GetFiles.html", {"fileList": fileList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendEmail(request):
    """
    "승인대기", "발행완료" 상태의 전자명세서와 관련된 발행 안내 메일을 재전송 합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#SendEmail
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 수신메일주소
        ReceiverMail = ""

        response = statementService.sendEmail(CorpNum, ItemCode, MgtKey, ReceiverMail)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendSMS(request):
    """
    전자명세서와 관련된 안내 SMS(단문) 문자를 재전송하는 함수로, 팝빌 사이트 [문자·팩스] > [문자] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 메시지는 최대 90byte까지 입력 가능하고, 초과한 내용은 자동으로 삭제되어 전송합니다. (한글 최대 45자)
    - 함수 호출시 포인트가 과금됩니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#SendSMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 발신번호
        Sender = ""

        # 수신번호
        Receiver = ""

        # 문자메시지내용, 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "전자명세서 API 문자메시지 테스트"

        response = statementService.sendSMS(CorpNum, ItemCode, MgtKey, Sender, Receiver, Contents)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAX(request):
    """
    전자명세서를 팩스로 전송하는 함수로, 팝빌 사이트 [문자·팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 함수 호출시 포인트가 과금됩니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서번호
        MgtKey = "20220805-002"

        # 발신번호
        Sender = ""

        # 수신번호
        Receiver = ""

        response = statementService.sendFAX(CorpNum, ItemCode, MgtKey, Sender, Receiver)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def FAXSend(request):
    """
    전자명세서를 팩스로 전송하는 함수로, 팝빌에 데이터를 저장하는 과정이 없습니다.
    - 팝빌 사이트 [문자·팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 함수 호출시 포인트가 과금됩니다.
    - 팩스 발행 요청시 작성한 문서번호는 팩스전송 파일명으로 사용됩니다.
    - 팩스 전송결과를 확인하기 위해서는 선팩스 전송 요청 시 반환받은 접수번호를 이용하여 팩스 API의 전송결과 확인 (GetFaxResult) API를 이용하면 됩니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#FAXSend
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스발신번호
        SendNum = ""

        # 팩스수신번호
        ReceiveNum = ""

        # 전자명세서 정보
        statement = Statement(
            # 작성일자 yyyyMMdd
            writeDate="20220805",

            # [영수 / 청구 / 없음] 중 기재
            purposeType="영수",

            # 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # 전자명세서 문서번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20220805-100",

            # 발신자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,

            # 발신자 상호
            senderCorpName="발신자 상호",

            # 발신자 주소
            senderAddr="발신자 주소",

            # 발신자 대표자 성명
            senderCEOName="발신자 대표자 성명",

            # 발신자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",

            # 발신자 종목
            senderBizClass="종목",

            # 발신자 업태
            senderBizType="업태",

            # 발신자 담당자 성명
            senderContactName="발신자 담당자명",

            # 발신자 메일주소
            senderEmail="",

            # 발신자 연락처
            senderTEL="",

            # 발신자 휴대폰번호
            senderHP="",

            # 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 수신자 상호
            receiverCorpName="수신자 상호",

            # 수신자 대표자 성명
            receiverCEOName="수신자 대표자 성명",

            # 수신자 주소
            receiverAddr="수신자 주소",

            # 수신자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",

            # 수신자 종목
            receiverBizClass="수신자 종목",

            # 수신자 업태
            receiverBizType="수신자 업태",

            # 수신자 담당자 성명
            receiverContactName="수신자 담당자명",

            # 수신자 메일주소
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            receiverEmail="",

            # 수신자 연락처
            receiverTEL="",

            # 수신자 휴대폰번호
            receiverHP="",

            # 공급가액 합계
            supplyCostTotal="20000",

            # 세액 합계
            taxTotal="2000",

            # 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",

            # 기재 상 '일련번호' 항목
            serialNum="123",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,

            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                # 일련번호, 1부터 순차기재
                serialNum=1,

                # 품목
                itemName="품목1",

                # 거래일자
                purchaseDT="20220805",

                # 규격
                spec="BOX",

                # 단가
                unitCost="10000",

                # 수량
                qty=1,

                # 공급가액
                supplyCost="10000",

                # 세액
                tax="1000",
            )
        )
        statement.detailList.append(
            StatementDetail(
                # 일련번호, 1부터 순차기재
                serialNum=2,

                # 품목
                itemName="품목1",

                # 거래일자
                purchaseDT="20220805",

                # 규격
                spec="BOX",

                # 단가
                unitCost="10000",

                # 수량
                qty=1,

                # 공급가액
                supplyCost="10000",

                # 세액
                tax="1000",
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            # 전잔액
            "Balance": "20000",

            # 입금액
            "Deposit": "5000",

            # 현잔액
            "CBalance": "25000",
        }

        result = statementService.FAXSend(CorpNum, statement, SendNum, ReceiveNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def attachStatement(request):
    """
    하나의 전자명세서에 다른 전자명세서를 첨부합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#AttachStatement
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        # 첨부할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부할 전자명세서 문서번호
        SubMgtKey = "20220805-002"

        response = statementService.attachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def detachStatement(request):
    """
    하나의 전자명세서에 첨부된 다른 전자명세서를 해제합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#DetachStatement
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서번호
        MgtKey = "20220805-001"

        # 첨부해제할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부해제할 전자명세서 문서번호
        SubMgtKey = "20220805-002"

        response = statementService.detachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listEmailConfig(request):
    """
    전자명세서 관련 메일 항목에 대한 발송설정을 확인합니다.
    https://developers.popbill.com/reference/statement/python/api/etc#ListEmailConfig
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        EmailConfig = statementService.listEmailConfig(CorpNum)

        return render(request, "Statement/ListEmailConfig.html", {"EmailConfig": EmailConfig})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateEmailConfig(request):
    """
    전자명세서 관련 메일 항목에 대한 발송설정을 수정합니다.
    - https://developers.popbill.com/reference/statement/python/api/etc#UpdateEmailConfig

    메일전송유형
    SMT_ISSUE : 수신자에게 전자명세서가 발행 되었음을 알려주는 메일입니다.
    SMT_ACCEPT : 발신자에게 전자명세서가 승인 되었음을 알려주는 메일입니다.
    SMT_DENY : 발신자에게 전자명세서가 거부 되었음을 알려주는 메일입니다.
    SMT_CANCEL : 수신자에게 전자명세서가 취소 되었음을 알려주는 메일입니다.
    SMT_CANCEL_ISSUE : 수신자에게 전자명세서가 발행취소 되었음을 알려주는 메일입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 메일 전송 유형
        EmailType = "SMT_ISSUE"

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        response = statementService.updateEmailConfig(CorpNum, EmailType, SendYN)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = statementService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = statementService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = statementService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUnitCost(request):
    """
    전자명세서 발행시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 확인할 전자명세서의 유형 코드 : 121 / 122 / 123 / 124 / 125 / 126 중 택 1
        # └ 121 = 거래명세서, 122 = 청구서, 123 = 견적서, 124 = 발주서, 125 = 입금표, 126 = 영수증
        ItemCode = 121

        result = statementService.getUnitCost(CorpNum, ItemCode)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 전자명세서 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 확인할 전자명세서의 유형 코드 : 121 / 122 / 123 / 124 / 125 / 126 중 택 1
        # └ 121 = 거래명세서, 122 = 청구서, 123 = 견적서, 124 = 발주서, 125 = 입금표, 126 = 영수증
        ItemCode = 121

        response = statementService.getChargeInfo(CorpNum, ItemCode)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#PaymentRequest
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

        response = statementService.paymentRequest(CorpNum,paymentForm, UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetPaymentHistory
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

        response = statementService.getPaymentHistory(CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetUseHistory
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

        response = statementService.getUseHistory(CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#Refund
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 환불신청 객체정보
        refundForm = RefundForm(
            # 담당자명
            contactname="환불신청테스트",

            # 담당자 연락처
            tel="01077777777",

            # 환불 신청 포인트
            requestpoint="10",

            # 은행명
            accountbank="국민",

            # 계좌번호
            accountnum="123123123-123",

            # 예금주명
            accountname="예금주",

            # 환불사유
            reason="테스트 환불 사유",
        )

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response =  statementService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/statement/python/api/point#GetRefundHistory
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

        response = statementService.getRefundHistory(CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = statementService.checkIsMember(CorpNum)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = statementService.checkID(memberID)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#JoinMember
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

        response = statementService.joinMember(newMember)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = statementService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#UpdateCorpInfo
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

        response = statementService.updateCorpInfo(CorpNum, corpInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#RegistContact
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

        response = statementService.registContact(CorpNum, newContact)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = statementService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = statementService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#UpdateContact
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

        response = statementService.updateContact(CorpNum, updateInfo)

        return render(request,"response.html",{"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def quitMember(request):
    """
    가입된 연동회원의 탈퇴를 요청합니다.
    회원탈퇴 신청과 동시에 팝빌의 모든 서비스 이용이 불가하며, 관리자를 포함한 모든 담당자 계정도 일괄탈퇴 됩니다.
    회원탈퇴로 삭제된 데이터는 복원이 불가능합니다.
    관리자 계정만 사용 가능합니다.
    - https://developers.popbill.com/reference/statement/python/api/member#QuitMember
    """
    try:
        CorpNum = settings.testCorpNum
        QuitReason = "테스트 탈퇴 사유"
        UserID = settings.testUserID

        response = statementService.quitMember(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundInfo(request):
    """
    포인트 환불에 대한 상세정보 1건을 확인합니다.
    - https://developers.popbill.com/reference/statement/python/api/point#GetRefundInfo
    """
    try:
        CorpNum = settings.testCorpNum
        RefundCode = "023040000017"
        UserID = settings.testUserID

        response = statementService.getRefundableResult(CorpNum,RefundCode,UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})

def getRefundableBalance(request):
    """
    환불 가능한 포인트를 확인합니다. (보너스 포인트는 환불가능포인트에서 제외됩니다.)
    - https://developers.popbill.com/reference/statement/python/api/point#GetRefundableBalance
    """
    try:
        CorpNum = settings.testCorpNum
        UserID = settings.testUserID

        refundableBalance = statementService.getRefundableBalance(CorpNum, UserID)
        return render(request, 'getRefundableBalance.html', {"refundableBalance": refundableBalance})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})
