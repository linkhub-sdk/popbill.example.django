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

        # 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 공급자별 고유번호 생성
        MgtKey = "20161121-01"

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
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
            writeDate="20180119",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 공급자별 고유번호 생성
            mgtKey="20180119-111",

            # [필수] 공급자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,

            # 공급자 상호
            senderCorpName="공급자 상호",

            # 공급자 주소
            senderAddr="공급자 주소",

            # 공급자 대표자 성명
            senderCEOName="공급자 대표자 성명",

            # 공급자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",

            # 공급자 종목
            senderBizClass="종목",

            # 공급자 업태
            senderBizType="업태",

            # 공급자 담당자 성명
            senderContactName="공급자 담당자명",

            # 공급자 메일주소
            senderEmail="test@test.com",

            # 공급자 연락처
            senderTEL="070-1234-1234",

            # 공급자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 공급받는자 상호
            receiverCorpName="공급받는자 상호",

            # [필수] 공급받는자 대표자 성명
            receiverCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            receiverAddr="공급받는자 주소",

            # 공급받는자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",

            # 공급받는자 종목
            receiverBizClass="공급받는자 종목",

            # 공급받는자 업태
            receiverBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            receiverContactName="공급받는자 담당자명",

            # 공급받는자  메일주소
            receiverEmail="test@test.com",

            # 공급받는자 연락처
            receiverTEL="070111222",

            # 공급받는자 휴대폰번호
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

            # 상세항목(품목) 정보
            detailList=[
                StatementDetail(
                    serialNum=1,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                ),
                StatementDetail(
                    serialNum=2,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                )
            ],

            # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
            # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
            propertyBag={
                'Balance': "20000",  # 전잔액
                'Deposit': "5000",  # 입금액
                'CBalnce': "25000"  # 현잔액
            }
        )

        result = statementService.registIssue(CorpNum, statement, Memo, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def register(request):
    """
    전자명세서 1건을 임시저장합니다.
    - 임시저장 상태의 명세서는 발행(Issue API)을 호출해야 공급받는자에게 메일이 전송됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20180119",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 공급자별 고유번호 생성
            mgtKey="20180119-100",

            # [필수] 공급자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,

            # 공급자 상호
            senderCorpName="공급자 상호",

            # 공급자 주소
            senderAddr="공급자 주소",

            # 공급자 대표자 성명
            senderCEOName="공급자 대표자 성명",

            # 공급자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",

            # 공급자 종목
            senderBizClass="종목",

            # 공급자 업태
            senderBizType="업태",

            # 공급자 담당자 성명
            senderContactName="공급자 담당자명",

            # 공급자 메일주소
            senderEmail="test@test.com",

            # 공급자 연락처
            senderTEL="070-1234-1234",

            # 공급자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 공급받는자 상호
            receiverCorpName="공급받는자 상호",

            # [필수] 공급받는자 대표자 성명
            receiverCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            receiverAddr="공급받는자 주소",

            # 공급받는자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",

            # 공급받는자 종목
            receiverBizClass="공급받는자 종목",

            # 공급받는자 업태
            receiverBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            receiverContactName="공급받는자 담당자명",

            # 공급받는자  메일주소
            receiverEmail="test@test.com",

            # 공급받는자 연락처
            receiverTEL="070111222",

            # 공급받는자 휴대폰번호
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

            # 상세항목(품목) 정보
            detailList=[
                StatementDetail(
                    serialNum=1,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                ),
                StatementDetail(
                    serialNum=2,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                )
            ],

            # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
            # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
            propertyBag={
                'Balance': "20000",  # 전잔액
                'Deposit': "5000",  # 입금액
                'CBalance': "25000"  # 현잔액
            }
        )

        result = statementService.register(CorpNum, statement)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 수정할 전자명세서 문서관리번호
        mgtKey = "20180119-100"

        # 전자명세서 정보
        statement = Statement(
            # [필수] 작성일자 yyyyMMdd
            writeDate="20180119",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
            itemCode=ItemCode,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 공급자별 고유번호 생성
            mgtKey=mgtKey,

            # [필수] 공급자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,

            # 공급자 상호
            senderCorpName="공급자 상호_수",

            # 공급자 주소
            senderAddr="공급자 주소",

            # 공급자 대표자 성명
            senderCEOName="공급자 대표자 성명",

            # 공급자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",

            # 공급자 종목
            senderBizClass="종목",

            # 공급자 업태
            senderBizType="업태",

            # 공급자 담당자 성명
            senderContactName="공급자 담당자명",

            # 공급자 메일주소
            senderEmail="test@test.com",

            # 공급자 연락처
            senderTEL="070-1234-1234",

            # 공급자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 공급받는자 상호
            receiverCorpName="공급받는자 상호",

            # [필수] 공급받는자 대표자 성명
            receiverCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            receiverAddr="공급받는자 주소",

            # 공급받는자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",

            # 공급받는자 종목
            receiverBizClass="공급받는자 종목",

            # 공급받는자 업태
            receiverBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            receiverContactName="공급받는자 담당자명",

            # 공급받는자  메일주소
            receiverEmail="test@test.com",

            # 공급받는자 연락처
            receiverTEL="070111222",

            # 공급받는자 휴대폰번호
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

            # 상세항목(품목) 정보
            detailList=[
                StatementDetail(
                    serialNum=1,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                ),
                StatementDetail(
                    serialNum=2,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20160119",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                )
            ],

            # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
            # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
            propertyBag={
                'Balance': "20000",  # 전잔액
                'Deposit': "5000",  # 입금액
                'CBalance': "25000"  # 현잔액
            }
        )

        result = statementService.update(CorpNum, ItemCode, mgtKey, statement)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 124

        # 전자명세서 문서관리번호
        MgtKey = "20180119-100"

        result = statementService.issue(CorpNum, ItemCode, MgtKey)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancel(request):
    """
    1건의 전자명세서를 [발행취소] 처리합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 124

        # 전자명세서 문서관리번호
        MgtKey = "20180119-100"

        # 메모
        Memo = "발행취소 메모"

        result = statementService.cancel(CorpNum, ItemCode, MgtKey, Memo)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 124

        # 전자명세서 문서관리번호
        MgtKey = "20180119-100"

        result = statementService.delete(CorpNum, ItemCode, MgtKey)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

        statementInfo = statementService.getInfo(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/Getinfo.html', {'statementInfo': statementInfo})
    except PopbillException as PE:
        return render(request, 'Statement/GetInfo.html', {'code': PE.code, 'message': PE.message})


def getInfos(request):
    """
    다수건의 전자명세서 상태/요약 정보를 확인합니다.
    - 응답항목에 대한 자세한 정보는 "[전자명세서 API 연동매뉴얼] > 3.3.2. GetInfos (상태 대량 확인)"
     을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 문서관리번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20161121-01")
        MgtKeyList.append("20161121-02")
        MgtKeyList.append("20161121-03")

        InfoList = statementService.getInfos(CorpNum, ItemCode, MgtKeyList)

        return render(request, 'Statement/Getinfos.html', {'InfoList': InfoList})
    except PopbillException as PE:
        return render(request, 'Statement/GetInfos.html', {'code': PE.code, 'message': PE.message})


def getDetailInfo(request):
    """
    전자명세서 1건의 상세정보를 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[전자명세서 API 연동매뉴얼] > 4.1. 전자명세서 구성" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

        statement = statementService.getDetailInfo(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetDetailInfo.html', {'statement': statement})
    except PopbillException as PE:
        return render(request, 'Statement/GetDetailInfo.html', {'code': PE.code, 'message': PE.message})


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
        SDate = "20161001"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20161131"

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
        return render(request, 'Statement/Search.html', {'code': PE.code, 'message': PE.message})


def getLogs(request):
    """
    전자명세서 상태 변경이력을 확인합니다.
    - 상태 변경이력 확인(GetLogs API) 응답항목에 대한 자세한 정보는 "[전자명세서 API 연동매뉴얼] >
     3.3.4 GetLogs (상태 변경이력 확인)" 을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

        LogList = statementService.getLogs(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetLogs.html', {'LogList': LogList})
    except PopbillException as PE:
        return render(request, 'Statement/GetLogs.html', {'code': PE.code, 'message': PE.message})


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
        TOGO = "SEAL"

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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161121-03"

        url = statementService.getPrintURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getEPrintURL(request):
    """
    전자명세서 인쇄(공급받는자) URL을 반환합니다.
    - 반환된 URL은 보안정책에 따라 30초의 유효시간을 갖습니다.
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 인쇄할 문서관리번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20180103010")
        MgtKeyList.append("20171228-013")
        MgtKeyList.append("20171228-001")

        url = statementService.getMassPrintURL(CorpNum, ItemCode, MgtKeyList)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMailURL(request):
    """
    공급받는자 메일링크 URL을 반환합니다.
    - 메일링크 URL은 유효시간이 존재하지 않습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20161123-01"

        url = statementService.getMailURL(CorpNum, ItemCode, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


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

        url = statementService.getPopbillURL(CorpNum, UserID, TOGO)

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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "2018-01-16-888"

        # 파일경로
        FilePath = "./StatementExample/static/image/attachfile.png"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = statementService.attachFile(CorpNum, ItemCode, MgtKey, FilePath, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "2018-01-16-888"

        # 삭제할 FileID, 첨부파일목록(getFiles API) 응답 전문의 attachedFile 값
        FileID = "0DD20B73-5654-488E-A683-0ABED95C7D07.PBF"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = statementService.deleteFile(CorpNum, ItemCode, MgtKey, FileID, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "2018-01-16-888"

        fileList = statementService.getFiles(CorpNum, ItemCode, MgtKey)

        return render(request, 'Statement/GetFiles.html', {'fileList': fileList})
    except PopbillException as PE:
        return render(request, 'Statement/GetFiles.html', {'code': PE.code, 'message': PE.message})


def sendEmail(request):
    """
    발행 안내메일을 재전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자세금서 문서관리번호
        MgtKey = "2018-01-16-888"

        # 수신메일주소
        ReceiverMail = "test@test.com"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = statementService.sendEmail(CorpNum, ItemCode, MgtKey, ReceiverMail, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendSMS(request):
    """
    알림문자를 전송합니다. (단문/SMS- 한글 최대 45자)
    - 알림문자 전송시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [전송내역] 탭에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "2018-01-16-888"

        # 발신번호
        Sender = "07000001234"

        # 수신번호
        Receiver = "010111222"

        # 문자메시지내용, 90Byte 초과시 길이가 조정되어 전송됨
        Contents = "전자명세서 API 문자메시지 테스트"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = statementService.sendSMS(CorpNum, ItemCode, MgtKey, Sender, Receiver, Contents, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = 121

        # 전자명세서 문서관리번호
        MgtKey = "20150326-01"

        # 발신번호
        Sender = "07043042991"

        # 수신번호
        Receiver = "070111222"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = statementService.sendFAX(CorpNum, ItemCode, MgtKey, Sender, Receiver, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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
            writeDate="20180119",

            # [필수] [영수 / 청구] 중 기재
            purposeType="영수",

            # [필수] 과세형태, [과세 / 영세 / 면세] 중 기재
            taxType="과세",

            # 맞춤양식코드, 미기재시 기본양식으로 처리
            formCode="",

            # [필수] 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
            itemCode=121,

            # [필수] 전자명세서 관리번호, 1~24자리, 영문,숫자,-,_ 조합으로 공급자별 고유번호 생성
            mgtKey="20180119-100",

            # [필수] 공급자 사업자번호, '-' 제외 10자리
            senderCorpNum=CorpNum,

            # 공급자 상호
            senderCorpName="공급자 상호",

            # 공급자 주소
            senderAddr="공급자 주소",

            # 공급자 대표자 성명
            senderCEOName="공급자 대표자 성명",

            # 공급자 종사업장 식별번호, 필요시 4자리 숫자값 기재
            senderTaxRegID="",

            # 공급자 종목
            senderBizClass="종목",

            # 공급자 업태
            senderBizType="업태",

            # 공급자 담당자 성명
            senderContactName="공급자 담당자명",

            # 공급자 메일주소
            senderEmail="test@test.com",

            # 공급자 연락처
            senderTEL="070-1234-1234",

            # 공급자 휴대폰번호
            senderHP="010-000-222",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            receiverCorpNum="8888888888",

            # 공급받는자 상호
            receiverCorpName="공급받는자 상호",

            # [필수] 공급받는자 대표자 성명
            receiverCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            receiverAddr="공급받는자 주소",

            # 공급받는자 종사업장식별번호, 필요시 4자리 숫자값 기재
            receiverTaxRegID="",

            # 공급받는자 종목
            receiverBizClass="공급받는자 종목",

            # 공급받는자 업태
            receiverBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            receiverContactName="공급받는자 담당자명",

            # 공급받는자  메일주소
            receiverEmail="test@test.com",

            # 공급받는자 연락처
            receiverTEL="070111222",

            # 공급받는자 휴대폰번호
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

            # 상세항목(품목) 정보
            detailList=[
                StatementDetail(
                    serialNum=1,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20161120",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                ),
                StatementDetail(
                    serialNum=2,  # 일련번호, 1부터 순차기재
                    itemName="품목1",  # 품목
                    purchaseDT="20161120",  # 거래일자
                    spec="BOX",  # 규격
                    unitCost="10000",  # 단가
                    qty=1,  # 수량
                    supplyCost="10000",  # 공급가액
                    tax="1000"  # 세액
                )
            ],

            # 추가속성정보, 명세서 종류별 추가적인 속성을{key:value}형식의 Dictionary로 정의
            # 자세한 정보는 "전자명세서 API 연동매뉴얼 > [5.2. 기본양식 추가속성 테이블] 참조
            propertyBag={
                'Balance': "20000",  # 전잔액
                'Deposit': "5000",  # 입금액
                'CBalance': "25000"  # 현잔액
            }
        )

        result = statementService.FAXSend(CorpNum, statement, SendNum, ReceiveNum, UserID)

        return render(request, 'result.html', {'code': result.code})
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
        MgtKey = "2018-01-16-888"

        # 첨부할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부할 전자명세서 문서관리번호
        SubMgtKey = "20171122-03"

        result = statementService.attachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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
        MgtKey = "2018-01-16-888"

        # 첨부할 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        SubItemCode = "121"

        # 첨부할 전자명세서 문서관리번호
        SubMgtKey = "20171122-03"

        result = statementService.detachStatement(CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        url = statementService.getPopbillURL(CorpNum, UserID, TOGO)

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

        # CHRG-포인트충전
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
        ItemCode = 123

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

        # 명세서 코드, [121-거래명세서], [122-청구서], [123-견적서] [124-발주서], [125-입금표], [126-영수증]
        ItemCode = "121"

        response = statementService.getChargeInfo(CorpNum, ItemCode, UserID)

        return render(request, 'GetChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 조회할 사업자등록번호, '-' 제외 10자리
        targetCorpNum = "1234567890"

        result = statementService.checkIsMember(targetCorpNum)

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

        result = statementService.joinMember(newMember)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        return render(request, 'getCorpInfo.html',
                      {'ceoname': response.ceoname, 'corpName': response.corpName,
                       'addr': response.addr, 'bizType': response.bizType,
                       'bizClass': response.bizClass})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


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

        result = statementService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
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

        result = statementService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listContact(request):
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = statementService.listContact(CorpNum, UserID)

        return render(request, 'ListContact.html', {'listContact': listContact})
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

        result = statementService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': result.code, 'message': result.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
