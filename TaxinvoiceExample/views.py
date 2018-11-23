# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import TaxinvoiceService, PopbillException, Taxinvoice, TaxinvoiceDetail, Contact, ContactInfo, JoinForm, \
    CorpInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 TaxinvoiceService 객체 생성
taxinvoiceService = TaxinvoiceService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
taxinvoiceService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Taxinvoice/Index.html', {})


def checkMgtKeyInUse(request):
    """
    세금계산서 관리번호 중복여부를 확인합니다.
    - 관리번호는 1~24자리로 숫자, 영문 '-', '_' 조합으로 구성할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별로 중복되지 않도록 구성
        MgtKey = "2018-02-06-1"

        keyInUse = taxinvoiceService.checkMgtKeyInUse(CorpNum, MgtKeyType, MgtKey)

        if keyInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registIssue(request):
    """
    1건의 세금계산서를 즉시발행 처리합니다. (권장)
    - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 세금계산서 문서관리번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
        MgtKey = "2018-02-07-1"

        # 지연발행 강제여부
        # 발행마감일이 지난 세금계산서를 발행하는 경우, 가산세가 부과될 수 있습니다.
        # 가산세가 부과되더라도 발행을 해야하는 경우에는 forceIssue의 값을 True로 선언
        forceIssue = False

        # 거래명세서 동시작성여부
        writeSpecification = False

        # 거래명세서 동시작성시, 명세서 관리번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
        dealInvoiceMgtKey = ""

        # 메모
        memo = "즉시발행 메모"

        # 발행안내 메일 제목, 미기재시 기본양식으로 전송
        emailSubject = ""

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 정보
        taxinvoice = Taxinvoice(

            # [필수] 작성일자, 날짜형식(yyyyMMdd) ex)20180116
            writeDate="20180207",

            # [필수] 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",

            # [필수] 발행영태, [정발행, 역발행, 위수탁] 중 기재
            issueType="정발행",

            # [필수] 영수/청구, [영수, 청구] 중 기재
            purposeType="영수",

            # [필수] 발행시점, [직접발행, 승인시자동발행] '중 기재
            # 발행예정(Send API) 프로세스를 구현하지 않는경우 "직접발행' 기재
            issueTiming="직접발행",

            # [필수] 과세형태, [과세, 영세, 면세] 중 기재
            taxType="과세",

            ######################################################################
            #                             공급자 정보
            ######################################################################

            # [필수] 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,

            # [필수] 공급자 상호
            invoicerCorpName="공급자 상호",

            # [필수] 공급자 문서관리번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
            # 사업자별로 중복되지 않도록 구성
            invoicerMgtKey=MgtKey,

            # [필수] 공급자 대표자 성명
            invoicerCEOName="공급자 대표자 성명",

            # 공급자 주소
            invoicerAddr="공급자 주소",

            # 공급자 종목
            invoicerBizClass="공급자 종목",

            # 공급자 업태
            invoicerBizType="공급자 업태",

            # 공급자 담당자 성명
            invoicerContactName="공급자 담당자명",

            # 공급자 담당자 메일주소
            invoicerEmail="test@test.com",

            # 공급자 담당자 연락처
            invoicerTEL="070-111-222",

            # 공급자 담당자 휴대폰 번호
            invoicerHP='010-111-222',

            # 정발행시 공급받는자에게 발행안내문자 전송여부
            invoicerSMSSendYN=False,

            ######################################################################
            #                            공급받는자 정보
            ######################################################################

            # [필수] 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            invoiceeCorpNum="8888888888",

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,

            # [필수] 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",

            # [역발행시 필수] 공급받는자 문서관리번호, 1~24자리 (숫자, 영문, '-', '_') 조합으로
            # 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey=None,

            # [필수] 공급받는자 대표자 성명
            invoiceeCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            invoiceeAddr="공급받는자 주소",

            # 공급받는자 종목
            invoiceeBizClass="공급받는자 종목",

            # 공급받는자 업태
            invoiceeBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            invoiceeContactName1="공급받는자 담당자",

            # 공급받는자 담당자 메일주소
            invoiceeEmail1="test@test.com",

            # 공급받는자 연락처
            invoiceeTEL1="070-111-222",

            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="010-111-222",

            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="070-111-222",

            # 역발행시 공급자에게 발행안내문자 전송여부
            invoiceeSMSSendYN=False,

            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################

            # [필수] 공급가액 합계
            supplyCostTotal="100000",

            # [필수] 세액 합계
            taxTotal="10000",

            # [필수] 합계금액, 공급가액 합계 + 세액 합계
            totalAmount="110000",

            # 기재상 '일련번호' 항목
            serialNum="123",

            # 기재상 '현금' 항목
            cash=None,

            # 기재상 '수표' 항목
            chkBill=None,

            # 기재상 '어음' 항목
            note=None,

            # 기재상 '외상미수금' 항목
            credit="",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 기재상 '권' 항목, 최대값 32767
            kwon=1,

            # 기재상 '호' 항목, 최대값 32767
            ho=2,

            # 사업자등록증 이미지 첨부여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부여부
            bankBookYN=False,

            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - http://blog.linkhub.com/650
            ######################################################################

            # 수정세금계산서 정보 수정사유별로 1~6중 선택기재
            # 수정사유코드
            modifyCode=None,

            # 원본 세금계산서 ItemKey, 문서확인 (GetInfo API)의 응답결과(ItemKey 항목) 확인.
            originalTaxinvoiceKey=None
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = [
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            ),
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            )
        ]

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = [
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            ),
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            )
        ]

        response = taxinvoiceService.registIssue(CorpNum, taxinvoice, writeSpecification,
                                                 forceIssue, dealInvoiceMgtKey, memo, emailSubject, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def register(request):
    """
    1건의 세금계산서를 임시저장 합니다.
    - 세금계산서 임시저장(Register API) 호출후에는 발행(Issue API)을 호출해야만 국세청으로 전송됩니다.
    - 임시저장과 발행을 한번의 호출로 처리하는 즉시발행(RegistIssue API) 프로세스 연동을 권장합니다.
    - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 세금계산서 문서관리번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
        # 사업자별로 중복되지 않도록 구성
        MgtKey = "2018-02-07-59"

        # 거래명세서 동시작성여부
        writeSpecification = False

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 정보
        taxinvoice = Taxinvoice(

            # [필수] 작성일자, 날짜형식(yyyyMMdd) ex)20180116
            writeDate="20180206",

            # [필수] 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",

            # [필수] 발행영태, [정발행, 역발행, 위수탁] 중 기재
            issueType="정발행",

            # [필수] 영수/청구, [영수, 청구] 중 기재
            purposeType="영수",

            # [필수] 발행시점, [직접발행, 승인시자동발행] '중 기재
            # 발행예정(Send API) 프로세스를 구현하지 않는경우 '직접발행' 기재
            issueTiming="직접발행",

            # [필수] 과세형태, [과세, 영세, 면세] 중 기재
            taxType="과세",

            ######################################################################
            #                             공급자 정보
            ######################################################################

            # [필수] 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,

            # [필수] 공급자 상호
            invoicerCorpName="공급자 상호",

            # [필수] 공급자 문서관리번호, 1~24자리, (영문, 숫자, '-', '_')조합으로
            # 사업자별로 중복되지 않도록 구성
            invoicerMgtKey=MgtKey,

            # 공급자 대표자 성명
            invoicerCEOName="공급자 대표자 성명",

            # 공급자 주소
            invoicerAddr="공급자 주소",

            # 공급자 종목
            invoicerBizClass="공급자 종목",

            # 공급자 업태
            invoicerBizType="공급자 업태",

            # 공급자 담당자 성명
            invoicerContactName="공급자 담당자명",

            # 공급자 담당자 메일주소
            invoicerEmail="test@test.com",

            # 공급자 담당자 연락처
            invoicerTEL="070-111-222",

            # 공급자 담당자 휴대폰 번호
            invoicerHP='010-111-222',

            # 정발행시 공급받는자에게 발행안내문자 전송여부
            invoicerSMSSendYN=False,

            ######################################################################
            #                            공급받는자 정보
            ######################################################################

            # [필수] 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            invoiceeCorpNum="8888888888",

            # [필수] 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",

            # [역발행시 필수] 공급받는자 문서관리번호, , 1~24자리, (영문, 숫자, '-', '_') 조합으로
            # 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey=None,

            # [필수] 공급받는자 대표자 성명
            invoiceeCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            invoiceeAddr="공급받는자 주소",

            # 공급받는자 종목
            invoiceeBizClass="공급받는자 종목",

            # 공급받는자 업태
            invoiceeBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            invoiceeContactName1="공급받는자 담당자",

            # 공급받는자 담당자 메일주소
            invoiceeEmail1="test@test.com",

            # 공급받는자 연락처
            invoiceeTEL1="070-111-222",

            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="010-111-222",

            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="070-111-222",

            # 역발행시 공급자에게 발안내문자 전송여부
            invoiceeSMSSendYN=False,

            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################

            # [필수] 공급가액 합계
            supplyCostTotal="100000",

            # [필수] 세액 합계
            taxTotal="10000",

            # [필수] 합계금액, 공급가액 합계 + 세액 합계
            totalAmount="110000",

            # 기재상 '일련번호' 항목
            serialNum="123",

            # 기재상 '현금' 항목
            cash=None,

            # 기재상 '수표' 항목
            chkBill=None,

            # 기재상 '어음' 항목
            note=None,

            # 기재상 '외상미수금' 항목
            credit="",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 기재상 '권' 항목, 최대값 32767
            kwon=1,

            # 기재상 '호' 항목, 최대값 32767
            ho=2,

            # 사업자등록증 이미지 첨부여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부여부
            bankBookYN=False,

            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - http://blog.linkhub.com/650
            ######################################################################

            # 수정세금계산서 정보
            # 수정사유코드, 수정사유별로 1~6중 선택기재
            modifyCode=None,

            # 원본세금계산서의 ItemKey, 문서확인 (GetInfo API)의 응답결과(ItemKey 항목) 확인.
            originalTaxinvoiceKey=None
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = [
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            ),
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            )
        ]

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = [
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            ),
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            )
        ]

        response = taxinvoiceService.register(CorpNum, taxinvoice, writeSpecification, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def update(request):
    """
    [임시저장] 상태의 세금계산서의 항목을 수정합니다.
    - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-02-07-2"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 정보
        taxinvoice = Taxinvoice(

            # [필수] 작성일자, 날짜형식(yyyyMMdd) ex)20180116
            writeDate="20180210",

            # [필수] 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",

            # [필수] 발행영태, [정발행, 역발행, 위수탁] 중 기재
            issueType="정발행",

            # [필수] 영수/청구, [영수, 청구] 중 기재
            purposeType="영수",

            # [필수] 발행시점, [직접발행, 승인시자동발행] '중 기재
            # 발행예정(Send API) 프로세스를 구현하지 않는경우 '직접발행' 기재
            issueTiming="직접발행",

            # [필수] 과세형태, [과세, 영세, 면세] 중 기재
            taxType="과세",

            ######################################################################
            #                             공급자 정보
            ######################################################################

            # [필수] 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,

            # [필수] 공급자 상호
            invoicerCorpName="공급자 상호",

            # [필수] 공급자 문서관리번호
            invoicerMgtKey=MgtKey,

            # [필수] 공급자 대표자 성명
            invoicerCEOName="공급자 대표자 성명",

            # 공급자 주소
            invoicerAddr="공급자 주소_수정",

            # 공급자 종목
            invoicerBizClass="공급자 종목",

            # 공급자 업태
            invoicerBizType="공급자 업태",

            # 공급자 담당자 성명
            invoicerContactName="공급자 담당자명",

            # 공급자 담당자 메일주소
            invoicerEmail="test@test.com",

            # 공급자 담당자 연락처
            invoicerTEL="070-111-222",

            # 공급자 담당자 휴대폰 번호
            invoicerHP="010-111-222",

            # 정발행시 공급받는자에게 발행안내문자 전송여부
            invoicerSMSSendYN=False,

            ######################################################################
            #                            공급받는자 정보
            ######################################################################

            # [필수] 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType='사업자',

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            invoiceeCorpNum="8888888888",

            # [필수] 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",

            # [역발행시 필수] 공급받는자 문서관리번호
            invoiceeMgtKey=None,

            # [필수] 공급받는자 대표자 성명
            invoiceeCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            invoiceeAddr="공급받는자 주소",

            # 공급받는자 종목
            invoiceeBizClass="공급받는자 종목",

            # 공급받는자 업태
            invoiceeBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            invoiceeContactName1="공급받는자 담당자",

            # 공급받는자 담당자 메일주소
            invoiceeEmail1="test@test.com",

            # 공급받는자 연락처
            invoiceeTEL1="070-111-222",

            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="010-111-222",

            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="070-111-222",

            # 역발행시 공급자에게 발행안내문자 전송여부
            invoiceeSMSSendYN=False,

            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################

            # [필수] 공급가액 합계
            supplyCostTotal="100000",

            # [필수] 세액 합계
            taxTotal="10000",

            # [필수] 합계금액, 공급가액 합계 + 세액 합계
            totalAmount="110000",

            # 기재상 '일련번호' 항목
            serialNum="123",

            # 기재상 '현금' 항목
            cash=None,

            # 기재상 '수표' 항목
            chkBill=None,

            # 기재상 '어음' 항목
            note=None,

            # 기재상 '외상미수금' 항목
            credit="",

            # 기재 상 '비고' 항목
            remark1='비고1',
            remark2='비고2',
            remark3='비고3',

            # 기재상 '권' 항목, 최대값 32767
            kwon=1,

            # 기재상 '호' 항목, 최대값 32767
            ho=2,

            # 사업자등록증 이미지 첨부여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부여부
            bankBookYN=False,

            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - http://blog.linkhub.com/650
            ######################################################################

            # 수정세금계산서 정보
            # 수정사유코드, 수정사유별로 1~6중 선택기재
            modifyCode=None,

            # 원본 세금계산서 ItemKey
            originalTaxinvoiceKey=None
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = [
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            ),
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20180116",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            )
        ]

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = [
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            ),
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            )
        ]

        response = taxinvoiceService.update(CorpNum, MgtKeyType, MgtKey, taxinvoice, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def issue(request):
    """
    [임시저장] 또는 [발행대기] 상태의 세금계산서를 [발행] 처리합니다.
    - 세금계산서를 발행하기 위해서는 먼저 공인인증서가 팝빌에 등록되어 있어야 합니다.
    - 발행(Issue API)를 호출하는 시점에서 포인트가 차감됩니다.
    - [발행완료] 세금계산서는 연동회원의 국세청 전송설정에 따라 익일/즉시전송 처리됩니다. 기본설정(익일전송)
    - 국세청 전송설정은 "팝빌 로그인" > [전자세금계산서] > [환경설정] >
      [전자세금계산서 관리] > [국세청 전송 및 지연발행 설정] 탭에서 확인할 수 있습니다.
    - 국세청 전송정책에 대한 사항은 "[전자세금계산서 API 연동매뉴얼] > 1.3. 국세청 전송 정책" 을 참조하시기 바랍니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # [필수] 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-02-07-0509-2"

        # 메모
        Memo = "발행 메모"

        # 발행 안내메일 제목, 미기재시 기본양식으로 전송
        EmailSubject = None

        # 지연발행 강제여부, 기본값 - False
        # 발행마감일이 지난 세금계산서를 발행하는 경우, 가산세가 부과될 수 있습니다.
        # 지연발행 세금계산서를 신고해야 하는 경우 forceIssue 값을 True로 선언하여
        # 발행(Issue API)을 호출할 수 있습니다.
        ForceIssue = False

        # 팝빌회원 아이디
        UserID = settings.testUserID

        result = taxinvoiceService.issue(CorpNum, MgtKeyType, MgtKey, Memo,
                                         EmailSubject, ForceIssue, UserID)

        return render(request, 'result.html', {'code': result.code})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelIssue(request):
    """
    [발행완료] 상태의 세금계산서를 [발행취소] 처리합니다.
    - [발행취소]는 국세청 전송전에만 가능합니다.
    - 발행취소된 세금계산서는 국세청에 전송되지 않습니다.
    - 발행취소 세금계산서에 기재된 '문서관리번호(mgtKey)'를 재사용 하기 위해서는 삭제(Delete API)를
      호출하여 [삭제] 처리 하셔야 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "201802061080"

        # 메모
        Memo = "발행취소 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.cancelIssue(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def send(request):
    """
    공급자가 [임시저장] 상태의 세금계산서를 [발행예정] 합니다.
    - 발행예정이란 공급자와 공급받는자 사이에 세금계산서 확인 후 발해하는 방법입니다.
    - "[전자세금계산서 API 연동매뉴얼] > 1.2.1. 정발행 프로세스 흐름도 > 다. 임시저장 발행예정" 의
      프로세스를 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-005"

        # 메모
        Memo = "발행예정 메모"

        # 안내메일 제목, 미기재시 기본양식으로 전송
        EmailSubject = ""

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.send(CorpNum, MgtKeyType, MgtKey, Memo, EmailSubject, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelSend(request):
    """
    [발행예정] 세금계산서를 [취소] 처리 합니다.
    - [취소]된 세금계산서를 삭제(Delete API)하면 등록된 '문서관리번호'를 재사용할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-005"

        # 메모
        Memo = "발행예정 취소 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.cancelSend(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def accept(request):
    """
    [발행예정] 세금계산서를 공급받는자가 [승인]처리 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-008"

        # 메모
        Memo = "발행예정 승인 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.accept(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def deny(request):
    """
    발행예정 세금계산서를 [거부]처리 합니다.
    - [거부]된 세금계산서를 삭제(Delete API)하면 등록된 '문서관리번호'를재사용할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 관리번호 유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-009"

        # 메모
        Memo = "발행예정 거부 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.deny(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def delete(request):
    """
    1건의 전자세금계산서를 삭제합니다.
    - 세금계산서를 삭제해야만 '문서관리번호(mgtKey)'를 재사용할 수 있습니다.
    - 삭제가능한 문서 상태 : [임시저장], [발행취소], [발행예정 취소], [발행예정 거부]
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180112001"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.delete(CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registRequest(request):
    """
     [공급받는자]가 공급자에게 1건의 역발행 세금계산서를 [즉시 요청]합니다.
      - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서구성"을 참조하시기 바랍니다.
      - 역발행 세금계산서 프로세스를 구현하기 위해서는 공급자/공급받는자가 모두 팝빌에 회원이여야 합니다.
      - 역발행 즉시요청후 공급자가 [발행] 처리시 포인트가 차감되며 역발행 세금계산서 항목중 과금방향(ChargeDirection)에 기재한 값에 따라
        정과금(공급자과금) 또는 역과금(공급받는자과금) 처리됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 정보
        taxinvoice = Taxinvoice(

            # [필수] 작성일자, 날짜형식(yyyyMMdd) ex)20181116
            writeDate="20181116",

            # [필수] 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",

            # [필수] 발행영태, [정발행, 역발행, 위수탁] 중 기재
            issueType="역발행",

            # [필수] 영수/청구, [영수, 청구] 중 기재
            purposeType="영수",

            # [필수] 발행시점, [직접발행, 승인시자동발행] '중 기재
            # 발행예정(Send API) 프로세스를 구현하지 않는경우 "직접발행' 기재
            issueTiming="직접발행",

            # [필수] 과세형태, [과세, 영세, 면세] 중 기재
            taxType="과세",

            ######################################################################
            #                             공급자 정보
            ######################################################################

            # [필수] 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum='8888888888',

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,

            # [필수] 공급자 상호
            invoicerCorpName="공급자 상호",

            # 공급자 문서관리번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
            # 사업자별로 중복되지 않도록 구성
            invoicerMgtKey="",

            # [필수] 공급자 대표자 성명
            invoicerCEOName="공급자 대표자 성명",

            # 공급자 주소
            invoicerAddr="공급자 주소",

            # 공급자 종목
            invoicerBizClass="공급자 종목",

            # 공급자 업태
            invoicerBizType="공급자 업태",

            # 공급자 담당자 성명
            invoicerContactName="공급자 담당자명",

            # 공급자 담당자 메일주소
            invoicerEmail="test@test.com",

            # 공급자 담당자 연락처
            invoicerTEL="070-111-222",

            # 공급자 담당자 휴대폰 번호
            invoicerHP='010-111-222',

            # 정발행시 공급받는자에게 발행안내문자 전송여부
            invoicerSMSSendYN=False,

            ######################################################################
            #                            공급받는자 정보
            ######################################################################

            # [필수] 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",

            # [필수] 공급받는자 사업자번호, '-' 제외 10자리
            invoiceeCorpNum=CorpNum,

            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,

            # [필수] 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",

            # [역발행시 필수] 공급받는자 문서관리번호, 1~24자리 (숫자, 영문, '-', '_') 조합으로
            # 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey="20181116-00A",

            # [필수] 공급받는자 대표자 성명
            invoiceeCEOName="공급받는자 대표자 성명",

            # 공급받는자 주소
            invoiceeAddr="공급받는자 주소",

            # 공급받는자 종목
            invoiceeBizClass="공급받는자 종목",

            # 공급받는자 업태
            invoiceeBizType="공급받는자 업태",

            # 공급받는자 담당자 성명
            invoiceeContactName1="공급받는자 담당자",

            # 공급받는자 담당자 메일주소
            invoiceeEmail1="test@test.com",

            # 공급받는자 연락처
            invoiceeTEL1="070-111-222",

            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="010-111-222",

            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="070-111-222",

            # 역발행시 공급자에게 발행안내문자 전송여부
            invoiceeSMSSendYN=False,

            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################

            # [필수] 공급가액 합계
            supplyCostTotal="100000",

            # [필수] 세액 합계
            taxTotal="10000",

            # [필수] 합계금액, 공급가액 합계 + 세액 합계
            totalAmount="110000",

            # 기재상 '일련번호' 항목
            serialNum="",

            # 기재상 '현금' 항목
            cash=None,

            # 기재상 '수표' 항목
            chkBill=None,

            # 기재상 '어음' 항목
            note=None,

            # 기재상 '외상미수금' 항목
            credit="",

            # 기재 상 '비고' 항목
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",

            # 기재상 '권' 항목, 최대값 32767
            kwon=10,

            # 기재상 '호' 항목, 최대값 32767
            ho=10,

            # 사업자등록증 이미지 첨부여부
            businessLicenseYN=False,

            # 통장사본 이미지 첨부여부
            bankBookYN=False,

            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - http://blog.linkhub.com/650
            ######################################################################

            # 수정세금계산서 정보 수정사유별로 1~6중 선택기재
            # 수정사유코드
            modifyCode=None,

            # 원본 세금계산서 ItemKey, 문서확인 (GetInfo API)의 응답결과(ItemKey 항목) 확인.
            originalTaxinvoiceKey=None
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = [
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20181116",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            ),
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20181116",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고"  # 비고
            )
        ]

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = [
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            ),
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com"  # 메일주소
            )
        ]

        memo = "즉시발행 메모"

        response = taxinvoiceService.registRequest(CorpNum, taxinvoice, memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def request(request):
    """
    공급받는자가 공급자에게 1건의 역발행 세금계산서를 요청합니다.
    - 역발행 세금계산서 프로세스를 구현하기 위해서는 공급자/공급받는자가 모두 팝빌에 회원이여야 합니다.
    - 역발행 요청후 공급자가 [발행] 처리시 포인트가 차감되며 역발행 세금계산서 항목 중
      과금방향(ChargeDirection) 에 기재한 값에 따라 정과금(공급자과금) 또는 역과금(공급받는자과금)
      처리됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "BUY"

        # 문서관리번호
        MgtKey = "2018-02-07-0509-5"

        # 메모
        Memo = "역발행 요청 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.request(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelRequest(request):
    """
    역발행 세금계산서를 [취소] 처리합니다.
    - [취소]한 세금계산서의 '문서관리번호(mgtKey)'를 재사용하기 위해서는 삭제 (Delete API)
      를 호출해야 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "BUY"

        # 문서관리번호
        MgtKey = "2018-02-07-0509-4"

        # 메모
        Memo = "처리시 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.cancelRequest(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def refuse(request):
    """
    공급받는자에게 요청받은 역발행 세금계산서를 [거부]처리 합니다.
    - [거부]한 세금계산서의 '문서관리번호(mgtKey)'를 재사용하기 위해서는 삭제 (Delete API)
      를 호출해야 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-02-07-0509-1"

        # 메모
        Memo = "발행 메모"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.refuse(CorpNum, MgtKeyType, MgtKey, Memo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendToNTS(request):
    """
    [발행완료] 상태의 세금계산서를 국세청으로 즉시전송합니다.
    - 국세청 즉시전송을 호출하지 않은 경우 [발행완료] 상태의 세금계산서는 발행일 기준
      익일 오후 3시에 팝빌 시스템에서 일괄적으로 국세청으로 전송합니다.
    - 익일전송시 전송일이 법정공휴일인 경우 다음 영업일에 전송됩니다.
    - 국세청 전송에 관한 사항은 "[전자세금계산서 API 연동매뉴얼] > 1.3 국세청 전송 정책" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "201802061081"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.sendToNTS(CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfo(request):
    """
    1건의 세금계산서 상태/요약 정보를 확인합니다.
    - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "BIC-67890-18010403_00000"

        taxinvoiceInfo = taxinvoiceService.getInfo(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'Taxinvoice/GetInfo.html', {'taxinvoiceInfo': taxinvoiceInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getInfos(request):
    """
    다량의 세금계산서 상태/요약 정보를 확인합니다. (최대 1000건)
    - 세금계산서 항목별 정보는 "[전자세금계산서 API 연동매뉴얼] > 4.1. (세금)계산서
      구성"을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("2018-01-16-001")
        MgtKeyList.append("2018-01-16-008")
        MgtKeyList.append("2018-01-16-009")

        InfoList = taxinvoiceService.getInfos(CorpNum, MgtKeyType, MgtKeyList)

        return render(request, 'Taxinvoice/GetInfos.html', {'InfoList': InfoList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getDetailInfo(request):
    """
    1건의 세금계산서 상세항목을 확인합니다.
    - 응답항목에 대한 자세한 사항은 "[전자세금계산서 API 연동매뉴얼]  > 4.1 (세금)계산서 구성" 을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서 관리번호
        MgtKey = "2018-01-16-5555"

        taxinvoice = taxinvoiceService.getDetailInfo(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'Taxinvoice/GetDetailInfo.html', {'taxinvoice': taxinvoice})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 세금계산서 목록을 조회합니다.
    - 응답항목에 대한 자세한 사항은 "[전자세금계산서 API 연동매뉴얼] > 4.2. (세금)계산서 상태정보 구성"
      을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # [필수] 세금계산서 유형 SELL-매출, BUY-매입, TRUSTEE-위수탁
        MgtKeyType = "SELL"

        # [필수] 조회일자유형, W-작성일자, R-등록일자, I-발행일자
        DType = "W"

        # [필수] 시작일자, 표시형식(yyyyMMdd)
        SDate = "20171210"

        # [필수] 종료일자, 표시형식(yyyyMMdd)
        EDate = "20180116"

        # 세금계산서 상태코드 배열, 2,3번째 자리에 와일드카드(*) 사용가능
        State = ["3**", "6**"]

        # 문서유형 배열, N-일반 세금계산서, M-수정 세금계산서
        Type = ["N", "M"]

        # 과세형태 배열, T-과세, N-면세, Z-영세
        TaxType = ["T", "N", "Z"]

        # 발행형태 배열, N-정발행, R-역발행, T-위수탁
        IssueType = ["N", "R", "T"]

        # 지연발행 여부, 0-정상발행, 1-지연발행
        LateOnly = ""

        # 종사업장번호 유무, 공백-전체조회, 0-종사업장번호 없음, 1-종사업장번호 있음
        TaxRegIDYN = ""

        # 종사업장번호 사업자유형, S-공급자, B-공급받는자, T-수탁자
        TaxRegIDType = "S"

        # 종사업장번호, 다수작성시 콤마(",")로 구분하여 구성 ex) "0001,0007"
        TaxRegID = ""

        # 페이지번호
        Page = 1

        # 페이지당 검색개수
        PerPage = 5

        # 정렬 방향, D-내림차순, A-오름차순
        Order = "D"

        # 거래처 정보, 거래처 상호 또는 사업자등록번호 기재, 공백처리시 전체조회
        QString = ""

        # 연동문서 조회여부, 공백-전체조회, 0-일반문서 조회, 1-연동문서조회
        InterOPYN = ""

        response = taxinvoiceService.search(CorpNum, MgtKeyType, DType,
                                            SDate, EDate, State, Type, TaxType, LateOnly, TaxRegIDYN,
                                            TaxRegIDType, TaxRegID, Page, PerPage, Order, UserID,
                                            QString, InterOPYN, IssueType)

        return render(request, 'Taxinvoice/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getLogs(request):
    """
    세금계산서 상태 변경이력을 확인합니다.
    - 상태 변경이력 확인(GetLogs API) 응답항목에 대한 자세한 정보는 "[전자세금계산서 API 연동매뉴얼]
      > 3.5.5 상태 변경이력 확인" 을 참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-5555"

        LogList = taxinvoiceService.getLogs(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'Taxinvoice/GetLogs.html', {'LogList': LogList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL(request):
    """
    팝빌 전자세금계산서 관련 문서함 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # SBOX : 매출문서함, PBOX : 매입문서함 , TBOX : 임시문서함 , WRITE : 문서작성
        TOGO = "SBOX"

        url = taxinvoiceService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopUpURL(request):
    """
    1건의 전자세금계산서 보기 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180115-00001"

        url = taxinvoiceService.getPopUpURL(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPrintURL(request):
    """
    1건의 전자세금계산서 인쇄팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL의 유효시간은 30초입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-5555"

        url = taxinvoiceService.getPrintURL(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getEPrintURL(request):
    """
    세금계산서 인쇄(공급받는자) URL을 반환합니다.
    - URL 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "2018-01-16-5555"

        url = taxinvoiceService.getEPrintURL(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMassPrintURL(request):
    """
    다수건의 전자세금계산서 인쇄팝업 URL을 반환합니다. (최대 100건)
    - 반환된 URL은 보안정책에 따라 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 인쇄할 문서관리번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20161117-01")
        MgtKeyList.append("20161117-02")
        MgtKeyList.append("20161117-03")

        url = taxinvoiceService.getMassPrintURL(CorpNum, MgtKeyType, MgtKeyList)

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

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180103006"

        url = taxinvoiceService.getMailURL(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'url.html', {'url': url})
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

        url = taxinvoiceService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSealURL(request):
    """
    인감 및 첨부문서 등록 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getSealURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def attachFile(request):
    """
    세금계산서에 첨부파일을 등록합니다.
    - [임시저장] 상태의 세금계산서만 파일을 첨부할수 있습니다.
    - 첨부파일은 최대 5개까지 등록할 수 있습니다.
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180115-00003"

        # 파일경로
        FilePath = "./TaxinvoiceExample/static/image/attachfile.png"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.attachFile(CorpNum, MgtKeyType, MgtKey, FilePath, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def deleteFile(request):
    """
    세금계산서에 첨부된 파일을 삭제합니다.
    - 첨부파일을 식별하는 파일아이디는 첨부파일 목록(GetFiles API) 의 응답항목
      중 파일아이디(attachFile) 통해 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180115-00003"

        # 첨부파일 아이디, GetFiles API의 응답항목(AtachedFile) 확인.
        FileID = "8D13F961-CD77-4856-9501-1FB59CAFEE9E.PBF"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.deleteFile(CorpNum, MgtKeyType, MgtKey, FileID, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFiles(request):
    """
    세금계산서에 첨부된 파일의 목록을 확인합니다.
    - 응답항목 중 파일아이디(AttachedFile) 항목은 파일삭제(DeleteFile API)
      호출시 이용할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180115-00003"

        fileList = taxinvoiceService.getFiles(CorpNum, MgtKeyType, MgtKey)

        return render(request, 'Taxinvoice/GetFiles.html', {'fileList': fileList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendEmail(request):
    """
    세금계산서 발행 안내메일을 재전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180104qwe"

        # 수신메일주소
        ReceiverMail = "test@test.com"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.sendEmail(CorpNum, MgtKeyType, MgtKey, ReceiverMail, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
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

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180104qwe"

        # 발신번호
        Sender = "070-4304-2991"

        # 수신번호
        Receiver = "010-111-222"

        # 메시지 내용, 최대 90byte 초과시 길이가 조정되어 전송됨
        Contents = "발신문자 내용"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.sendSMS(CorpNum, MgtKeyType, MgtKey, Sender, Receiver,
                                             Contents, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFAX(request):
    """
    전자세금계산서를 팩스전송합니다.
    - 팩스 전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 전송내역 확인은 "팝빌 로그인" > [문자 팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서관리번호
        MgtKey = "20180104qwe"

        # 발신번호
        Sender = "070-4304-2991"

        # 수신팩스번호
        Receiver = "070-111-222"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.sendFax(CorpNum, MgtKeyType, MgtKey, Sender, Receiver, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def attachStatement(request):
    """
    1건의 전자명세서를 세금계산서에 첨부합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 세금계산서 문서관리번호
        MgtKey = "20180115-00003"

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "126"

        # 전자명세서 문서관리번호
        StmtMgtKey = "2018-01-16-888"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.attachStatement(CorpNum, MgtKeyType, MgtKey, ItemCode,
                                                     StmtMgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def detachStatement(request):
    """
    세금계산서에 첨부된 전자명세서 1건을 첨부해제합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서 관리번호
        MgtKey = "20180115-00003"

        # 전자명세서 종류코드, 121-거래명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
        ItemCode = "126"

        # 전자명세서 문서관리번호
        StmtMgtKey = "2018-01-16-888"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.detachStatement(CorpNum, MgtKeyType, MgtKey,
                                                     ItemCode, StmtMgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getEmailPublicKeys(request):
    """
    대용량 연계사업자 메일주소 목록을 반환합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        aspList = taxinvoiceService.getEmailPublicKeys(CorpNum)

        return render(request, 'Taxinvoice/GetEmailPublicKeys.html', {'aspList': aspList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def assignMgtKet(request):
    """
    팝빌사이트에서 작성된 세금계산서에 파트너 문서관리번호를 할당합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 세금계산서 아이템키, 문서 목록조회(Search) API의 반환항목중 ItemKey 참조
        ItemKey = '018081611481500001'

        # 할당할 문서관리번호, 숫자, 영문 '-', '_' 조합으로 1~24자리까지
        # 사업자번호별 중복없는 고유번호 할당
        MgtKey = "20180912-002"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.assignMgtKey(CorpNum, MgtKeyType, ItemKey, MgtKey, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listEmailConfig(request):
    """
    전자세금계산서 관련 메일전송 항목에 대한 전송여부를 목록으로 반환합니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        EmailConfig = taxinvoiceService.listEmailConfig(CorpNum, UserID)

        return render(request, 'Taxinvoice/ListEmailConfig.html', {'EmailConfig': EmailConfig})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateEmailConfig(request):
    """
    전자세금계산서 관련 메일전송 항목에 대한 전송여부를 수정합니다.
    메일전송유형
    [정발행]
    TAX_ISSUE : 공급받는자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_ISSUE_INVOICER : 공급자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_CHECK : 공급자에게 전자세금계산서가 수신확인 되었음을 알려주는 메일입니다.
    TAX_CANCEL_ISSUE : 공급받는자에게 전자세금계산서가 발행취소 되었음을 알려주는 메일입니다.

    [발행예정]
    TAX_SEND : 공급받는자에게 [발행예정] 세금계산서가 발송 되었음을 알려주는 메일입니다.
    TAX_ACCEPT : 공급자에게 [발행예정] 세금계산서가 승인 되었음을 알려주는 메일입니다.
    TAX_ACCEPT_ISSUE : 공급자에게 [발행예정] 세금계산서가 자동발행 되었음을 알려주는 메일입니다.
    TAX_DENY : 공급자에게 [발행예정] 세금계산서가 거부 되었음을 알려주는 메일입니다.
    TAX_CANCEL_SEND : 공급받는자에게 [발행예정] 세금계산서가 취소 되었음을 알려주는 메일입니다.

    [역발행]
    TAX_REQUEST : 공급자에게 세금계산서를 전자서명 하여 발행을 요청하는 메일입니다.
    TAX_CANCEL_REQUEST : 공급받는자에게 세금계산서가 취소 되었음을 알려주는 메일입니다.
    TAX_REFUSE : 공급받는자에게 세금계산서가 거부 되었음을 알려주는 메일입니다.

    [위수탁발행]
    TAX_TRUST_ISSUE : 공급받는자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_TRUST_ISSUE_TRUSTEE : 수탁자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_TRUST_ISSUE_INVOICER : 공급자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_TRUST_CANCEL_ISSUE : 공급받는자에게 전자세금계산서가 발행취소 되었음을 알려주는 메일입니다.
    TAX_TRUST_CANCEL_ISSUE_INVOICER : 공급자에게 전자세금계산서가 발행취소 되었음을 알려주는 메일입니다.

    [위수탁 발행예정]
    TAX_TRUST_SEND : 공급받는자에게 [발행예정] 세금계산서가 발송 되었음을 알려주는 메일입니다.
    TAX_TRUST_ACCEPT : 수탁자에게 [발행예정] 세금계산서가 승인 되었음을 알려주는 메일입니다.
    TAX_TRUST_ACCEPT_ISSUE : 수탁자에게 [발행예정] 세금계산서가 자동발행 되었음을 알려주는 메일입니다.
    TAX_TRUST_DENY : 수탁자에게 [발행예정] 세금계산서가 거부 되었음을 알려주는 메일입니다.
    TAX_TRUST_CANCEL_SEND : 공급받는자에게 [발행예정] 세금계산서가 취소 되었음을 알려주는 메일입니다.

    [처리결과]
    TAX_CLOSEDOWN : 거래처의 휴폐업 여부를 확인하여 안내하는 메일입니다.
    TAX_NTSFAIL_INVOICER : 전자세금계산서 국세청 전송실패를 안내하는 메일입니다.

    [정기발송]
    TAX_SEND_INFO : 전월 귀속분 [매출 발행 대기] 세금계산서의 발행을 안내하는 메일입니다.
    ETC_CERT_EXPIRATION : 팝빌에서 이용중인 공인인증서의 갱신을 안내하는 메일입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 메일 전송 유형
        EmailType = 'TAX_ISSUE'

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.updateEmailConfig(CorpNum, EmailType, SendYN, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCertificateExpireDate(request):
    """
    팝빌에 등록되어 있는 공인인증서의 만료일자를 확인합니다.
    - 공인인증서가 갱신/재발급/비밀번호 변경이 되는 경우 해당 인증서를
      재등록 하셔야 정상적으로 API를 이용하실 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        expiredate = taxinvoiceService.getCertificateExpireDate(CorpNum)

        return render(request, 'Taxinvoice/GetCertificateExpireDate.html', {'expiredate': expiredate})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getTaxCertURL(request):
    """
    공인인증서 등록 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getTaxCertURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API)
      를 통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = taxinvoiceService.getBalance(CorpNum)

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

        url = taxinvoiceService.getChargeURL(CorpNum, UserID)

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

        result = taxinvoiceService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-팝빌 파트너 포인트 충전 URL
        TOGO = "CHRG"

        url = taxinvoiceService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    전자세금계산서 발행시 차감되는 포인트 단가를 반환합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = taxinvoiceService.getUnitCost(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 전자세금계산서 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 가입여부 확인할 사업자 번호
        CorpNum = "1234567890"

        response = taxinvoiceService.checkIsMember(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    회원가입(JoinMember API)을 호출하기전 팝빌 회원아이디 중복여부를 확인합니다.
    """
    try:
        # 중복확인할 아이디
        targetID = "testkorea"

        response = taxinvoiceService.checkID(targetID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    파트너의 연동회원으로 회원가입을 요청합니다.
    아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    """
    try:
        # 연동회원 가입정보
        newMember = JoinForm(

            # 회원아이디 (4자 이상 50자 미만)
            ID="join_id_test",

            # 비밀번호, 최대 20자
            PWD="this_is_password",

            # 사업자번호
            CorpNum="0000000000",

            # 상호
            CorpName="테스트가입상호",

            # 대표자성명
            CEOName="테스트대표자성명",

            # 주소
            Addr="테스트회사주소",

            # 업태
            BizType="테스트업태",

            # 종목
            BizClass="테스트업종",

            # 담당자 성명
            ContactName="담당자성명",

            # 담당자 연락처
            ContactTEL="070-111-222",

            # 담당자 휴대폰번호
            ContactHP="010-111-222",

            # 담당자 팩스번호
            ContactFAX="070-111-222",

            # 담당자 메일주소
            ContactEmail="test@test.com"
        )

        response = taxinvoiceService.joinMember(newMember)

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

        response = taxinvoiceService.getCorpInfo(CorpNum, UserID)

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
            ceoname="대표자_성명",

            # 상호
            corpName="상호",

            # 주소
            addr="주소",

            # 업태
            bizType="업태",

            # 종목
            bizClass="종목"
        )

        response = taxinvoiceService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

            # 아이디 (4자 이상 50자 미만)
            id="popbill_test_id",

            # 비밀번호
            pwd="popbill_test_pwd",

            # 담당자명
            personName="담당자명",

            # 연락처
            tel="010-111-222",

            # 휴대폰번호
            hp="010-111-222",

            # 팩스번호
            fax="070-111-222",

            # 메일주소
            email="test@test.com",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True
        )

        response = taxinvoiceService.registContact(CorpNum, newContact, UserID)

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

        listContact = taxinvoiceService.listContact(CorpNum, UserID)

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
            id="UserID",

            # 담당자 성명
            personName="담당자_성명",

            # 연락처
            tel="010-111-111",

            # 휴대폰번호
            hp="010-111-111",

            # 팩스번호
            fax="070-111-222",

            # 메일주소
            email="test@test.com",

            # 회사조회 여부, True-회사조회, False-개인조회
            searchAllAllowYN=True
        )

        response = taxinvoiceService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkCertValidation(request):
    """
    팝빌에 등록된 공인인증서의 유효성을 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = taxinvoiceService.checkCertValidation(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
