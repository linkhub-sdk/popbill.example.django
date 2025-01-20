# -*- coding: utf-8 -*-
"""
팝빌 팩스 API Python SDK Django Example

Django 연동 튜토리얼 안내 : https://developers.popbill.com/guide/fax/python/getting-started/tutorial
연동 기술지원 연락처 : 1600-9854
연동 기술지원 이메일 : code@linkhubcorp.com

<테스트 연동개발 준비사항>
1) 발신번호 사전등록을 합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
    - 1. 팝빌 사이트 로그인 > [문자/팩스] > [팩스] > [발신번호 사전등록] 메뉴에서 등록
    - 2. getSenderNumberMgtURL API를 통해 반환된 URL을 이용하여 발신번호 등록
"""
from django.shortcuts import render
from popbill import (
    ContactInfo,
    CorpInfo,
    FaxReceiver,
    FaxService,
    FileData,
    JoinForm,
    PaymentForm,
    PopbillException,
    RefundForm,
)

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 FaxService 객체 생성
faxService = FaxService(settings.LinkID, settings.SecretKey)

# 연동환경 설정, true-테스트, false-운영(Production), (기본값:true)
faxService.IsTest = settings.IsTest

# 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
faxService.IPRestrictOnOff = settings.IPRestrictOnOff

# 통신 IP 고정, true-사용, false-미사용, (기본값:false)
faxService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, true-사용, false-미사용, (기본값:true)
faxService.UseLocalTimeYN = settings.UseLocalTimeYN


def index(request):
    return render(request, "Fax/Index.html", {})


def checkSenderNumber(request):
    """
    팩스 발신번호 등록여부를 확인합니다.
    - 발신번호 상태가 '승인'인 경우에만 리턴값 'Response'의 변수 'code'가 1로 반환됩니다.
    - https://developers.popbill.com/reference/fax/python/api/sendnum#CheckSenderNumber
    """

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인할 발신번호
        senderNumber = ""

        response = faxService.checkSenderNumber(CorpNum, senderNumber)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSenderNumberMgtURL(request):
    """
    발신번호를 등록하고 내역을 확인하는 팩스 발신번호 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/sendnum#GetSenderNumberMgtURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getSenderNumberMgtURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSenderNumberList(request):
    """
    팝빌에 등록한 연동회원의 팩스 발신번호 목록을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/sendnum#GetSenderNumberList
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        senderList = faxService.getSenderNumberList(CorpNum)

        return render(
            request, "Fax/GetSenderNumberList.html", {"senderList": senderList}
        )
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAX(request):
    """
    팩스 1건을 팝빌에 접수합니다. (최대 전송파일 개수: 20개)
    - https://developers.popbill.com/reference/fax/python/api/send#SendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 발신번호
        # 팝빌에 등록되지 않은 번호를 입력하는 경우 '원발신번호'로 팩스 전송됨
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        Receiver = ""

        # 수신자명
        ReceiverName = "수신자명"

        # 파일경로 (해당파일에 읽기 권한이 설정되어 있어야 함. 최대 20개)
        FilePath = [
            "./FaxExample/static/file/faxfile.jpg",
            "./FaxExample/static/file/test.pdf",
        ]

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리 , true / false 중 택 1
        AdsYN = False

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax(CorpNum, Sender, Receiver, ReceiverName,
                                        FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAX_multi(request):
    """
    동일한 팩스파일을 다수의 수신자에게 전송하기 위해 팝빌에 접수합니다. (최대 전송파일 개수 : 20개) (최대 1,000건)
    - https://developers.popbill.com/reference/fax/python/api/send#SendFAX_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 발신번호
        # 팝빌에 등록되지 않은 번호를 입력하는 경우 '원발신번호'로 팩스 전송됨
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 파일경로 (해당파일에 읽기 권한이 설정되어 있어야 함. 최대 20개)
        FilePath = [
            "./FaxExample/static/file/faxfile.jpg",
            "./FaxExample/static/file/test.pdf",
        ]

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리
        AdsYN = False

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = "Python 팩스동보전송 제목"

        Receivers = []  # 수신정보 리스트, 최대 1000개
        for x in range(0, 5):
            Receivers.append(
                FaxReceiver(
                    receiveNum="",  # 수신번호
                    receiveName="수신자명" + str(x),  # 수신자명
                    interOPRefKey="20220805-" + str(x),  # 파트너 지정키
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax_multi(
            CorpNum, Sender, Receivers, FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAXBinary(request):
    """
    전송할 파일의 바이너리 데이터로 팩스 1건을 팝빌에 접수합니다. (최대 전송파일 개수: 20개)
    - https://developers.popbill.com/reference/fax/python/api/send#SendFAXBinary
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 발신번호
        # 팝빌에 등록되지 않은 번호를 입력하는 경우 '원발신번호'로 팩스 전송됨
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        Receiver = ""

        # 수신자명
        ReceiverName = "수신자명"

        # 전송 파일 객체정보 리스트, 최대 20개
        FileDatas = []
        with open("./FaxExample/static/file/test.pdf", "rb") as f:
            FileDatas.append(
                FileData(
                    fileName="test.pdf", fileData=f.read()  # 전송 파일명  # 전송 파일 바이너리 데이터
                )
            )

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리
        AdsYN = True

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary(
            CorpNum, Sender, Receiver, ReceiverName, FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def sendFAXBinary_multi(request):
    """
    전송할 파일의 바이너리 데이터로 다수의 수신자에게 팩스를 전송하기 위해 팝빌에 접수합니다. (최대 전송파일 개수 : 20개) (최대 1,000건)
    - https://developers.popbill.com/reference/fax/python/api/send#SendFAXBinary_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 발신번호
        # 팝빌에 등록되지 않은 번호를 입력하는 경우 '원발신번호'로 팩스 전송됨
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리
        AdsYN = False

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 팩스제목
        Title = "Python 팩스동보전송 제목"

        Receivers = []  # 수신정보 리스트, 최대 1000개
        for x in range(0, 5):
            Receivers.append(
                FaxReceiver(
                    receiveNum="",  # 수신번호
                    receiveName="수신자명" + str(x),  # 수신자명
                    interOPRefKey="20220805-" + str(x),  # 파트너 지정키
                )
            )

        # 전송 파일 객체정보 리스트, 최대 20개
        FileDatas = []
        with open("./FaxExample/static/file/test.pdf", "rb") as f:
            FileDatas.append(
                FileData(
                    fileName="test.pdf", fileData=f.read()  # 전송 파일명  # 전송 파일 바이너리 데이터
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary_multi(
            CorpNum, Sender, Receivers, FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def resendFAX(request):
    """
    팝빌에서 반환받은 접수번호를 통해 팩스 1건을 재전송합니다.
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/send#ResendFAX
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 요청시 발급받은 접수번호
        ReceiptNum = "022080515503200001"

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

        # 재전송 팩스의 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax(
            CorpNum, ReceiptNum, Sender, SenderName, Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def resendFAXRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 팩스 1건을 재전송합니다.
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/send#ResendFAXRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = ""

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

        # 재전송 팩스의 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN(
            CorpNum, OrgRequestNum, Sender, SenderName, Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def resendFAX_multi(request):
    """
    팝빌에서 반환받은 접수번호를 통해 다수의 수신자에게 팩스를 재전송합니다. (최대 1000건)
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/send#ResendFAX_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스전송 요청시 발급받은 접수번호
        ReceiptNum = "022080515503200001"

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
                    receiveNum = "", # 수신번호
                    receiveName = "수신자명"+str(x), # 수신자명
                    interOPRefKey = '20220805-'+str(x) # 파트너 지정키
                )
            )
        """
        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax_multi(
            CorpNum, ReceiptNum, Sender, SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def resendFAXRN_multi(request):
    """
    파트너가 할당한 전송요청번호를 통해 다수의 수신자에게 팩스를 재전송합니다. (최대 1,000건)
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
        - https://developers.popbill.com/reference/fax/python/api/send#ResendFAXRN_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = ""

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
                    receiveNum = '', # 수신번호
                    receiveName = '수신자명'+str(x), # 수신자명
                    interOPRefKey = '20220805-'+str(x) # 파트너 지정키
                )
            )
        """

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 할당하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN_multi(
            CorpNum, OrgRequestNum, Sender, SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, "Fax/ReceiptNum.html", {"receiptNum": receiptNum})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def cancelReserve(request):
    """
    팝빌에서 반환받은 접수번호를 통해 예약접수된 팩스 전송을 취소합니다. (예약시간 10분 전까지 가능)
    - https://developers.popbill.com/reference/fax/python/api/send#CancelReserve
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스 예약전송 요청시 반환받은 접수번호
        receiptNum = "022080515534100001"

        response = faxService.cancelReserve(CorpNum, receiptNum)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def cancelReserveRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 예약접수된 팩스 전송을 취소합니다. (예약시간 10분 전까지 가능)
    - https://developers.popbill.com/reference/fax/python/api/send#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약팩스전송 요청시 할당한 전송요청번호
        requestNum = ""

        response = faxService.cancelReserveRN(CorpNum, requestNum)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFaxResult(request):
    """
    팝빌에서 반환 받은 접수번호를 통해 팩스 전송상태 및 결과를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/info#GetFaxResult
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송 요청시 반환받은 접수번호 (receiptNum)
        receiptNum = "022080515534100001"

        resultList = faxService.getFaxResult(CorpNum, receiptNum)

        return render(request, "Fax/GetFaxResult.html", {"resultList": resultList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getFaxResultRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 팩스 전송상태 및 결과를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/info#GetFaxResultRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송요청시 할당한 전송요청번호 (requestNum)
        requestNum = ""

        resultList = faxService.getFaxResultRN(CorpNum, requestNum)

        return render(request, "Fax/GetFaxResult.html", {"resultList": resultList})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def search(request):
    """
    검색조건에 해당하는 팩스 전송내역 목록을 조회합니다. (조회기간 단위 : 최대 2개월)
    - 팩스 접수일시로부터 2개월 이내 접수건만 조회할 수 있습니다.
    - https://developers.popbill.com/reference/fax/python/api/info#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 최대 검색기간 : 6개월 이내
        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20241201"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20241231"

        # 전송상태 배열 ("1" , "2" , "3" , "4" 중 선택, 다중 선택 가능)
        # └ 1 = 대기 , 2 = 성공 , 3 = 실패 , 4 = 취소
        # - 미입력 시 전체조회
        State = ["1", "2", "3", "4"]

        # 예약여부 (None, False , True 중 택 1)
        # └ None = 전체조회, False = 즉시전송건 조회, True = 예약전송건 조회
        # - 미입력 시 전체조회
        ReserveYN = False

        # 개인조회 여부 (False , True 중 택 1)
        # False = 접수한 팩스 전체 조회 (관리자권한)
        # True = 해당 담당자 계정으로 접수한 팩스만 조회 (개인권한)
        # 미입력시 기본값 False 처리
        SenderOnly = False

        # 페이지 번호
        Page = 1

        # 페이지당 목록갯수, 기본값 500
        PerPage = 10

        # 정렬방향, D-내림차순, A-오름차순
        Order = "D"

        # 조회하고자 하는 발신자명 또는 수신자명
        # 미입력시 전체조회
        QString = ""

        response = faxService.search(
            CorpNum, SDate, EDate, State, ReserveYN, SenderOnly, Page, PerPage, Order, UserID, QString)

        return render(request, "Fax/Search.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSentListURL(request):
    """
    팩스 전송내역 확인 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/info#GetSentListURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getSentListURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPreviewURL(request):
    """
    팩스 미리보기 팝업 URL을 반환하며, 팩스전송을 위한 TIF 포맷 변환 완료 후 호출 할 수 있습니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/info#GetPreviewURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스 접수번호
        ReceiptNum = "018012215343900001"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getPreviewURL(CorpNum, ReceiptNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetChargeURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getChargeURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getPaymentURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getUseHistoryURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetPartnerBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getPartnerBalance(CorpNum)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetPartnerURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = faxService.getPartnerURL(CorpNum, TOGO)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUnitCost(request):
    """
    팩스 전송시 과금되는 포인트 단가를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 수신번호 유형 : "일반" / "지능" 중 택 1
        # └ 일반망 : 지능망을 제외한 번호
        # └ 지능망 : 030*, 050*, 070*, 080*, 대표번호
        receiveNumType = "지능"

        result = faxService.getUnitCost(CorpNum, receiveNumType)

        return render(request, "result.html", {"result": result})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getChargeInfo(request):
    """
    팝빌 팩스 API 서비스 과금정보를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 수신번호 유형 : "일반" / "지능" 중 택 1
        # └ 일반망 : 지능망을 제외한 번호
        # └ 지능망 : 030*, 050*, 070*, 080*, 대표번호
        receiveNumType = "지능"

        response = faxService.getChargeInfo(CorpNum, UserID, receiveNumType)

        return render(request, "getChargeInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def paymentRequest(request):
    """
    연동회원 포인트 충전을 위해 무통장입금을 신청합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#PaymentRequest
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

        response = faxService.paymentRequest(CorpNum, paymentForm, UserID)

        return render(request, "paymentResponse.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getSettleResult(request):
    """
    연동회원 포인트 무통장 입금신청내역 1건을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetSettleResult
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 정산코드
        SettleCode = "202303070000000052"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.getSettleResult(CorpNum, SettleCode, UserID)

        return render(request, "paymentHistory.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getPaymentHistory(request):
    """
    연동회원의 포인트 결제내역을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetPaymentHistory
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

        response = faxService.getPaymentHistory(
            CorpNum, SDate, EDate, Page, PerPage, UserID)

        return render(request, "paymentHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getUseHistory(request):
    """
    연동회원의 포인트 사용내역을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetUseHistory
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

        response = faxService.getUseHistory(
            CorpNum, SDate, EDate, Page, PerPage, Order, UserID)

        return render(request, "useHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def refund(request):
    """
    연동회원 포인트를 환불 신청합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#Refund
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

        response = faxService.refund(CorpNum, refundForm, UserID)

        return render(request,"response.html",{"code": response.code, "message": response.message, "refundCode": response.refundCode})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundHistory(request):
    """
    연동회원의 포인트 환불신청내역을 확인합니다.
    - - https://developers.popbill.com/reference/fax/python/api/point#GetRefundHistory
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

        response = faxService.getRefundHistory(CorpNum, Page, PerPage, UserID)

        return render(request, "refundHistoryResult.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#CheckIsMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = faxService.checkIsMember(CorpNum)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def checkID(request):
    """
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#CheckID
    """
    try:
        # 중복확인할 아이디
        memberID = "testkorea"

        response = faxService.checkID(memberID)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def joinMember(request):
    """
    사용자를 연동회원으로 가입처리합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#JoinMember
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

        response = faxService.joinMember(newMember)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#GetAccessURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = faxService.getAccessURL(CorpNum, UserID)

        return render(request, "url.html", {"url": url})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = faxService.getCorpInfo(CorpNum)

        return render(request, "getCorpInfo.html", {"response": response})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#UpdateCorpInfo
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

        response = faxService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#RegistContact
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

        response = faxService.registContact(CorpNum, newContact)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = "testkorea"

        contactInfo = faxService.getContactInfo(CorpNum, contactID)

        return render(request, "getContactInfo.html", {"contactInfo": contactInfo})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = faxService.listContact(CorpNum)

        return render(request, "listContact.html", {"listContact": listContact})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#UpdateContact
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

        response = faxService.updateContact(CorpNum, updateInfo)

        return render(request, "response.html", {"code": response.code, "message": response.message})

    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def quitMember(request):
    """
    가입된 연동회원의 탈퇴를 요청합니다.
    - 회원탈퇴 신청과 동시에 팝빌의 모든 서비스 이용이 불가하며, 관리자를 포함한 모든 담당자 계정도 일괄탈퇴 됩니다.
    - 회원탈퇴로 삭제된 데이터는 복원이 불가능합니다.
    - 관리자 계정만 사용 가능합니다.
    - https://developers.popbill.com/reference/fax/python/api/member#QuitMember
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 탈퇴 사유
        QuitReason = "테스트 탈퇴 사유"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.quitMember(CorpNum, QuitReason, UserID)
        return render(request, 'response.html', {"code": response.code, "message": response.message})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundInfo(request):
    """
    포인트 환불에 대한 상세정보 1건을 확인합니다.
    - https://developers.popbill.com/reference/fax/python/api/point#GetRefundInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 환불코드
        RefundCode = "023040000017"

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.getRefundInfo(CorpNum, RefundCode, UserID)
        return render(request, 'getRefundInfo.html', {"code": response.code, "response": response})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})


def getRefundableBalance(request):
    """
    환불 가능한 포인트를 확인합니다. (보너스 포인트는 환불가능포인트에서 제외됩니다.)
    - https://developers.popbill.com/reference/fax/python/api/point#GetRefundableBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        refundableBalance = faxService.getRefundableBalance(CorpNum, UserID)
        return render(request, 'getRefundableBalance.html', {"refundableBalance": refundableBalance})
    except PopbillException as PE:
        return render(request, "exception.html", {"code": PE.code, "message": PE.message})
