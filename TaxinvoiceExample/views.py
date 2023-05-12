# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import (
    Contact,
    ContactInfo,
    CorpInfo,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
    Taxinvoice,
    TaxinvoiceDetail,
    TaxinvoiceService,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 TaxinvoiceService 객체 생성
taxinvoiceService = TaxinvoiceService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
taxinvoiceService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
taxinvoiceService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
taxinvoiceService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, 권장(True)
taxinvoiceService.UseLocalTimeYN = settings.UseLocalTimeYN

# 전자세금계산서 발행을 위해 인증서를 등록합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌사이트 로그인 > [전자세금계산서] > [환경설정] > [인증서 관리] 메뉴에서 등록
# 2. 인증서 등록 팝업 URL (getTaxCertURL API)을 이용하여 등록


def index(request):
    return render(request, "Taxinvoice/Index.html", {})


def checkMgtKeyInUse(request):
    """
    파트너가 세금계산서 관리 목적으로 할당하는 문서번호의 사용여부를 확인합니다.
    - 이미 사용 중인 문서번호는 중복 사용이 불가하고, 세금계산서가 삭제된 경우에만 문서번호의 재사용이 가능합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#CheckMgtKeyInUse
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호, 1~24자리, (영문,숫자,'-','_') 조합으로 사업자별로 중복되지 않도록 구성
        MgtKey = "20220805-001"

        keyInUse = taxinvoiceService.checkMgtKeyInUse(
            CorpNum, MgtKeyType, MgtKey)

        if keyInUse:
            result = "사용중"
        else:
            result = "미사용중"

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registIssue(request):
    """
    작성된 세금계산서 데이터를 팝빌에 저장과 동시에 발행(전자서명)하여 "발행완료" 상태로 처리합니다.
    - 세금계산서 국세청 전송 정책 [https://developers.popbill.com/guide/taxinvoice/python/introduction/policy-of-send-to-nts]
    - "발행완료"된 전자세금계산서는 국세청 전송 이전에 발행취소(CancelIssue API) 함수로 국세청 신고 대상에서 제외할 수 있습니다.
    - 임시저장(Register API) 함수와 발행(Issue API) 함수를 한 번의 프로세스로 처리합니다.
    - 세금계산서 발행을 위해서 공급자의 인증서가 팝빌 인증서버에 사전등록 되어야 합니다.
        └ 위수탁발행의 경우, 수탁자의 인증서 등록이 필요합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#RegistIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
        MgtKey = "20220805-002"

        # 지연발행 강제여부  (true / false 중 택 1)
        # └ true = 가능 , false = 불가능
        # - 미입력 시 기본값 false 처리
        # - 발행마감일이 지난 세금계산서를 발행하는 경우, 가산세가 부과될 수 있습니다.
        # - 가산세가 부과되더라도 발행을 해야하는 경우에는 forceIssue의 값을
        #   true로 선언하여 발행(Issue API)를 호출하시면 됩니다.
        forceIssue = False

        # 거래명세서 동시작성여부 (true / false 중 택 1)
        # └ true = 사용 , false = 미사용
        # - 미입력 시 기본값 false 처리
        writeSpecification = False

        # {writeSpecification} = true인 경우, 거래명세서 문서번호 할당
        # - 미입력시 기본값 세금계산서 문서번호와 동일하게 할당
        dealInvoiceMgtKey = ""

        # 메모
        memo = "즉시발행 메모"

        # 발행안내 메일 제목, 미기재시 기본양식으로 전송
        emailSubject = ""

        # 세금계산서 정보
        taxinvoice = Taxinvoice(
            # 작성일자, 날짜형식(yyyyMMdd) ex)20220805
            writeDate="20220805",
            # 과금방향, {정과금} 기재
            chargeDirection="정과금",
            # 발행형태, {정발행, 위수탁} 중 기재
            issueType="정발행",
            # {영수, 청구, 없음} 중 기재
            purposeType="영수",
            # 과세형태, {과세, 영세, 면세} 중 기재
            taxType="과세",
            ######################################################################
            #                             공급자 정보
            ######################################################################
            # 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,
            # 공급자 상호
            invoicerCorpName="공급자 상호",
            # 공급자 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
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
            invoicerEmail="",
            # 공급자 담당자 연락처
            invoicerTEL="",
            # 공급자 담당자 휴대폰 번호
            invoicerHP="",
            # 발행 안내 문자 전송여부 (true / false 중 택 1)
            # └ true = 전송 , false = 미전송
            # └ 공급받는자 (주)담당자 휴대폰번호 {invoiceeHP1} 값으로 문자 전송
            # - 전송 시 포인트 차감되며, 전송실패시 환불처리
            invoicerSMSSendYN=False,
            ######################################################################
            #                            공급받는자 정보
            ######################################################################
            # 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",
            # 공급받는자 사업자번호
            # - {invoiceeType}이 "사업자" 인 경우, 사업자번호 (하이픈 ('-') 제외 10자리)
            # - {invoiceeType}이 "개인" 인 경우, 주민등록번호 (하이픈 ('-') 제외 13자리)
            # - {invoiceeType}이 "외국인" 인 경우, "9999999999999" (하이픈 ('-') 제외 13자리)
            invoiceeCorpNum="8888888888",
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,
            # 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",
            # [역발행시 필수] 공급받는자 문서번호, 1~24자리 (숫자, 영문, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey=None,
            # 공급받는자 대표자 성명
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
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            invoiceeEmail1="",
            # 공급받는자 연락처
            invoiceeTEL1="",
            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="",
            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="",
            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################
            # 공급가액 합계
            supplyCostTotal="100000",
            # 세액 합계
            taxTotal="10000",
            # 합계금액, 공급가액 합계 + 세액 합계
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
            # 비고
            # {invoiceeType}이 "외국인" 이면 remark1 필수
            # - 외국인 등록번호 또는 여권번호 입력
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 기재상 '권' 항목, 최대값 32767
            # 미기재시 kwon=None,
            kwon=1,
            # 기재상 '호' 항목, 최대값 32767
            # 미기재시 ho=None,
            ho=2,
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - https://developers.popbill.com/guide/taxinvoice/python/introduction/modified-taxinvoice
            ######################################################################
            # 수정세금계산서 정보 수정사유별로 1~6중 선택기재
            # 수정사유코드
            modifyCode=None,
            # 원본세금계산서 국세청승인번호 기재
            orgNTSConfirmNum=None,
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = []

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = []

        taxinvoice.addContactList.append(
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        taxinvoice.addContactList.append(
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        response = taxinvoiceService.registIssue(
            CorpNum,
            taxinvoice,
            writeSpecification,
            forceIssue,
            dealInvoiceMgtKey,
            memo,
            emailSubject,
        )

        return render(
            request,
            "response.html",
            {
                "code": response.code,
                "message": response.message,
                "ntsConfirmNum": response.ntsConfirmNum,
            },
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def bulkSubmit(request):
    """
    최대 100건의 세금계산서 발행을 한번의 요청으로 접수합니다.
    - 세금계산서 발행을 위해서 공급자의 인증서가 팝빌 인증서버에 사전등록 되어야 합니다.
        └ 위수탁발행의 경우, 수탁자의 인증서 등록이 필요합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#BulkSubmit
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 제출아이디
        # 최대 36자리 영문, 숫자, '-' 조합으로 구성
        submitID = "PYTHON-DJANGO-BULK"

        # 지연발행 강제여부  (true / false 중 택 1)
        # └ true = 가능 , false = 불가능
        # - 미입력 시 기본값 false 처리
        # - 발행마감일이 지난 세금계산서를 발행하는 경우, 가산세가 부과될 수 있습니다.
        # - 가산세가 부과되더라도 발행을 해야하는 경우에는 forceIssue의 값을
        #   true로 선언하여 발행(Issue API)를 호출하시면 됩니다.
        forceIssue = False

        # 세금계산서 객체정보 리스트
        taxinvoicelist = []
        for i in range(0, 20):
            taxinvoicelist.append(
                Taxinvoice(
                    # 작성일자, 날짜형식(yyyyMMdd) ex)20220805
                    writeDate="20220805",
                    # 과금방향, [정과금(공급자)] 기재
                    chargeDirection="정과금",
                    # 발행형태, {정발행, 위수탁} 중 기재
                    issueType="정발행",
                    # {영수, 청구, 없음} 중 기재
                    purposeType="영수",
                    # 과세형태, {과세, 영세, 면세} 중 기재
                    taxType="과세",
                    ######################################################################
                    #                             공급자 정보
                    ######################################################################
                    # 공급자 사업자번호 , '-' 없이 10자리 기재.
                    invoicerCorpNum=settings.testCorpNum,
                    # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
                    invoicerTaxRegID=None,
                    # 공급자 상호
                    invoicerCorpName="공급자 상호",
                    # 공급자 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
                    # 사업자별로 중복되지 않도록 구성
                    invoicerMgtKey=submitID + "-" + str(i),
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
                    invoicerEmail="",
                    # 공급자 담당자 연락처
                    invoicerTEL="",
                    # 공급자 담당자 휴대폰 번호
                    invoicerHP="",
                    # 발행 안내 문자 전송여부 (true / false 중 택 1)
                    # └ true = 전송 , false = 미전송
                    # └ 공급받는자 (주)담당자 휴대폰번호 {invoiceeHP1} 값으로 문자 전송
                    # - 전송 시 포인트 차감되며, 전송실패시 환불처리
                    invoicerSMSSendYN=False,
                    ######################################################################
                    #                            공급받는자 정보
                    ######################################################################
                    # 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
                    invoiceeType="사업자",
                    # 공급받는자 사업자번호
                    # - {invoiceeType}이 "사업자" 인 경우, 사업자번호 (하이픈 ('-') 제외 10자리)
                    # - {invoiceeType}이 "개인" 인 경우, 주민등록번호 (하이픈 ('-') 제외 13자리)
                    # - {invoiceeType}이 "외국인" 인 경우, "9999999999999" (하이픈 ('-') 제외 13자리)
                    invoiceeCorpNum="8888888888",
                    # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
                    invoiceeTaxRegID=None,
                    # 공급받는자 상호
                    invoiceeCorpName="BulkTEST 상호",
                    # [역발행시 필수] 공급받는자 문서번호, 1~24자리 (숫자, 영문, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
                    invoiceeMgtKey=None,
                    # 공급받는자 대표자 성명
                    invoiceeCEOName="BulkTEST 대표자 성명",
                    # 공급받는자 주소
                    invoiceeAddr="BulkTEST 주소",
                    # 공급받는자 종목
                    invoiceeBizClass="BulkTEST 종목",
                    # 공급받는자 업태
                    invoiceeBizType="BulkTEST 업태",
                    # 공급받는자 담당자 성명
                    invoiceeContactName1="BulkTEST 담당자",
                    # 공급받는자 담당자 메일주소
                    # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
                    # 실제 거래처의 메일주소가 기재되지 않도록 주의
                    invoiceeEmail1="",
                    # 공급받는자 연락처
                    invoiceeTEL1="",
                    # 공급받는자 담당자 휴대폰번호
                    invoiceeHP1="",
                    # 공급받는자 담당자 팩스번호
                    invoiceeFAX1="",
                    ######################################################################
                    #                          세금계산서 기재정보
                    ######################################################################
                    # 공급가액 합계
                    supplyCostTotal="100000",
                    # 세액 합계
                    taxTotal="10000",
                    # 합계금액, 공급가액 합계 + 세액 합계
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
                    # 비고
                    # {invoiceeType}이 "외국인" 이면 remark1 필수
                    # - 외국인 등록번호 또는 여권번호 입력
                    remark1="비고1",
                    remark2="비고2",
                    remark3="비고3",
                    # 기재상 '권' 항목, 최대값 32767
                    # 미기재시 kwon=None,
                    kwon=1,
                    # 기재상 '호' 항목, 최대값 32767
                    # 미기재시 ho=None,
                    ho=2,
                    # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
                    # └ true = 첨부 , false = 미첨부(기본값)
                    # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
                    businessLicenseYN=False,
                    # 통장사본 이미지 첨부여부  (true / false 중 택 1)
                    # └ true = 첨부 , false = 미첨부(기본값)
                    # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
                    bankBookYN=False,
                    ######################################################################
                    #                           상세항목(품목) 정보
                    ######################################################################
                    # 상세항목 0~99개 까지 작성가능.
                    # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
                    detailList=[
                        TaxinvoiceDetail(
                            serialNum=1,
                            purchaseDT="20220805",
                            itemName="품목1",
                            spec="규격",
                            qty=1,
                            unitCost="100000",
                            supplyCost="100000",
                            tax="10000",
                            remark="품목비고",
                        )
                    ],
                )
            )

        bulkResponse = taxinvoiceService.bulkSubmit(
            CorpNum, submitID, taxinvoicelist, forceIssue
        )

        return render(
            request,
            "Taxinvoice/BulkResponse.html",
            {
                "code": bulkResponse.code,
                "message": bulkResponse.message,
                "receiptID": bulkResponse.receiptID,
            },
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBulkResult(request):
    """
    접수시 기재한 SubmitID를 사용하여 세금계산서 접수결과를 확인합니다.
    - 개별 세금계산서 처리상태는 접수상태(txState)가 완료(2) 시 반환됩니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#GetBulkResult
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 제출아이디
        # 최대 36자리 영문, 숫자, '-' 조합으로 구성
        submitID = "PYTHON-DJANGO-BULK"

        bulkTaxinvoiceResult = taxinvoiceService.getBulkResult(
            CorpNum, submitID)

        return render(
            request,
            "Taxinvoice/BulkResult.html",
            {"bulkTaxinvoiceResult": bulkTaxinvoiceResult},
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def register(request):
    """
    작성된 세금계산서 데이터를 팝빌에 저장합니다.
    - "임시저장" 상태의 세금계산서는 발행(Issue) 함수를 호출하여 "발행완료" 처리한 경우에만 국세청으로 전송됩니다.
    - 정발행 시 임시저장(Register)과 발행(Issue)을 한번의 호출로 처리하는 즉시발행(RegistIssue API) 프로세스 연동을 권장합니다.
    - 역발행 시 임시저장(Register)과 역발행요청(Request)을 한번의 호출로 처리하는 즉시요청(RegistRequest API) 프로세스 연동을 권장합니다.
    - 세금계산서 파일첨부 기능을 구현하는 경우, 임시저장(Register API) -> 파일첨부(AttachFile API) -> 발행(Issue API) 함수를 차례로 호출합니다.
    - 임시저장된 세금계산서는 팝빌 사이트 '임시문서함'에서 확인 가능합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Register
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
        # 사업자별로 중복되지 않도록 구성
        MgtKey = "20220805-001"

        # 거래명세서 동시작성여부 (true / false 중 택 1)
        # └ true = 사용 , false = 미사용
        # - 미입력 시 기본값 false 처리
        writeSpecification = False

        # 세금계산서 정보
        taxinvoice = Taxinvoice(
            # 작성일자, 날짜형식(yyyyMMdd) ex)20220805
            writeDate="20220805",
            # 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",
            # 발행형태, {정발행, 역발행, 위수탁} 중 기재
            issueType="정발행",
            # {영수, 청구, 없음} 중 기재
            purposeType="영수",
            # 과세형태, {과세, 영세, 면세} 중 기재
            taxType="과세",
            ######################################################################
            #                             공급자 정보
            ######################################################################
            # 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,
            # 공급자 상호
            invoicerCorpName="공급자 상호",
            # 공급자 문서번호, 1~24자리, (영문, 숫자, '-', '_')조합으로 사업자별로 중복되지 않도록 구성
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
            invoicerEmail="",
            # 공급자 담당자 연락처
            invoicerTEL="",
            # 공급자 담당자 휴대폰 번호
            invoicerHP="",
            # 발행 안내 문자 전송여부 (true / false 중 택 1)
            # └ true = 전송 , false = 미전송
            # └ 공급받는자 (주)담당자 휴대폰번호 {invoiceeHP1} 값으로 문자 전송
            # - 전송 시 포인트 차감되며, 전송실패시 환불처리
            invoicerSMSSendYN=False,
            ######################################################################
            #                            공급받는자 정보
            ######################################################################
            # 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,
            # 공급받는자 사업자번호
            # - {invoiceeType}이 "사업자" 인 경우, 사업자번호 (하이픈 ('-') 제외 10자리)
            # - {invoiceeType}이 "개인" 인 경우, 주민등록번호 (하이픈 ('-') 제외 13자리)
            # - {invoiceeType}이 "외국인" 인 경우, "9999999999999" (하이픈 ('-') 제외 13자리)
            invoiceeCorpNum="8888888888",
            # 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",
            # [역발행시 필수] 공급받는자 문서번호, , 1~24자리, (영문, 숫자, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey=None,
            # 공급받는자 대표자 성명
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
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            invoiceeEmail1="",
            # 공급받는자 연락처
            invoiceeTEL1="",
            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="",
            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="",
            # 역발행 요청시 알림문자 전송여부 (역발행에서만 사용가능)
            # - 공급자 담당자 휴대폰번호(invoicerHP)로 전송
            # - 전송시 포인트가 차감되며 전송실패하는 경우 포인트 환불처리
            invoiceeSMSSendYN=False,
            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################
            # 공급가액 합계
            supplyCostTotal="100000",
            # 세액 합계
            taxTotal="10000",
            # 합계금액, 공급가액 합계 + 세액 합계
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
            # 비고
            # {invoiceeType}이 "외국인" 이면 remark1 필수
            # - 외국인 등록번호 또는 여권번호 입력
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 기재상 '권' 항목, 최대값 32767
            # 미기재시 kwon=None,
            kwon=1,
            # 기재상 '호' 항목, 최대값 32767
            # 미기재시 ho=None,
            ho=2,
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - https://developers.popbill.com/guide/taxinvoice/python/introduction/modified-taxinvoice
            ######################################################################
            # 수정세금계산서 정보
            # 수정사유코드, 수정사유별로 1~6중 선택기재
            modifyCode=None,
            # 원본세금계산서 국세청승인번호 기재
            orgNTSConfirmNum=None,
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = []

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = []

        taxinvoice.addContactList.append(
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        taxinvoice.addContactList.append(
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        response = taxinvoiceService.register(
            CorpNum, taxinvoice, writeSpecification)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def update(request):
    """
    "임시저장" 상태의 세금계산서를 수정합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Update
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        # 세금계산서 정보
        taxinvoice = Taxinvoice(
            # 작성일자, 날짜형식(yyyyMMdd) ex)20220805
            writeDate="20220805",
            # 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",
            # 발행형태, {정발행, 역발행, 위수탁} 중 기재
            issueType="정발행",
            # {영수, 청구, 없음} 중 기재
            purposeType="영수",
            # 과세형태, {과세, 영세, 면세} 중 기재
            taxType="과세",
            ######################################################################
            #                             공급자 정보
            ######################################################################
            # 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum=settings.testCorpNum,
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,
            # 공급자 상호
            invoicerCorpName="공급자 상호",
            # 공급자 문서번호
            invoicerMgtKey=MgtKey,
            # 공급자 대표자 성명
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
            invoicerEmail="",
            # 공급자 담당자 연락처
            invoicerTEL="",
            # 공급자 담당자 휴대폰 번호
            invoicerHP="",
            # 발행 안내 문자 전송여부 (true / false 중 택 1)
            # └ true = 전송 , false = 미전송
            # └ 공급받는자 (주)담당자 휴대폰번호 {invoiceeHP1} 값으로 문자 전송
            # - 전송 시 포인트 차감되며, 전송실패시 환불처리
            invoicerSMSSendYN=False,
            ######################################################################
            #                            공급받는자 정보
            ######################################################################
            # 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,
            # 공급받는자 사업자번호
            # - {invoiceeType}이 "사업자" 인 경우, 사업자번호 (하이픈 ('-') 제외 10자리)
            # - {invoiceeType}이 "개인" 인 경우, 주민등록번호 (하이픈 ('-') 제외 13자리)
            # - {invoiceeType}이 "외국인" 인 경우, "9999999999999" (하이픈 ('-') 제외 13자리)
            invoiceeCorpNum="8888888888",
            # 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",
            # [역발행시 필수] 공급받는자 문서번호
            invoiceeMgtKey=None,
            # 공급받는자 대표자 성명
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
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            invoiceeEmail1="",
            # 공급받는자 연락처
            invoiceeTEL1="",
            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="",
            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="",
            # 역발행 요청시 알림문자 전송여부 (역발행에서만 사용가능)
            # - 공급자 담당자 휴대폰번호(invoicerHP)로 전송
            # - 전송시 포인트가 차감되며 전송실패하는 경우 포인트 환불처리
            invoiceeSMSSendYN=False,
            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################
            # 공급가액 합계
            supplyCostTotal="100000",
            # 세액 합계
            taxTotal="10000",
            # 합계금액, 공급가액 합계 + 세액 합계
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
            # 비고
            # {invoiceeType}이 "외국인" 이면 remark1 필수
            # - 외국인 등록번호 또는 여권번호 입력
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 기재상 '권' 항목, 최대값 32767
            # 미기재시 kwon=None,
            kwon=1,
            # 기재상 '호' 항목, 최대값 32767
            # 미기재시 ho=None,
            ho=2,
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - https://developers.popbill.com/guide/taxinvoice/python/introduction/modified-taxinvoice
            ######################################################################
            # 수정세금계산서 정보
            # 수정사유코드, 수정사유별로 1~6중 선택기재
            modifyCode=None,
            # 원본세금계산서 국세청승인번호 기재
            orgNTSConfirmNum=None,
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = []

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        ######################################################################
        #                           추가담당자 정보
        # - 세금계산서 발행안내 메일을 수신받을 공급받는자 담당자가 다수인 경우
        #   담당자 정보를 추가하여 발행안내메일을 다수에게 전송할 수 있습니다.
        ######################################################################

        # 최대 5개까지 기재 가능
        taxinvoice.addContactList = []

        taxinvoice.addContactList.append(
            Contact(
                serialNum=1,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        taxinvoice.addContactList.append(
            Contact(
                serialNum=2,  # 일련번호, 1부터 순차기재
                contactName="추가담당자 성명",  # 담당자명
                email="test1@test.com",  # 메일주소
            )
        )

        response = taxinvoiceService.update(
            CorpNum, MgtKeyType, MgtKey, taxinvoice)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def issue(request):
    """
    "임시저장" 또는 "(역)발행대기" 상태의 세금계산서를 발행(전자서명)하며, "발행완료" 상태로 처리합니다.
    - 세금계산서 국세청 전송정책 [https://developers.popbill.com/guide/taxinvoice/python/introduction/policy-of-send-to-nts]
    - "발행완료" 된 전자세금계산서는 국세청 전송 이전에 발행취소(CancelIssue API) 함수로 국세청 신고 대상에서 제외할 수 있습니다.
    - 세금계산서 발행을 위해서 공급자의 인증서가 팝빌 인증서버에 사전등록 되어야 합니다.
        └ 위수탁발행의 경우, 수탁자의 인증서 등록이 필요합니다.
    - 세금계산서 발행 시 공급받는자에게 발행 메일이 발송됩니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Issue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        # 메모
        Memo = "발행 메모"

        # 발행 안내메일 제목, 미기재시 기본양식으로 전송
        EmailSubject = None

        # 지연발행 강제여부, 기본값 - False
        # 발행마감일이 지난 세금계산서를 발행하는 경우, 가산세가 부과될 수 있습니다.
        # 지연발행 세금계산서를 신고해야 하는 경우 forceIssue 값을 True로 선언하여
        # 발행(Issue API)을 호출할 수 있습니다.
        ForceIssue = False

        response = taxinvoiceService.issue(
            CorpNum, MgtKeyType, MgtKey, Memo, EmailSubject, ForceIssue
        )

        return render(
            request,
            "response.html",
            {
                "code": response.code,
                "message": response.message,
                "ntsConfirmNum": response.ntsConfirmNum,
            },
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def cancelIssue(request):
    """
    국세청 전송 이전 "발행완료" 상태의 세금계산서를 "발행취소"하고 국세청 전송 대상에서 제외합니다.
    - Delete(삭제)함수를 호출하여 "발행취소" 상태의 전자세금계산서를 삭제하면, 문서번호 재사용이 가능합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#CancelIssue
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        # 메모
        Memo = "발행취소 메모"

        response = taxinvoiceService.cancelIssue(
            CorpNum, MgtKeyType, MgtKey, Memo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registRequest(request):
    """
    공급받는자가 작성한 세금계산서 데이터를 팝빌에 저장하고 공급자에게 송부하여 발행을 요청합니다.
    - 역발행 세금계산서 프로세스를 구현하기 위해서는 공급자/공급받는자가 모두 팝빌에 회원이여야 합니다.
    - 발행 요청된 세금계산서는 "(역)발행대기" 상태이며, 공급자가 팝빌 사이트 또는 함수를 호출하여 발행한 경우에만 국세청으로 전송됩니다.
    - 공급자는 팝빌 사이트의 "매출 발행 대기함"에서 발행대기 상태의 역발행 세금계산서를 확인할 수 있습니다.
    - 임시저장(Register API) 함수와 역발행 요청(Request API) 함수를 한 번의 프로세스로 처리합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#RegistRequest
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로
        # 사업자별로 중복되지 않도록 구성
        MgtKey = "20220805-003"

        # 세금계산서 정보
        taxinvoice = Taxinvoice(
            # 작성일자, 날짜형식(yyyyMMdd) ex)20220805
            writeDate="20220805",
            # 과금방향, [정과금(공급자), 역과금(공급받는자)]중 기재
            # 역과금의 경우 역발행세금계산서 발행시에만 사용가능
            chargeDirection="정과금",
            # 발행형태, {역발행} 중 기재
            issueType="역발행",
            # {영수, 청구, 없음} 중 기재
            purposeType="영수",
            # 과세형태, {과세, 영세, 면세} 중 기재
            taxType="과세",
            ######################################################################
            #                             공급자 정보
            ######################################################################
            # 공급자 사업자번호 , '-' 없이 10자리 기재.
            invoicerCorpNum="8888888888",
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoicerTaxRegID=None,
            # 공급자 상호
            invoicerCorpName="공급자 상호",
            # 공급자 문서번호, 1~24자리, (영문, 숫자, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
            invoicerMgtKey="",
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
            invoicerEmail="",
            # 공급자 담당자 연락처
            invoicerTEL="",
            # 공급자 담당자 휴대폰 번호
            invoicerHP="",
            # 정발행시 공급받는자에게 발행안내문자 전송여부
            invoicerSMSSendYN=False,
            ######################################################################
            #                            공급받는자 정보
            ######################################################################
            # 공급받는자 구분, [사업자, 개인, 외국인] 중 기재
            invoiceeType="사업자",
            # 공급받는자 사업자번호
            # - {invoiceeType}이 "사업자" 인 경우, 사업자번호 (하이픈 ('-') 제외 10자리)
            # - {invoiceeType}이 "개인" 인 경우, 주민등록번호 (하이픈 ('-') 제외 13자리)
            # - {invoiceeType}이 "외국인" 인 경우, "9999999999999" (하이픈 ('-') 제외 13자리)
            invoiceeCorpNum=CorpNum,
            # 공급자 종사업장 식별번호, 필요시 숫자 4자리 기재
            invoiceeTaxRegID=None,
            # 공급받는자 상호
            invoiceeCorpName="공급받는자 상호",
            # [역발행시 필수] 공급받는자 문서번호, 1~24자리 (숫자, 영문, '-', '_') 조합으로 사업자별로 중복되지 않도록 구성
            invoiceeMgtKey=MgtKey,
            # 공급받는자 대표자 성명
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
            # 팝빌 개발환경에서 테스트하는 경우에도 안내 메일이 전송되므로,
            # 실제 거래처의 메일주소가 기재되지 않도록 주의
            invoiceeEmail1="",
            # 공급받는자 연락처
            invoiceeTEL1="",
            # 공급받는자 담당자 휴대폰번호
            invoiceeHP1="",
            # 공급받는자 담당자 팩스번호
            invoiceeFAX1="",
            # 역발행시 공급자에게 발행안내문자 전송여부
            invoiceeSMSSendYN=False,
            ######################################################################
            #                          세금계산서 기재정보
            ######################################################################
            # 공급가액 합계
            supplyCostTotal="100000",
            # 세액 합계
            taxTotal="10000",
            # 합계금액, 공급가액 합계 + 세액 합계
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
            # 비고
            # {invoiceeType}이 "외국인" 이면 remark1 필수
            # - 외국인 등록번호 또는 여권번호 입력
            remark1="비고1",
            remark2="비고2",
            remark3="비고3",
            # 기재상 '권' 항목, 최대값 32767
            # 미기재시 kwon=None,
            kwon=1,
            # 기재상 '호' 항목, 최대값 32767
            # 미기재시 ho=None,
            ho=2,
            # 사업자등록증 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            businessLicenseYN=False,
            # 통장사본 이미지 첨부여부  (true / false 중 택 1)
            # └ true = 첨부 , false = 미첨부(기본값)
            # - 팝빌 사이트 또는 인감 및 첨부문서 등록 팝업 URL (GetSealURL API) 함수를 이용하여 등록
            bankBookYN=False,
            ######################################################################
            #                 수정세금계산서 정보 (수정세금계산서 발행시에만 기재)
            # - 수정세금계산서 관련 정보는 연동매뉴얼 또는 개발가이드 링크 참조
            # - [참고] 수정세금계산서 작성방법 안내 - https://developers.popbill.com/guide/taxinvoice/python/introduction/modified-taxinvoice
            ######################################################################
            # 수정세금계산서 정보 수정사유별로 1~6중 선택기재
            # 수정사유코드
            modifyCode=None,
            # 원본세금계산서 국세청승인번호 기재
            orgNTSConfirmNum=None,
        )

        ######################################################################
        #                           상세항목(품목) 정보
        ######################################################################

        # 상세항목 0~99개 까지 작성가능.
        # 일련번호 (serialNum) 는 1부터 99까지 순차기재.
        taxinvoice.detailList = []

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=1,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목1",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공급가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        taxinvoice.detailList.append(
            TaxinvoiceDetail(
                serialNum=2,  # 일련번호, 1부터 순차기재
                purchaseDT="20220805",  # 거래일자, yyyyMMdd
                itemName="품목2",  # 품목
                spec="규격",  # 규격
                qty=1,  # 수량
                unitCost="50000",  # 단가
                supplyCost="50000",  # 공가액
                tax="5000",  # 세액
                remark="품목비고",  # 비고
            )
        )

        memo = "역발행 즉시요청 메모"

        response = taxinvoiceService.registRequest(CorpNum, taxinvoice, memo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def request(request):
    """
    공급받는자가 저장된 역발행 세금계산서를 공급자에게 송부하여 발행 요청합니다.
    - 역발행 세금계산서 프로세스를 구현하기 위해서는 공급자/공급받는자가 모두 팝빌에 회원이여야 합니다.
    - 역발행 요청후 공급자가 [발행] 처리시 포인트가 차감되며 역발행 세금계산서 항목중 과금방향(ChargeDirection) 에 기재한 값에 따라
        └ 정과금(공급자과금) 또는 역과금(공급받는자과금) 처리됩니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Request
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "BUY"

        # 문서번호
        MgtKey = "20220805-999"

        # 메모
        Memo = "역발행 요청 메모"

        response = taxinvoiceService.request(CorpNum, MgtKeyType, MgtKey, Memo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def cancelRequest(request):
    """
    공급자가 요청받은 역발행 세금계산서를 발행하기 전, 공급받는자가 역발행요청을 취소합니다.
    - 함수 호출시 상태 값이 "취소"로 변경되고, 해당 역발행 세금계산서는 공급자에 의해 발행 될 수 없습니다.
    - [취소]한 세금계산서의 문서번호를 재사용하기 위해서는 삭제 (Delete API) 함수를 호출해야 합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#CancelRequest
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "BUY"

        # 문서번호
        MgtKey = "20220805-003"

        # 메모
        Memo = "처리시 메모"

        response = taxinvoiceService.cancelRequest(
            CorpNum, MgtKeyType, MgtKey, Memo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refuse(request):
    """
    공급자가 공급받는자에게 역발행 요청 받은 세금계산서의 발행을 거부합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Refuse
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-003"

        # 메모
        Memo = "발행 메모"

        response = taxinvoiceService.refuse(CorpNum, MgtKeyType, MgtKey, Memo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def delete(request):
    """
    삭제 가능한 상태의 세금계산서를 삭제합니다.
    - 삭제 가능한 상태: "임시저장", "발행취소", "역발행거부", "역발행취소", "전송실패"
    - 세금계산서를 삭제해야만 문서번호(mgtKey)를 재사용할 수 있습니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#Delete
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        response = taxinvoiceService.delete(CorpNum, MgtKeyType, MgtKey)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendToNTS(request):
    """
    "발행완료" 상태의 전자세금계산서를 국세청에 즉시 전송하며, 함수 호출 후 최대 30분 이내에 전송 처리가 완료됩니다.
    - 국세청 즉시전송을 호출하지 않은 세금계산서는 발행일 기준 다음 영업일 오후 3시에 팝빌 시스템에서 일괄적으로 국세청으로 전송합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/issue#SendToNTS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        response = taxinvoiceService.sendToNTS(CorpNum, MgtKeyType, MgtKey)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfo(request):
    """
    세금계산서 1건의 상태 및 요약정보를 확인합니다.
    - 리턴값 'TaxinvoiceInfo'의 변수 'stateCode'를 통해 세금계산서의 상태코드를 확인합니다.
    - 세금계산서 상태코드 [https://developers.popbill.com/reference/taxinvoice/python/response-code#state-code]
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        taxinvoiceInfo = taxinvoiceService.getInfo(CorpNum, MgtKeyType, MgtKey)

        return render(
            request, "Taxinvoice/GetInfo.html", {
                "taxinvoiceInfo": taxinvoiceInfo}
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getInfos(request):
    """
    다수건의 세금계산서 상태 및 요약 정보를 확인합니다. (1회 호출 시 최대 1,000건 확인 가능)
    - 리턴값 'TaxinvoiceInfo'의 변수 'stateCode'를 통해 세금계산서의 상태코드를 확인합니다.
    - 세금계산서 상태코드 [https://developers.popbill.com/reference/taxinvoice/python/response-code#state-code]
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetInfos
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호 배열, 최대 1000건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")

        InfoList = taxinvoiceService.getInfos(CorpNum, MgtKeyType, MgtKeyList)

        return render(request, "Taxinvoice/GetInfos.html", {"InfoList": InfoList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getDetailInfo(request):
    """
    세금계산서 1건의 상세정보를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetDetailInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        taxinvoice = taxinvoiceService.getDetailInfo(
            CorpNum, MgtKeyType, MgtKey)

        return render(
            request, "Taxinvoice/GetDetailInfo.html", {
                "taxinvoice": taxinvoice}
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getXML(request):
    """
    세금계산서 1건의 상세정보를 XML로 반환합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetXML
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        taxinvoiceXML = taxinvoiceService.getXML(CorpNum, MgtKeyType, MgtKey)

        return render(
            request, "Taxinvoice/GetXML.html", {"taxinvoiceXML": taxinvoiceXML}
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    검색조건에 해당하는 세금계산서를 조회합니다. (조회기간 단위 : 최대 6개월)
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 유형 SELL-매출, BUY-매입, TRUSTEE-위수탁
        MgtKeyType = "SELL"

        # 일자 유형 ("R" , "W" , "I" 중 택 1)
        # └ R = 등록일자 , W = 작성일자 , I = 발행일자
        DType = "W"

        # 시작일자, 표시형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 표시형식(yyyyMMdd)
        EDate = "20220731"

        # 상태코드 배열 (2,3번째 자리에 와일드카드(*) 사용 가능)
        # - 미입력시 전체조회
        State = ["3**", "6**"]

        # 문서 유형 배열 ("N" , "M" 중 선택, 다중 선택 가능)
        # - N = 일반 세금계산서 , M = 수정 세금계산서
        # - 미입력시 전체조회
        Type = ["N", "M"]

        # 과세형태 배열 ("T" , "N" , "Z" 중 선택, 다중 선택 가능)
        # - T = 과세 , N = 면세 , Z = 영세
        # - 미입력시 전체조회
        TaxType = ["T", "N", "Z"]

        # 발행형태 배열 ("N" , "R" , "T" 중 선택, 다중 선택 가능)
        # - N = 정발행 , R = 역발행 , T = 위수탁발행
        # - 미입력시 전체조회
        IssueType = ["N", "R", "T"]

        # 등록유형 배열 ("P" , "H" 중 선택, 다중 선택 가능)
        # - P = 팝빌, H = 홈택스 또는 외부ASP
        # - 미입력시 전체조회
        RegType = ["P", "H"]

        # 공급받는자 휴폐업상태 배열 ("N" , "0" , "1" , "2" , "3" , "4" 중 선택, 다중 선택 가능)
        # - N = 미확인 , 0 = 미등록 , 1 = 사업 , 2 = 폐업 , 3 = 휴업 , 4 = 확인실패
        # - 미입력시 전체조회
        CloseDownState = ["N", "0", "1", "2", "3"]

        # 지연발행 여부 (None , true , false 중 택 1)
        # - None = 전체조회 , true = 지연발행 , false = 정상발행
        LateOnly = ""

        # 종사업장번호 유무 (None , "0" , "1" 중 택 1)
        # - None = 전체 , 0 = 없음, 1 = 있음
        TaxRegIDYN = ""

        # 종사업장번호의 주체 ("S" , "B" , "T" 중 택 1)
        # └ S = 공급자 , B = 공급받는자 , T = 수탁자
        # - 미입력시 전체조회
        TaxRegIDType = "S"

        # 종사업장번호
        # 다수기재시 콤마(",")로 구분하여 구성 ex ) "0001,0002"
        # - 미입력시 전체조회
        TaxRegID = ""

        # 페이지번호, 기본값 '1'
        Page = 1

        # 페이지당 검색개수, 기본값 500, 최대 1000
        PerPage = 5

        # 정렬 방향, D-내림차순, A-오름차순
        Order = "D"

        # 거래처 상호 / 사업자번호 (사업자) / 주민등록번호 (개인) / "9999999999999" (외국인) 중 검색하고자 하는 정보 입력
        # - 사업자번호 / 주민등록번호는 하이픈('-')을 제외한 숫자만 입력
        # - 미입력시 전체조회
        QString = ""

        # 연동문서 여부 (None , "0" , "1" 중 택 1)
        # - None = 전체조회 , 0 = 일반문서 , 1 = 연동문서
        # - 일반문서 : 세금계산서 작성 시 API가 아닌 팝빌 사이트를 통해 등록한 문서
        # - 연동문서 : 세금계산서 작성 시 API를 통해 등록한 문서
        InterOPYN = ""

        # 세금계산서의 문서번호 / 국세청 승인번호 중 검색하고자 하는 정보 입력
        # - 미입력시 전체조회
        MgtKey = ""

        response = taxinvoiceService.search(
            CorpNum,
            MgtKeyType,
            DType,
            SDate,
            EDate,
            State,
            Type,
            TaxType,
            LateOnly,
            TaxRegIDYN,
            TaxRegIDType,
            TaxRegID,
            Page,
            PerPage,
            Order,
            UserID,
            QString,
            InterOPYN,
            IssueType,
            RegType,
            CloseDownState,
            MgtKey,
        )

        return render(request, "Taxinvoice/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getLogs(request):
    """
    세금계산서의 상태에 대한 변경이력을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetLogs
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        LogList = taxinvoiceService.getLogs(CorpNum, MgtKeyType, MgtKey)

        return render(request, "Taxinvoice/GetLogs.html", {"LogList": LogList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getURL(request):
    """
    로그인 상태로 팝빌 사이트의 전자세금계산서 문서함 메뉴에 접근할 수 있는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/info#GetURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # TBOX = 임시 문서함, SWBOX = 매출 발행 대기함, PWBOX = 매입 발행 대기함
        # SBOX = 매출 문서함, PBOX = 매입 문서함, WRITE = 정발행 작성
        TOGO = "SBOX"

        url = taxinvoiceService.getURL(CorpNum, UserID, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPopUpURL(request):
    """
    팝빌 사이트와 동일한 세금계산서 1건의 상세 정보 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetPopUpURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getPopUpURL(
            CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getViewURL(request):
    """
    팝빌 사이트와 동일한 세금계산서 1건의 상세정보 페이지(사이트 상단, 좌측 메뉴 및 버튼 제외)의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetViewURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getViewURL(CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPrintURL(request):
    """
    세금계산서 1건을 인쇄하기 위한 페이지의 팝업 URL을 반환하며, 페이지내에서 인쇄 설정값을 "공급자" / "공급받는자" / "공급자+공급받는자"용 중 하나로 지정할 수 있습니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getPrintURL(
            CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getOldPrintURL(request):
    """
    세금계산서 1건을 구버전 양식으로 인쇄하기 위한 페이지의 팝업 URL을 반환하며, 페이지내에서 인쇄 설정값을 "공급자" / "공급받는자" / "공급자+공급받는자"용 중 하나로 지정할 수 있습니다..
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetOldPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getOldPrintURL(
            CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getEPrintURL(request):
    """
    "공급받는자" 용 세금계산서 1건을 인쇄하기 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetEPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getEPrintURL(
            CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMassPrintURL(request):
    """
    다수건의 세금계산서를 인쇄하기 위한 페이지의 팝업 URL을 반환합니다. (최대 100건)
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetMassPrintURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 인쇄할 문서번호 배열, 최대 100건
        MgtKeyList = []
        MgtKeyList.append("20220805-001")
        MgtKeyList.append("20220805-002")

        url = taxinvoiceService.getMassPrintURL(
            CorpNum, MgtKeyType, MgtKeyList, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getMailURL(request):
    """
    안내메일과 관련된 전자세금계산서를 확인 할 수 있는 상세 페이지의 팝업 URL을 반환하며, 해당 URL은 메일 하단의 "전자세금계산서 보기" 버튼의 링크와 같습니다.
    - 메일링크 URL은 유효시간이 존재하지 않습니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetMailURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getMailURL(CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPDFURL(request):
    """
    전자세금계산서 PDF 파일을 다운 받을 수 있는 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/view#GetPDFURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        url = taxinvoiceService.getPDFURL(CorpNum, MgtKeyType, MgtKey, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌 사이트에 로그인 상태로 접근할 수 있는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSealURL(request):
    """
    세금계산서에 첨부할 인감, 사업자등록증, 통장사본을 등록하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#GetSealURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getSealURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def attachFile(request):
    """
    "임시저장" 상태의 세금계산서에 1개의 파일을 첨부합니다. (최대 5개)
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#AttachFile
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        # 파일경로
        FilePath = "./TaxinvoiceExample/static/image/attachfile.png"

        response = taxinvoiceService.attachFile(
            CorpNum, MgtKeyType, MgtKey, FilePath)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def deleteFile(request):
    """
    "임시저장" 상태의 세금계산서에 첨부된 1개의 파일을 삭제합니다.
    - 파일을 식별하는 파일아이디는 첨부파일 목록(GetFiles API) 의 응답항목 중 파일아이디(AttachedFile) 값을 통해 확인할 수 있습니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#DeleteFile
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        # 첨부파일 아이디, GetFiles API의 응답항목(attachedFile) 확인.
        FileID = "8D13F961-CD77-4856-9501-1FB59CAFEE9E.PBF"

        response = taxinvoiceService.deleteFile(
            CorpNum, MgtKeyType, MgtKey, FileID)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFiles(request):
    """
    세금계산서에 첨부된 파일목록을 확인합니다.
    - 응답항목 중 파일아이디(AttachedFile) 항목은 파일삭제(DeleteFile API) 호출시 이용할 수 있습니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#GetFiles
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-001"

        fileList = taxinvoiceService.getFiles(CorpNum, MgtKeyType, MgtKey)

        return render(request, "Taxinvoice/GetFiles.html", {"fileList": fileList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendEmail(request):
    """
    세금계산서와 관련된 안내 메일을 재전송 합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#SendEmail
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        # 수신메일주소
        ReceiverMail = ""

        response = taxinvoiceService.sendEmail(
            CorpNum, MgtKeyType, MgtKey, ReceiverMail)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendSMS(request):
    """
    세금계산서와 관련된 안내 SMS(단문) 문자를 재전송하는 함수로, 팝빌 사이트 [문자·팩스] > [문자] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 메시지는 최대 90byte까지 입력 가능하고, 초과한 내용은 자동으로 삭제되어 전송합니다. (한글 최대 45자)
    - 함수 호출시 포인트가 과금됩니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#SendSMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        # 발신번호
        Sender = ""

        # 수신번호
        Receiver = ""

        # 메시지 내용, 최대 90byte 초과시 길이가 조정되어 전송됨
        Contents = "발신문자 내용"

        response = taxinvoiceService.sendSMS(
            CorpNum, MgtKeyType, MgtKey, Sender, Receiver, Contents)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAX(request):
    """
    세금계산서를 팩스로 전송하는 함수로, 팝빌 사이트 [문자·팩스] > [팩스] > [전송내역] 메뉴에서 전송결과를 확인 할 수 있습니다.
    - 함수 호출시 포인트가 과금됩니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 문서번호
        MgtKey = "20220805-002"

        # 발신번호
        Sender = ""

        # 수신팩스번호
        Receiver = ""

        response = taxinvoiceService.sendFax(
            CorpNum, MgtKeyType, MgtKey, Sender, Receiver)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def attachStatement(request):
    """
    팝빌 전자명세서 API를 통해 발행한 전자명세서를 세금계산서에 첨부합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#AttachStatement
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 세금계산서 문서번호
        MgtKey = "20220805-001"

        # 전자명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서, 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서번호
        StmtMgtKey = "20220805-001"

        response = taxinvoiceService.attachStatement(
            CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def detachStatement(request):
    """
    세금계산서에 첨부된 전자명세서를 해제합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#DetachStatement
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 유형 , SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 세금계산서 문서번호
        MgtKey = "20220805-001"

        # 전자명세서 종류코드, 121-거래명세서, 122-청구서, 123-견적서, 124-발주서, 125-입금표, 126-영수증
        ItemCode = "121"

        # 전자명세서 문서번호
        StmtMgtKey = "20220805-001"

        response = taxinvoiceService.detachStatement(
            CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getEmailPublicKeys(request):
    """
    전자세금계산서 유통사업자의 메일 목록을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#GetEmailPublicKeys
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        aspList = taxinvoiceService.getEmailPublicKeys(CorpNum)

        return render(request, "Taxinvoice/GetEmailPublicKeys.html", {"aspList": aspList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def assignMgtKey(request):
    """
    팝빌 사이트를 통해 발행하였지만 문서번호가 존재하지 않는 세금계산서에 문서번호를 할당합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#AssignMgtKey
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 세금계산서 발행유형, SELL : 매출 , BUY : 매입 , TRUSTEE : 수탁
        MgtKeyType = "SELL"

        # 세금계산서 아이템키, 문서 목록조회(Search) API의 반환항목중 ItemKey 참조
        ItemKey = "019011609280500001"

        # 할당할 문서번호, 숫자, 영문 '-', '_' 조합으로 1~24자리까지
        # 사업자번호별 중복없는 고유번호 할당
        MgtKey = "20220805-003"

        response = taxinvoiceService.assignMgtKey(
            CorpNum, MgtKeyType, ItemKey, MgtKey)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listEmailConfig(request):
    """
    세금계산서 관련 메일 항목에 대한 발송설정을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#ListEmailConfig
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        EmailConfig = taxinvoiceService.listEmailConfig(CorpNum)

        return render(request, "Taxinvoice/ListEmailConfig.html", {"EmailConfig": EmailConfig})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateEmailConfig(request):
    """
    세금계산서 관련 메일 항목에 대한 발송설정을 수정합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#UpdateEmailConfig

    메일전송유형
    [정발행]
    TAX_ISSUE : 공급받는자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_ISSUE_INVOICER : 공급자에게 전자세금계산서가 발행 되었음을 알려주는 메일입니다.
    TAX_CHECK : 공급자에게 전자세금계산서가 수신확인 되었음을 알려주는 메일입니다.
    TAX_CANCEL_ISSUE : 공급받는자에게 전자세금계산서가 발행취소 되었음을 알려주는 메일입니다.

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

    [처리결과]
    TAX_CLOSEDOWN : 거래처의 휴폐업 여부를 확인하여 안내하는 메일입니다.
    TAX_NTSFAIL_INVOICER : 전자세금계산서 국세청 전송실패를 안내하는 메일입니다.

    [정기발송]
    ETC_CERT_EXPIRATION : 팝빌에서 이용중인 인증서의 갱신을 안내하는 메일입니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 메일 전송 유형
        EmailType = "TAX_ISSUE"

        # 전송 여부 (True = 전송, False = 미전송)
        SendYN = True

        response = taxinvoiceService.updateEmailConfig(
            CorpNum, EmailType, SendYN)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSendToNTSConfig(request):
    """
    연동회원의 국세청 전송 옵션 설정 상태를 확인합니다.
    - 팝빌 국세청 전송 정책 [https://developers.popbill.com/guide/taxinvoice/python/introduction/policy-of-send-to-nts]
    - 국세청 전송 옵션 설정은 팝빌 사이트 [전자세금계산서] > [환경설정] > [세금계산서 관리] 메뉴에서 설정할 수 있으며, API로 설정은 불가능 합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/etc#GetSendToNTSConfig
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        sendToNTSConfig = taxinvoiceService.getSendToNTSConfig(CorpNum)

        return render(request, "Taxinvoice/SendToNTSConfig.html", {"sendToNTS": sendToNTSConfig})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getTaxCertURL(request):
    """
    전자세금계산서 발행에 필요한 인증서를 팝빌 인증서버에 등록하기 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - 인증서 갱신/재발급/비밀번호 변경한 경우, 변경된 인증서를 팝빌 인증서버에 재등록 해야합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/cert#GetTaxCertURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getTaxCertURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCertificateExpireDate(request):
    """
    팝빌 인증서버에 등록된 인증서의 만료일을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/cert#GetCertificateExpireDate
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        expiredate = taxinvoiceService.getCertificateExpireDate(CorpNum)

        return render(request, "Taxinvoice/GetCertificateExpireDate.html", {"expiredate": expiredate})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkCertValidation(request):
    """
    팝빌 인증서버에 등록된 인증서의 유효성을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/cert#CheckCertValidation
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = taxinvoiceService.checkCertValidation(CorpNum)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getTaxCertInfo(request):
    """
    팝빌 인증서버에 등록된 공동인증서의 정보를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/cert#GetTaxCertInfo
    """

    try:
        print("=" * 15 + " 인증서 정보 확인 " + "=" * 15)

        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        taxinvoiceCertificate = taxinvoiceService.getTaxCertInfo(CorpNum)

        return render(request, "Taxinvoice/GetTaxCertInfo.html", {"taxinvoiceCertificate": taxinvoiceCertificate})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = taxinvoiceService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = taxinvoiceService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = taxinvoiceService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = taxinvoiceService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUnitCost(request):
    """
    세금계산서 발행시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        result = taxinvoiceService.getUnitCost(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 전자세금계산서 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        response = taxinvoiceService.getChargeInfo(CorpNum)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#PaymentRequest
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 무통장입금 요청 객체
        paymentForm = PaymentForm(
            # 담당자명
            settlerName="담당자 이름",

            # 담당자 이메일
            settlerEmail="popbill_django_test@email.com",

            # 담당자 휴대폰
            notifyHP="01012341234",

            # 입금자명
            paymentName="입금자",

            # 결제금액
            settleCost="10000",
        )
        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.paymentRequest(
            CorpNum, paymentForm,  UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.getSettleResult(
            CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetPaymentHistory
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

        response = taxinvoiceService.getPaymentHistory(
            CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetUseHistory
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

        response = taxinvoiceService.getUseHistory(
            CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#Refund
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

        response = taxinvoiceService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message, "refundCode": response.refundCode})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetRefundHistory
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

        response = taxinvoiceService.getRefundHistory(
            CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = taxinvoiceService.checkIsMember(CorpNum)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = taxinvoiceService.checkID(memberID)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#JoinMember
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

        response = taxinvoiceService.joinMember(newMember)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = taxinvoiceService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#UpdateCorpInfo
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

        response = taxinvoiceService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#RegistContact
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

        response = taxinvoiceService.registContact(CorpNum, newContact)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = taxinvoiceService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = taxinvoiceService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#UpdateContact
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

        response = taxinvoiceService.updateContact(CorpNum, updateInfo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def quitMember(request):
    """
    가입된 연동회원의 탈퇴를 요청합니다.
    - 회원탈퇴 신청과 동시에 팝빌의 모든 서비스 이용이 불가하며, 관리자를 포함한 모든 담당자 계정도 일괄탈퇴 됩니다.
    - 회원탈퇴로 삭제된 데이터는 복원이 불가능합니다.
    - 관리자 계정만 사용 가능합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/member#QuitMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 탈퇴 사유
        QuitReason = "테스트 탈퇴 사유"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.quitMember(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundInfo(request):
    """
    포인트 환불에 대한 상세정보 1건을 확인합니다.
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetRefundInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 환불코드
        RefundCode = "023040000017"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = taxinvoiceService.getRefundInfo(
            CorpNum, RefundCode, UserID)
        return render(request, 'getRefundInfo.html', {"code": response.code, "response": response})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundableBalance(request):
    """
    환불 가능한 포인트를 확인합니다. (보너스 포인트는 환불가능포인트에서 제외됩니다.)
    - https://developers.popbill.com/reference/taxinvoice/python/api/point#GetRefundableBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        refundableBalance = taxinvoiceService.getRefundableBalance(CorpNum, UserID)
        return render(request, 'getRefundableBalance.html', {"refundableBalance": refundableBalance})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})
