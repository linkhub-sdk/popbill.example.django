# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import FaxService, PopbillException, ContactInfo, JoinForm, FaxReceiver, FileData, CorpInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 FaxService 객체 생성
faxService = FaxService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
faxService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
faxService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
faxService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
faxService.UseLocalTimeYN = settings.UseLocalTimeYN

def index(request):
    return render(request, 'Fax/Index.html', {})


def getSenderNumberMgtURL(request):
    """
    발신번호 관리 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetSenderNumberMgtURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getSenderNumberMgtURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSenderNumberList(request):
    """
    팝빌에 등록된 팩스 발신번호 목록을 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetSenderNumberList
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        senderList = faxService.getSenderNumberList(CorpNum)

        return render(request, 'Fax/GetSenderNumberList.html', {'senderList': senderList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFAX(request):
    """
    팩스를 전송합니다. (전송할 파일 개수는 최대 20개까지 가능)
    - https://docs.popbill.com/fax/python/api#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = "070111222"

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        Receiver = "070222111"

        # 수신자명
        ReceiverName = "수신자명"

        # 파일경로 (해당파일에 읽기 권한이 설정되어 있어야 함. 최대 20개)
        FilePath = ["./FaxExample/static/file/faxfile.jpg", "./FaxExample/static/file/test.pdf"]

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 광고팩스 전송여부
        AdsYN = False

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax(CorpNum, Sender, Receiver, ReceiverName,
                                        FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFAX_multi(request):
    """
    [대량전송] 팩스를 전송합니다. (전송할 파일 개수는 최대 20개까지 가능)
    - https://docs.popbill.com/fax/python/api#SendFAX_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = "07043042991"

        # 발신자명
        SenderName = "발신자명"

        # 파일경로 (해당파일에 읽기 권한이 설정되어 있어야 함. 최대 20개)
        FilePath = ["./FaxExample/static/file/faxfile.jpg", "./FaxExample/static/file/test.pdf"]

        # 광고팩스 전송여부
        AdsYN = False

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = "Python 팩스동보전송 제목"

        Receivers = []  # 수신정보 리스트, 최대 1000개
        for x in range(0, 5):
            Receivers.append(
                FaxReceiver(
                    receiveNum="070111222",  # 수신번호
                    receiveName="수신자명" + str(x),  # 수신자명
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax_multi(CorpNum, Sender, Receivers,
                                              FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFAXBinary(request):
    """
    전송할 파일의 바이너리 데이터로 팩스를 전송합니다. (전송할 파일 개수는 최대 20개까지 가능)
    - https://docs.popbill.com/fax/python/api#SendFAXBinary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = "070111222"

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        Receiver = "070222111"

        # 수신자명
        ReceiverName = "수신자명"

        #전송 파일 객체정보 리스트, 최대 20개
        FileDatas = []
        with open("./test.pdf", "rb") as f:
            FileDatas.append(
                FileData(
                    fileName='test.pdf', #전송 파일명
                    fileData=f.read()    #전송 파일 바이너리 데이터
                )
            )

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = "20210428140000"

        # 광고팩스 전송여부
        AdsYN = True

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary(CorpNum, Sender, Receiver, ReceiverName,
                                        FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFAXBinary_multi(request):
    """
    [대량전송] 전송할 파일의 바이너리 데이터로 팩스를 전송합니다. (전송할 파일 개수는 최대 20개까지 가능)
    - https://docs.popbill.com/fax/python/api#SendFAXBinary_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = "07043042991"

        # 발신자명
        SenderName = "발신자명"

        # 광고팩스 전송여부
        AdsYN = False

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = "Python 팩스동보전송 제목"

        Receivers = []  # 수신정보 리스트, 최대 1000개
        for x in range(0, 5):
            Receivers.append(
                FaxReceiver(
                    receiveNum="070111222",  # 수신번호
                    receiveName="수신자명" + str(x),  # 수신자명
                )
            )

        #전송 파일 객체정보 리스트, 최대 20개
        FileDatas = []
        with open("./test.pdf", "rb") as f:
            FileDatas.append(
                FileData(
                    fileName='test.pdf', #전송 파일명
                    fileData=f.read()    #전송 파일 바이너리 데이터
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary_multi(CorpNum, Sender, Receivers,
                                              FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def resendFAX(request):
    """
    팩스를 재전송합니다.
    - 접수일로부터 60일이 경과되지 않은 팩스전송건만 재전송할 수 있습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://docs.popbill.com/fax/python/api#ResendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 요청시 발급받은 접수번호
        ReceiptNum = "018120517165400001"

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ""

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = "발신자명"

        # 수신번호/수신자명 모두 공백처리시 기존전송정보로 재전송
        # 수신번호
        Receiver = ""

        # 수신자명
        ReceiverName = ""

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = "팩스 재전송 제목"

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax(CorpNum, ReceiptNum, Sender, SenderName,
                                          Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def resendFAXRN(request):
    """
    전송요청번호(requestNum)을 할당한 팩스를 재전송합니다.
    - 접수일로부터 60일이 경과된 경우 재전송할 수 없습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://docs.popbill.com/fax/python/api#ResendFAXRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = '20211227-001'

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = '07043042991'

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = '발신자명'

        # 수신번호/수신자명 모두 공백처리시 기존전송정보로 재전송
        # 수신번호
        Receiver = ""

        # 수신자명
        ReceiverName = ""

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = '팩스 재전송 제목'

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN(CorpNum, OrgRequestNum, Sender, SenderName,
                                            Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def resendFAX_multi(request):
    """
    [대량전송] 팩스를 재전송합니다.
    - 접수일로부터 60일이 경과되지 않은 팩스전송건만 재전송할 수 있습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://docs.popbill.com/fax/python/api#ResendFAX_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 요청시 발급받은 접수번호
        ReceiptNum = "018012215401700001"

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ""

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = "발신자명"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 수신정보 배열, None처리시 기존전송정보로 전송
        Receivers = None

        # 팩스제목
        Title = "Python 팩스동보 재전송"

        # 수신자 정보가 기존전송정보와 다를경우 아래의 코드 참조
        """
        Receivers = [] # 수신정보 배열, 최대 1000개
        for x in range(0, 10):
            Receivers.append(
            	FaxReceiver(
                    receiveNum = "010111222", # 수신번호
                	receiveName = "수신자명"+str(x), # 수신자명
                )
            )
        """
        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax_multi(CorpNum, ReceiptNum, Sender,
                                                SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def resendFAXRN_multi(request):
    """
    [대량전] 전송요청번호(requestNum)을 할당한 팩스를 재전송합니다.
    - 접수일로부터 60일이 경과된 경우 재전송할 수 없습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - https://docs.popbill.com/fax/python/api#ResendFAXRN_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = '20211227-001'

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = '07043042991'

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = '발신자명'

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 수신정보 배열, None처리시 기존전송정보로 전송
        Receivers = None

        # 팩스제목
        Title = 'Python 팩스동보 재전송'

        # 수신자 정보가 기존전송정보와 다를경우 아래의 코드 참조
        """
        Receivers = [] # 수신정보 배열, 최대 1000개
        for x in range(0, 10):
            Receivers.append(
            	FaxReceiver(
                    receiveNum = '010111222', # 수신번호
                	receiveName = '수신자명'+str(x), # 수신자명
                )
            )
        """

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN_multi(CorpNum, OrgRequestNum, Sender,
                                                  SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserve(request):
    """
    팩스전송요청시 발급받은 접수번호(receiptNum)로 팩스 예약전송건을 취소합니다.
    - 예약전송 취소는 예약전송시간 10분전까지 가능하며, 팩스변환 이후 가능합니다.
    - https://docs.popbill.com/fax/python/api#CancelReserve
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스 예약전송 요청시 반환받은 접수번호
        receiptNum = "018020617315000001"

        response = faxService.cancelReserve(CorpNum, receiptNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserveRN(request):
    """
    팩스전송요청시 할당한 전송요청번호(requestNum)로 팩스 예약전송건을 취소합니다.
    - 예약전송 취소는 예약전송시간 10분전까지 가능하며, 팩스변환 이후 가능합니다.
    - https://docs.popbill.com/fax/python/api#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약팩스전송 요청시 할당한 전송요청번호
        requestNum = "20211201-004"

        response = faxService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFaxDetail(request):
    """
    팩스전송요청시 발급받은 접수번호(receiptNum)로 전송결과를 확인합니다
    - https://docs.popbill.com/fax/python/api#GetFaxResult
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송 요청시 반환받은 접수번호 (receiptNum)
        receiptNum = "019012311143200001"

        resultList = faxService.getFaxResult(CorpNum, receiptNum)

        return render(request, 'Fax/GetFaxDetail.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFaxDetailRN(request):
    """
    팩스전송요청시 할당한 전송요청번호(requestNum)으로 전송결과를 확인합니다
    - https://docs.popbill.com/fax/python/api#GetFaxResultRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송요청시 할당한 전송요청번호 (requestNum)
        requestNum = "20211201-001"

        resultList = faxService.getFaxResultRN(CorpNum, requestNum)

        return render(request, 'Fax/GetFaxDetail.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 팩스전송 내역을 조회합니다. (조회기간 단위 : 최대 2개월)
    - 팩스 접수일시로부터 2개월 이내 접수건만 조회할 수 있습니다.
    - https://docs.popbill.com/fax/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20211201"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20211230"

        # 팩스전송상태 배열, [1-대기 / 2-성공 / 3-실패 / 4-취소]
        State = ["1", "2", "3", "4"]

        # 예약전송 검색여부, [True-예약전송건 조회 / False-전체조회]
        ReserveYN = False

        # 개인조회 여부, [True-개인조회 / False-회사조회]
        SenderOnly = False

        # 페이지 번호
        Page = 1

        # 페이지당 검색개수, 기본값 500, 최대값 1000
        PerPage = 10

        # 정렬방향, [D-내림차순 / A-오름차순]
        Order = "D"

        # 조회 검색어, 발신자명 또는 수신자명 기재
        QString = ""

        response = faxService.search(CorpNum, SDate, EDate, State, ReserveYN, SenderOnly,
                                     Page, PerPage, Order, UserID, QString)

        return render(request, 'Fax/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSentListURL(request):
    """
    팩스 전송내역 목록 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetSentListURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getSentListURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPreviewURL(request):
    """
    접수한 팩스 전송건에 대한 미리보기 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetPreviewURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스 접수번호
        ReceiptNum = "018012215343900001"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getPreviewURL(CorpNum, ReceiptNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeURL(request):
    """
    팝빌 연동회원 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 팩스 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    팩스 전송단가를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        result = faxService.getUnitCost(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    - https://docs.popbill.com/fax/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPaymentURL(request):
    """
    팝빌 연동회원 포인트 결재내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getPaymentURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUseHistoryURL(request):
    """
    팝빌 연동회원 포인트 사용내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getUseHistoryURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를 이용하시기 바랍니다.
    - https://docs.popbill.com/fax/python/api#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = faxService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    - https://docs.popbill.com/fax/python/api#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = faxService.checkIsMember(CorpNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkID(request):
    """
    팝빌 회원아이디 중복여부를 확인합니다.
    - https://docs.popbill.com/fax/python/api#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = faxService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    파트너의 연동회원으로 회원가입을 요청합니다.
    - 아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    - https://docs.popbill.com/fax/python/api#JoinMember
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
            ContactEmail="test@test.com",

            # 담당자 연락처 (최대 20자)
            ContactTEL="070-111-222",

            # 담당자 휴대폰번호 (최대 20자)
            ContactHP="010-111-222",

            # 담당자 팩스번호 (최대 20자)
            ContactFAX="070-111-222"
        )

        response = faxService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/fax/python/api#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def registContact(request):
    """
    연동회원의 담당자를 신규로 등록합니다.
    - https://docs.popbill.com/fax/python/api#RegistContact
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
            tel="010-111-222",

            # 담당자 휴대폰번호 (최대 20자)
            hp="010-111-222",

            # 담당자 팩스번호 (최대 20자)
            fax="070-111-222",

            # 담당자 이메일 (최대 100자)
            email="test@test.com",

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = faxService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원의 담당자 정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = faxService.getContactInfo(CorpNum, contactID, UserID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원의 담당자 목록을 확인합니다.
    - https://docs.popbill.com/fax/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        listContact = faxService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://docs.popbill.com/fax/python/api#UpdateCorpInfo
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

        response = faxService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/fax/python/api#UpdateContact
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

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = faxService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
