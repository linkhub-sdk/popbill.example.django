# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import StatementService, PopbillException, Statement, StatementDetail, JoinForm, ContactInfo, CorpInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 StatementService 객체 생성
statementService = StatementService(settings.LinkID, settings.SecretKey)

# 연동환경 설정, 개발용(True), 상업용(False)
statementService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Statement/Index.html', {})


def checkMgtKeyInUse(request):
    """
    전자명세서 관리번호 중복여부를 확인합니다.
    - 관리번호는 1~24자리로 숫자, 영문 '-', '_' 조합으로 구성할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 발신자별 고유번호 생성
        MgtKey = "20190116-001"

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        bIsInUse = statementService.checkMgtKeyInUse(CorpNum, ItemCode, MgtKey)
        if bIsInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registIssue(request):
    """
    1건의 전자명세서를 즉시발행합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 메모
        Memo = "즉시발행 메모"

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20190116",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20190116-300",

            # [필수] 발신자 사업자번호, '-' 제외 10자리
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
            senderEmail="test@test.com",

            # 발신자 연락처
            senderTEL="070-1234-1234",

            # 발신자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 수신자 상호
            receiverCorpName="수신자 상호",

            # [필수] 수신자 대표자 성명
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
            receiverEmail="test@test.com",

            # 수신자 연락처
            receiverTEL="070111222",

            # 수신자 휴대폰번호
            receiverHP="010-111-222",

            # [필수] 공급가액 합계
            supplyCostTotal="20000",

            # [필수] 세액 합계
            taxTotal="2000",

            # [필수] 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",

            # 기재 상 '일련번호' 항목
            serialNum="123",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 사업자등록증 이미지 첨부 여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부 여부
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            'Balance': "20000",  # 전잔액
            'Deposit': "5000",  # 입금액
            'CBalance': "25000"  # 현잔액
        }

        response = statementService.registIssue(CorpNum, statement, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def register(request):
    """
    전자명세서 1건을 임시저장합니다.
    - 임시저장 상태의 명세서는 발행(Issue API)을 호출해야 수신자에게 메일이 전송됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20190116",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20190116-002",

            # [필수] 발신자 사업자번호, '-' 제외 10자리
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
            senderEmail="test@test.com",

            # 발신자 연락처
            senderTEL="070-1234-1234",

            # 발신자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # [필수] 수신자 상호
            receiverCorpName="수신자 상호",

            # [필수] 수신자 대표자 성명
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

            # 수신자  메일주소
            receiverEmail="test@test.com",

            # 수신자 연락처
            receiverTEL="070111222",

            # 수신자 휴대폰번호
            receiverHP="010-111-222",

            # [필수] 공급가액 합계
            supplyCostTotal="20000",

            # [필수] 세액 합계
            taxTotal="2000",

            # [필수] 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",

            # 기재 상 '일련번호' 항목
            serialNum="123",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 사업자등록증 이미지 첨부 여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부 여부
            bankBookYN=False,

        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            'Balance': "20000",  # 전잔액
            'Deposit': "5000",  # 입금액
            'CBalance': "25000"  # 현잔액
        }

        response = statementService.register(CorpNum, statement)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def update(request):
    """
    1건의 전자명세서를 수정합니다.
    - [임시저장] 상태의 전자명세서만 수정할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 수정할 전자명세서 문서관리번호
        mgtKey = "20190116-002"

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20190116",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=ItemCode,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey=mgtKey,

            # [필수] 발신자 사업자번호, '-' 제외 10자리
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
            senderEmail="test@test.com",

            # 발신자 연락처
            senderTEL="070-1234-1234",

            # 발신자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # [필수] 수신자 상호
            receiverCorpName="수신자 상호",

            # [필수] 수신자 대표자 성명
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
            receiverEmail="test@test.com",

            # 수신자 연락처
            receiverTEL="070111222",

            # 수신자 휴대폰번호
            receiverHP="010-111-222",

            # [필수] 공급가액 합계
            supplyCostTotal="20000",

            # [필수] 세액 합계
            taxTotal="2000",

            # [필수] 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",

            # 기재 상 '일련번호' 항목
            serialNum="123",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 사업자등록증 이미지 첨부 여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부 여부
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            'Balance': "20000",  # 전잔액
            'Deposit': "5000",  # 입금액
            'CBalance': "25000"  # 현잔액
        }

        response = statementService.update(CorpNum, ItemCode, mgtKey, statement)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def issue(request):
    """
    1건의 [임시저장] 상태의 전자명세서를 발행처리합니다.
    - 발행시 포인트가 차감됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        response = statementService.issue(CorpNum, ItemCode, MgtKey)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancel(request):
    """
    1건의 전자명세서를 [발행취소] 처리합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 메모
        Memo = "발행취소 메모"

        response = statementService.cancel(CorpNum, ItemCode, MgtKey, Memo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def delete(request):
    """
    1건의 전자명세서를 삭제합니다.
    - 전자명세서를 삭제하면 사용된 문서관리번호(mgtKey)를 재사용할 수 있습니다.
    - 삭제가능한 문서 상태 : [임시저장], [발행취소]
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        response = statementService.delete(CorpNum, ItemCode, MgtKey)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfo(request):
    """
    1건의 전자명세서 상태/요약 정보를 확인합니다.
    - 응답항목에 대한 자세한 정보는 "[전자명세서 API 연동매뉴얼] > 3.3.1.
      GetInfo (상태 확인)"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        statementInfo = statementService.getInfo(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetInfo.html', {'statementInfo': statementInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfos(request):
    """
    다수건의 전자명세서 상태/요약 정보를 확인합니다.
    - 응답항목에 대한 자세한 정보는 "[전자명세서 API 연동매뉴얼] > 3.3.2. GetInfos (상태 대량 확인)"
     을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 문서관리번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20190116-001")
        MgtKeyList.append("20190116-002")
        MgtKeyList.append("20190116-003")

        InfoList = statementService.getInfos(CorpNum, ItemCode, MgtKeyList)

        return render(request, 'Statement/GetInfos.html', {'InfoList': InfoList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getDetailInfo(request):
    """
    전자명세서 1건의 상세정보를 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[전자명세서 API 연동매뉴얼] > 4.1. 전자명세서 구성" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        statement = statementService.getDetailInfo(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetDetailInfo.html', {'statement': statement})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 전자명세서 목록을 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[전자명세서 API 연동매뉴얼] > 3.2.4. Search (목록 조회)"
      를 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 일자유형, R-등록일시, W-작성일자, I-발행일시 중 택 1
        DType = "W"

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20190101"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20190116"

        # 명세서 상태코드, 2,3번째 자리에 와일드카드(*) 사용 가능
        State = ["2**", "3**"]

        # 명세서 종류 코드 배열, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = ["121", "122", "123", "124", "125", "126"]

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향 D-내림차순, A-오름차순
        Order = "D"

        # 거래처 정보, 거래처 상호 또는 사업자등록번호 기재, 공백처리시 전체조회
        QString = ""

        response = statementService.search(CorpNum, DType, SDate, EDate, State, ItemCode,
                                           Page, PerPage, Order, UserID, QString)

        return render(request, 'Statement/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getLogs(request):
    """
    전자명세서 상태 변경이력을 확인합니다.
    - 상태 변경이력 확인(GetLogs API) 응답항목에 대한 자세한 정보는 "[전자명세서 API 연동매뉴얼] >
     3.2.5 GetLogs (상태 변경이력 확인)" 을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        LogList = statementService.getLogs(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetLogs.html', {'LogList': LogList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL(request):
    """
    전자명세서 문서함 관련 URL을 반홚합니다.
    - 보안정책으로 인해 반한된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # TBOX-임시 문서함, SBOX-발행 문서함
        TOGO = "TBOX"

        url = statementService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopUpURL(request):
    """
    1건의 전자명세서 보기 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        url = statementService.getPopUpURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPrintURL(request):
    """
    1건의 전자명세서 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        url = statementService.getPrintURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getEPrintURL(request):
    """
    전자명세서 인쇄(수신자) URL을 반환합니다.
    - 반환된 URL은 보안정책에 따라 30초의 유효시간을 갖습니다.
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        url = statementService.getEPrintURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMassPrintURL(request):
    """
    다수건의 전자명세서 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 인쇄할 문서관리번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20190116-001")
        MgtKeyList.append("20190116-002")
        MgtKeyList.append("20190116-003")

        url = statementService.getMassPrintURL(CorpNum, ItemCode, MgtKeyList)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMailURL(request):
    """
    수신자 메일링크 URL을 반환합니다.
    - 메일링크 URL은 유효시간이 존재하지 않습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        url = statementService.getMailURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌 로그인 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = statementService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def attachFile(request):
    """
    전자명세서에 첨부파일을 등록합니다.
    - 첨부파일 등록은 전자명세서가 [임시저장] 상태인 경우에만 가능합니다.
    - 첨부파일은 최대 5개까지 등록할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 파일경로
        FilePath = "./StatementExample/static/image/attachfile.png"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.attachFile(CorpNum, ItemCode, MgtKey, FilePath, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def deleteFile(request):
    """
    전자명세서에 첨부된 파일을 삭제합니다.
    - 파일을 식별하는 파일아이디는 첨부파일 목록(GetFileList API) 의 응답항목
      중 파일아이디(AttachedFile) 값을 통해 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 삭제할 FileID, 첨부파일목록(getFiles API) 응답 전문의 attachedFile 값
        FileID = "0DD20B73-5654-488E-A683-0ABED95C7D07.PBF"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.deleteFile(CorpNum, ItemCode, MgtKey, FileID, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFiles(request):
    """
    전자명세서에 첨부된 파일의 목록을 확인합니다.
    - 응답항목 중 파일아이디(AttachedFile) 항목은 파일삭제(DeleteFile API) 호출시 이용할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        fileList = statementService.getFiles(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetFiles.html', {'fileList': fileList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendEmail(request):
    """
    발행 안내메일을 재전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 수신메일주소
        ReceiverMail = "test@test.com"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.sendEmail(CorpNum, ItemCode, MgtKey, ReceiverMail, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendSMS(request):
    """
    알림문자를 전송합니다. (단문/SMS- 한글 최대 45자)
    - 알림문자 전송시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [문자] >[전송내역] 탭에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 발신번호
        Sender = "07000001234"

        # 수신번호
        Receiver = "010111222"

        # 문자메시지내용, 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "전자명세서 API 문자메시지 테스트"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.sendSMS(CorpNum, ItemCode, MgtKey, Sender, Receiver, Contents, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFAX(request):
    """
    전자명세 팩스전송합니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20190116-002"

        # 발신번호
        Sender = "070222111"

        # 수신번호
        Receiver = "070111222"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.sendFAX(CorpNum, ItemCode, MgtKey, Sender, Receiver, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def FAXSend(request):
    """
    팝빌에 등록하지 않고 전자명세서를 팩스전송합니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌" > [문자 팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스발신번호
        SendNum = "070-1234-1234"

        # 팩스수신번호
        ReceiveNum = "070-1111-2122"

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20190116",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 발신자별 고유번호 생성
            mgtKey="20190116-100",

            # [필수] 발신자 사업자번호, '-' 제외 10자리
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
            senderEmail="test@test.com",

            # 발신자 연락처
            senderTEL="070-1234-1234",

            # 발신자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 수신자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 수신자 상호
            receiverCorpName="수신자 상호",

            # [필수] 수신자 대표자 성명
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

            # 수신자  메일주소
            receiverEmail="test@test.com",

            # 수신자 연락처
            receiverTEL="070111222",

            # 수신자 휴대폰번호
            receiverHP="010-111-222",

            # [필수] 공급가액 합계
            supplyCostTotal="20000",

            # [필수] 세액 합계
            taxTotal="2000",

            # [필수] 합계금액, 공금가액 합계 + 세액 합계
            totalAmount="22000",

            # 기재 상 '일련번호' 항목
            serialNum="123",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 사업자등록증 이미지 첨부 여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부 여부
            bankBookYN=False,
        )

        # 상세항목(품목) 정보 (배열 길이 제한 없음)
        statement.detailList = []

        statement.detailList.append(
            StatementDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )
        statement.detailList.append(
            StatementDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                itemName="품목1",  # 품목
                purchaseDT="20190116",  # 거래일자
                spec="BOX",  # 규격
                unitCost="10000",  # 단가
                qty=1,  # 수량
                supplyCost="10000",  # 공급가액
                tax="1000"  # 세액
            )
        )

        # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
        # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
        statement.propertyBag = {
            'Balance': "20000",  # 전잔액
            'Deposit': "5000",  # 입금액
            'CBalance': "25000"  # 현잔액
        }

        result = statementService.FAXSend(CorpNum, statement, SendNum, ReceiveNum, UserID)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def attachStatement(request):
    """
    전자명서세에 다른 전자명세서 1건을 첨부합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        # 첨부할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부할 전자명세서 문서관리번호
        SubMgtKey = "20190115-001"

        response = statementService.attachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def detachStatement(request):
    """
    전자명서세에 첨부된 다른 전자명세서를 첨부해제합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서관리번호
        MgtKey = "20190116-001"

        # 첨부해제할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부해제할 전자명세서 문서관리번호
        SubMgtKey = "20190115-001"

        response = statementService.detachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listEmailConfig(request):
    """
    전자명세서 관련 메일전송 항목에 대한 전송여부를 목록으로 반환합니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        EmailConfig = statementService.listEmailConfig(CorpNum, UserID)

        return render(request, 'Statement/ListEmailConfig.html', {'EmailConfig': EmailConfig})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateEmailConfig(request):
    """
    전자명세서 관련 메일전송 항목에 대한 전송여부를 수정합니다.
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
        EmailType = 'SMT_ISSUE'

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.updateEmailConfig(CorpNum, EmailType, SendYN, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금이 아닌 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API)를
      통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = statementService.getBalance(CorpNum)

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

        url = statementService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를
      이용하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = statementService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = statementService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    전자명세서 발행단가를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드 [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        result = statementService.getUnitCost(CorpNum, ItemCode)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 전자명세서 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서], [124-발주서], [125-입금표], [126-영수증]
        ItemCode = "121"

        response = statementService.getChargeInfo(CorpNum, ItemCode, UserID)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 조회할 사업자등록번호, '-' 제외 10자리
        targetCorpNum = "1234567890"

        response = statementService.checkIsMember(targetCorpNum)

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

        response = statementService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    팝빌 연동회원 가입을 요청합니다.
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

        response = statementService.joinMember(newMember)

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

        response = statementService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
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

        response = statementService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

        response = statementService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        listContact = statementService.listContact(CorpNum, UserID)

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

        response = statementService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
