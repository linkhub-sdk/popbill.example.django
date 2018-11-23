# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import PopbillException, ContactInfo, CorpInfo, JoinForm, MessageService, \
    MessageReceiver

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 MessageService 객체 생성
messageService = MessageService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
messageService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Message/Index.html', {})


def getSenderNumberMgtURL(request):
    """
    발신번호 관리 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = messageService.getSenderNumberMgtURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSenderNumberList(request):
    """
    등록된 문자 발신번호 목록을 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        senderList = messageService.getSenderNumberList(CorpNum)

        return render(request, 'Message/GetSenderNumberList.html', {'senderList': senderList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendSMS(request):
    """
    1건의 SMS(단문)를 전송합니다.
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

        # 수신번호
        ReceiverNum = "010111222"

        # 수신자명
        ReceiverName = "수신자명"

        # 단문메시지 내용, 90Byte 초과시 길이가 조정되 전송됨
        Contents = "문자 API 단건전송 테스트"

        # 예약전송시간, 형태 yyyyMMddHHmmss 공백 기재시 즉시전송
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendSMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendSMS_multi(request):
    """
    [대량전송 / 부분전송] 단문SMS를 전송합니다.
    - 대량전송/부분전송에 대한 설명은 "[문자 API 연동매뉴얼] > 3.2.1 SendSMS(단문전송)"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = "07043042991"

        # 단문메시지 내용(동보전송용)
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 형태 yyyyMMddHHmmss 공백 기재시 즉시전송
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        # 개별수신정보 배열(최대 10000건)
        messages = []
        for x in range(0, 10):
            messages.append(
                MessageReceiver(
                    snd='07043042991',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='010111222',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='단문 문자 API TEST'  # 메시지 내용, msg값이 없는경우 동보전송 메시지로 전송됨
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendSMS_multi(CorpNum, Sender, Contents, messages,
                                                  reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendLMS(request):
    """
    1건의 LMS(장문)를 전송합니다.
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

        # 수신번호
        ReceiverNum = "010111222"

        # 수신자명
        ReceiverName = "수신자명"

        # 장문 메시지 제목
        Subject = "장문 문자 제목"

        # 장문 메시지 내용, 길이가 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "장문메시지 단건전송 테스트"

        # 예약전송시간, 형태 yyyyMMddHHmmss, 공백 처리시 즉시전송
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendLMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Subject, Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendLMS_multi(request):
    """
    [대량전송 / 부분전송] 장문LMS을 전송합니다.
    - 대량전송/부분전송에 대한 설명은 "[문자 API 연동매뉴얼] > 3.2.1 SendLMS(장문전송)"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = "07043042991"

        # 장문 메시지 제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 장문 메시지 내용, 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 공백 처리시 즉시전송(작성형태 yyyyMMddHHmmss)
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        # 개별 전송정보 배열 (최대 1000건)
        messages = []
        for x in range(0, 100):
            messages.append(
                MessageReceiver(
                    snd='07043042991',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='010111222',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='장문 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨.
                    sjt='장문문자제목'  # 장문 메시지 제목
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendLMS_multi(CorpNum, Sender, Subject, Contents,
                                                  messages, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendMMS(request):
    """
    1건의 MMS(포토)를 전송합니다.
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

        # 수신번호
        ReceiverNum = "010111222"

        # 수신자명
        ReceiverName = "수신자명"

        # 장문 메시지 제목
        Subject = "멀티 문자 제목"

        # 장문 메시지 내용, 길이가 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "멀티메시지 단건전송 테스트"

        # 예약전송시간, 형태 yyyyMMddHHmmss, 공백 처리시 즉시전송
        reserveDT = ""

        # 전송할 파일경로 (이미지 파일의 크기는 최대 300Kbyte(JPEG), 가로/세로 1500px 이하 권장)
        FilePath = './MessageExample/static/image/test.jpg'

        # 광고문자 전송여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendMMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Subject, Contents, FilePath, reserveDT, adsYN, UserID, SenderName,
                                            RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendMMS_multi(request):
    """
    [대량전송 / 부분전송] 포토MMS를 전송합니다.
    - 대량전송/부분전송에 대한 설명은 "[문자 API 연동매뉴얼] > 3.2.3 SendMMS(포토)"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = "07043042991"

        # 장문 메시지 제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 장문 메시지 내용, 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 공백 처리시 즉시전송(작성형태 yyyyMMddHHmmss)
        reserveDT = ""

        # 전송할 파일경로 (이미지 파일의 크기는 최대 300Kbyte(JPEG), 가로/세로 1500px 이하 권장)
        filePath = './MessageExample/static/image/test.jpg'

        # 광고문자 전송여부
        adsYN = False

        # 개별 전송정보 배열 (최대 1000건)
        messages = []
        for x in range(0, 5):
            messages.append(
                MessageReceiver(
                    snd='07043042991',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='010111222',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='멀티 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨.
                    sjt='멀티 문자제목'  # 장문 메시지 제목
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendMMS_Multi(CorpNum, Sender, Subject, Contents,
                                                  messages, filePath, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendXMS(request):
    """
    메시지 내용의 길이(90Byte)에 따라 SMS/LMS를 자동인식하여 전송합니다.
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

        # 수신번호
        ReceiverNum = "010111222"

        # 수신자명
        ReceiverName = "수신자명"

        # 메시지 내용, 90Byte 기준으로 단/장문 자동인식
        Contents = "장문메시지 단건전송 테스트"

        # 메시지 제목
        Subject = "장문 문자 제목"

        # 예약전송시간, 형태 yyyyMMddHHmmss 공백 처리시 즉시전송
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendXMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Subject, Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendXMS_multi(request):
    """
    [대량전송 / 부분전송] 메시지 내용의 길이(90Byte)에 따라 SMS/LMS를 자동인식하여 전송합니다
    - 대량전송/부분전송에 대한 설명은 "[문자 API 연동매뉴얼] > 3.2.4 SendSMS(단문전송)"을
      참조하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = "07043042991"

        # 메시지제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 메시지 내용(동보전송용)
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 공백 처리시 즉시전송(작성형태 yyyyMMddHHmmss)
        reserveDT = ""

        # 광고문자 전송여부
        adsYN = False

        messages = []  # 개별 전송정보 배열, 최대 1000건

        for x in range(0, 10):
            messages.append(
                MessageReceiver(
                    snd='07043042991',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='010111222',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='문자 API TEST',  # 90Byte를 기준으로 단/장문을 자동으로 인식하여 전송
                    sjt='장문문자제목'  # 장문메시지 제목
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendXMS_multi(CorpNum, Sender, Subject, Contents,
                                                  messages, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserve(request):
    """
    예약문자전송을 취소합니다.
    - 예약취소는 예약전송시간 10분전까지만 가능합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약문자전송 접수번호
        receiptNum = "018012213000000035"

        response = messageService.cancelReserve(CorpNum, receiptNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserveRN(request):
    """
    문자전송요청시 할당한 전송요청번호(requestNum)로 예약문자전송을 취소합니다.
    - 예약취소는 예약전송시간 10분전까지만 가능합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약문자전송 요청시 할당한 전송요청번호
        requestNum = "20180912104018"

        response = messageService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessages(request):
    """
    문자전송요청에 대한 전송결과를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자전송 요청시 반환받은 접수번호
        receiptNum = "018012213000000035"

        resultList = messageService.getMessages(CorpNum, receiptNum)

        return render(request, 'Message/GetMessages.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessagesRN(request):
    """
    문자전송요청시 할당한 전송요청번호(requestNum)로 전송상태를 확인합니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자전송 요청 시 할당한 전송요청번호(requestNum)
        requestNum = '20180910103454'

        resultList = messageService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Message/GetMessages.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getStates(request):
    """
    문자 전송내역 요약정보를 확인한다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자전송 요청시 반환받은 접수번호
        receiptNumList = []
        receiptNumList.append("018041717000000018")
        receiptNumList.append("018041717000000019")

        resultList = messageService.getStates(CorpNum, receiptNumList)

        return render(request, 'Message/GetStates.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 문자전송 내역을 조회합니다.
     - 최대 검색기간 : 6개월 이내
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20171201"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20180131"

        # 전송상태 배열, 1-대기, 2-성공, 3-실패, 4-취소
        State = ['1', '2', '3', '4']

        # 전송유형, SMS-단문, LMS-장문, MMS-포토
        Item = ['SMS', 'LMS', 'MMS']

        # 예약전송 검색여부, 0-전체조회, 1-예약전송건 조회
        ReserveYN = '0'

        # 개인조회여부, 0-전체조회, 1-개인조회
        SenderYN = '0'

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향, D-내림차순, A-오름차순
        Order = "D"

        response = messageService.search(CorpNum, SDate, EDate, State, Item, ReserveYN,
                                         SenderYN, Page, PerPage, Order, UserID)

        return render(request, 'Message/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSentListURL(request):
    """
    문자메시지 전송내역 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = messageService.getSentListURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAutoDenyList(request):
    """
    080 서비스 수신거부 목록을 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = messageService.getAutoDenyList(CorpNum, UserID)

        return render(request, 'Message/GetAutoDenyList.html', {'response': response})
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

        url = messageService.getChargeURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 문자 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 문자유형, [SMS(단문) / LMS(장문) / MMS(포토)]
        MsgType = "SMS"

        response = messageService.getChargeInfo(CorpNum, MsgType, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    문자메시지 전송단가를 확인합니다.
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 문자전송유형, [SMS(단문) / LMS(장문) / MMS(포토)]
        MsgType = "MMS"

        result = messageService.getUnitCost(CorpNum, MsgType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = messageService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를 이용하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = messageService.getPartnerBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPartnerURL(request):
    """
    파트너 포인트 충전 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # CHRG-파트너 포인트충전
        TOGO = "CHRG"

        url = messageService.getPartnerURL(CorpNum, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def checkIsMember(request):
    """
    해당 사업자의 파트너 연동회원 가입여부를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = messageService.checkIsMember(CorpNum)

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

        response = messageService.checkID(memberID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def joinMember(request):
    """
    파트너의 연동회원으로 회원가입을 요청합니다.
    아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    """
    try:
        # 회원정보
        newMember = JoinForm(

            # 회원아이디, 최대 20자
            ID="testkorea",

            # 비밀번호, 최대 20자
            PWD="this_is_password",

            # 사업자번호
            CorpNum="1234567890",

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
            ContactTEL="070-4304-2991",

            # 담당자 휴대폰번호
            ContactHP="010-2222-3333",

            # 담당자 팩스번호
            ContactFAX="070-4304-2991",

            # 담당자 메일주소
            ContactEmail="test@test.com"
        )

        response = messageService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
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

        url = messageService.getAccessURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
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
            id="testkorea_1117",

            # 비밀번호
            pwd="this_is_password",

            # 담당자명
            personName="정대리",

            # 연락처
            tel="010-4304-2991",

            # 휴대폰번호
            hp="010-4304-2991",

            # 팩스번호
            fax="070-4324-2991",

            # 메일주소
            email="dev@linkhub.co.kr",

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True
        )

        response = messageService.registContact(CorpNum, newContact, UserID)

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

        listContact = messageService.listContact(CorpNum, UserID)

        return render(request, 'listContact.html', {'listContact': listContact})
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
            ceoname="대표자성명",

            # 상호
            corpName="상호",

            # 주소
            addr="주소",

            # 업태
            bizType="업태",

            # 종목
            bizClass="종목"
        )

        response = messageService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

        response = messageService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html',
                      {'ceoname': response.ceoname, 'corpName': response.corpName,
                       'addr': response.addr, 'bizType': response.bizType,
                       'bizClass': response.bizClass})
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

            # 담당자 성명
            personName="담당자 성명",

            # 연락처
            tel="070-4304-2991",

            # 휴대폰번호
            hp="010-4324-4324",

            # 팩스번호
            fax="070-111-222",

            # 메일주소
            email="dev@linkhub.co.kr",

            # 회사조회 여부, True-회사조회, False-개인조회
            searchAllAllowYN=True
        )

        response = messageService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
