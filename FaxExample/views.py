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

def checkSenderNumber(request):
    '''
    팩스 발신번호 등록여부를 확인합니다.
    - 발신번호 상태가 '승인'인 경우에만 리턴값 'Response'의 변수 'code'가 1로 반환됩니다.
    - https://docs.popbill.com/fax/python/api#CheckSenderNumber
    '''

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인할 발신번호
        senderNumber = ""

        result = faxService.checkSenderNumber(CorpNum, senderNumber)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getSenderNumberMgtURL(request):
    """
    발신번호를 등록하고 내역을 확인하는 팩스 발신번호 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    팝빌에 등록한 연동회원의 팩스 발신번호 목록을 확인합니다.
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
    팩스 1건을 팝빌에 접수합니다. (최대 전송파일 개수: 20개)
    - https://docs.popbill.com/fax/python/api#SendFAX
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
        FilePath = ["./FaxExample/static/file/faxfile.jpg", "./FaxExample/static/file/test.pdf"]

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        ReserveDT = ""

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리 , true / false 중 택 1
        AdsYN = False

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax(CorpNum, Sender, Receiver, ReceiverName,
                                        FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFAX_multi(request):
    """
    동일한 팩스파일을 다수의 수신자에게 전송하기 위해 팝빌에 접수합니다. (최대 전송파일 개수 : 20개) (최대 1,000건)
    - https://docs.popbill.com/fax/python/api#SendFAX_Multi
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
        FilePath = ["./FaxExample/static/file/faxfile.jpg", "./FaxExample/static/file/test.pdf"]

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
                    interOPRefKey = '20220803-'+str(x) # 파트너 지정키
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFax_multi(CorpNum, Sender, Receivers,
                                                FilePath, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFAXBinary(request):
    """
    전송할 파일의 바이너리 데이터로 팩스 1건을 팝빌에 접수합니다. (최대 전송파일 개수: 20개)
    - https://docs.popbill.com/fax/python/api#SendFAXBinary
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
        ReserveDT = ""

        # 광고팩스 전송여부 , true / false 중 택 1
        # └ true = 광고 , false = 일반
        # └ 미입력 시 기본값 false 처리
        AdsYN = True

        # 팩스제목
        Title = "Python 팩스단건 제목"

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary(CorpNum, Sender, Receiver, ReceiverName,
                                        FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFAXBinary_multi(request):
    """
    전송할 파일의 바이너리 데이터로 다수의 수신자에게 팩스를 전송하기 위해 팝빌에 접수합니다. (최대 전송파일 개수 : 20개) (최대 1,000건)
    - https://docs.popbill.com/fax/python/api#SendFAXBinary_Multi
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
                    interOPRefKey = '20220803-'+str(x) # 파트너 지정키
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
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.sendFaxBinary_multi(CorpNum, Sender, Receivers,
                                                FileDatas, ReserveDT, UserID, SenderName, AdsYN, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def resendFAX(request):
    """
    팝빌에서 반환받은 접수번호를 통해 팩스 1건을 재전송합니다.
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
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

        # 재전송 팩스의 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax(CorpNum, ReceiptNum, Sender, SenderName,
                                            Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def resendFAXRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 팩스 1건을 재전송합니다.
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
    - https://docs.popbill.com/fax/python/api#ResendFAXRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = ''

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ''

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

        # 재전송 팩스의 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN(CorpNum, OrgRequestNum, Sender, SenderName,
                                            Receiver, ReceiverName, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def resendFAX_multi(request):
    """
    팝빌에서 반환받은 접수번호를 통해 다수의 수신자에게 팩스를 재전송합니다. (최대 1000건)
    - 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
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
                    receiveNum = "", # 수신번호
                    receiveName = "수신자명"+str(x), # 수신자명
                    interOPRefKey = '20220803-'+str(x) # 파트너 지정키
                )
            )
        """
        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFax_multi(CorpNum, ReceiptNum, Sender,
                                                SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def resendFAXRN_multi(request):
    """
파트너가 할당한 전송요청번호를 통해 다수의 수신자에게 팩스를 재전송합니다. (최대 1,000건)
- 발신/수신 정보 미입력시 기존과 동일한 정보로 팩스가 전송되고, 접수일 기준 최대 60일이 경과되지 않는 건만 재전송이 가능합니다.
- 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
- 변환실패 사유로 전송실패한 팩스 접수건은 재전송이 불가합니다.
    - https://docs.popbill.com/fax/python/api#ResendFAXRN_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = ''

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ''

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
                    receiveNum = '', # 수신번호
                    receiveName = '수신자명'+str(x), # 수신자명
                    interOPRefKey = '20220803-'+str(x) # 파트너 지정키
                )
            )
        """

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = faxService.resendFaxRN_multi(CorpNum, OrgRequestNum, Sender,
                                                    SenderName, Receivers, ReserveDT, UserID, Title, RequestNum)

        return render(request, 'Fax/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def cancelReserve(request):
    """
    팝빌에서 반환받은 접수번호를 통해 예약접수된 팩스 전송을 취소합니다. (예약시간 10분 전까지 가능)
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
    파트너가 할당한 전송요청 번호를 통해 예약접수된 팩스 전송을 취소합니다. (예약시간 10분 전까지 가능)
    - https://docs.popbill.com/fax/python/api#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약팩스전송 요청시 할당한 전송요청번호
        requestNum = ""

        response = faxService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getFaxResult(request):
    """
    팝빌에서 반환 받은 접수번호를 통해 팩스 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetFaxResult
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송 요청시 반환받은 접수번호 (receiptNum)
        receiptNum = "019012311143200001"

        resultList = faxService.getFaxResult(CorpNum, receiptNum)

        return render(request, 'Fax/GetFaxResult.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getFaxResultRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 팩스 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetFaxResultRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송요청시 할당한 전송요청번호 (requestNum)
        requestNum = ""

        resultList = faxService.getFaxResultRN(CorpNum, requestNum)

        return render(request, 'Fax/GetFaxResult.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def search(request):
    """
    검색조건에 해당하는 팩스 전송내역 목록을 조회합니다. (조회기간 단위 : 최대 2개월)
    - 팩스 접수일시로부터 2개월 이내 접수건만 조회할 수 있습니다.
    - https://docs.popbill.com/fax/python/api#Search
    """
    try:
        CorpNum = testValue.testCorpNum

        # 최대 검색기간 : 6개월 이내
        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        # 전송상태 배열 ("1" , "2" , "3" , "4" 중 선택, 다중 선택 가능)
        # └ 1 = 대기 , 2 = 성공 , 3 = 실패 , 4 = 취소
        # - 미입력 시 전체조회
        State = ["1", "2", "3", "4"]

        # 예약여부 (false , true 중 택 1)
        # false = 전체조회, true = 예약전송건 조회
        # 미입력시 기본값 false 처리
        ReserveYN = False

        # 개인조회 여부 (false , true 중 택 1)
        # false = 접수한 팩스 전체 조회 (관리자권한)
        # true = 해당 담당자 계정으로 접수한 팩스만 조회 (개인권한)
        # 미입력시 기본값 false 처리
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

        response = faxService.search(CorpNum, SDate, EDate, State, ReserveYN, SenderOnly,
                                        Page, PerPage, Order, UserID, QString)

        return render(request, 'Fax/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getSentListURL(request):
    """
    팩스 전송내역 확인 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    팩스 미리보기 팝업 URL을 반환하며, 팩스전송을 위한 TIF 포맷 변환 완료 후 호출 할 수 있습니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getUnitCost(request):
    """
    팩스 전송시 과금되는 포인트 단가를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 수신번호 유형 : "일반" / "지능" 중 택 1
        # └ 일반망 : 지능망을 제외한 번호
        # └ 지능망 : 030*, 050*, 070*, 080*, 대표번호
        receiveNumType = "지능"

        result = faxService.getUnitCost(CorpNum, receiveNumType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeInfo(request):
    """
    팝빌 팩스 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 수신번호 유형 : "일반" / "지능" 중 택 1
        # └ 일반망 : 지능망을 제외한 번호
        # └ 지능망 : 030*, 050*, 070*, 080*, 대표번호
        receiveNumType = "지능"

        response = faxService.getChargeInfo(CorpNum, receiveNumType)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
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
    사용하고자 하는 아이디의 중복여부를 확인합니다.
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
    사용자를 연동회원으로 가입처리합니다.
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
            ContactEmail="",

            # 담당자 연락처 (최대 20자)
            ContactTEL=""
        )

        response = faxService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = faxService.getCorpInfo(CorpNum)

        return render(request, 'getCorpInfo.html', {'response': response})
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

        response = faxService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://docs.popbill.com/fax/python/api#RegistContact
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

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = faxService.registContact(CorpNum, newContact)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://docs.popbill.com/fax/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = faxService.getContactInfo(CorpNum, contactID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://docs.popbill.com/fax/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = faxService.listContact(CorpNum)

        return render(request, 'listContact.html', {'listContact': listContact})
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
            tel="",

            # 담당자 메일주소 (최대 100자)
            email="",

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = faxService.updateContact(CorpNum, updateInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
