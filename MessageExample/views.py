# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import PopbillException, ContactInfo, CorpInfo, JoinForm, MessageService, \
    MessageReceiver

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 MessageService 객체 생성
messageService = MessageService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
messageService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
messageService.IPRestrictOnOff = settings.IPRestrictOnOff

# 팝빌 API 서비스 고정 IP 사용여부(GA), true-사용, false-미사용, 기본값(false)
messageService.UseStaticIP = settings.UseStaticIP

#로컬서버 시간 사용여부, 권장(True)
messageService.UseLocalTimeYN = settings.UseLocalTimeYN

# 문자를 전송하기 위해 발신번호 사전등록을 합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌 사이트 로그인 > [문자/팩스] > [문자] > [발신번호 사전등록] 메뉴에서 등록
# 2. getSenderNumberMgtURL API를 통해 반환된 URL을 이용하여 발신번호 등록


def index(request):
    return render(request, 'Message/Index.html', {})


def getSenderNumberMgtURL(request):
    """
    발신번호 관리 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/message/python/api#GetSenderNumberMgtURL
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
    - https://docs.popbill.com/message/python/api#GetSenderNumberList
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
    - https://docs.popbill.com/message/python/api#SendSMS
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
    [대량전송] 단문SMS를 전송합니다.
    - https://docs.popbill.com/message/python/api#SendSMS_Multi
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
                    msg='단문 문자 API TEST'  # 메시지 내용, msg값이 없는경우 동보전송 메시지로 전송됨, 90Byte 초과시 길이가 조정되 전송됨
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
    - https://docs.popbill.com/message/python/api#SendLMS
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
    [대량전송] 장문LMS을 전송합니다.
    - https://docs.popbill.com/message/python/api#SendLMS_Multi
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
                    msg='장문 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨. 2000Byte 초과시 길이가 조정되어 전송됨.
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
    - https://docs.popbill.com/message/python/api#SendMMS
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 전송할 파일경로 (이미지 파일의 크기는 최대 300Kbyte(JPEG), 가로/세로 1000px 이하 권장)
        FilePath = './MessageExample/static/image/mms.jpg'

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
    [대량전송] 포토MMS를 전송합니다.
    - 메시지 내용이 2,000Byte 초과시 메시지 내용은 자동으로 제거됩니다.
    - 이미지 파일의 크기는 최대 300Kbtye (JPEG), 가로/세로 1000px 이하 권장
    - https://docs.popbill.com/message/python/api#SendMMS_Multi
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 전송할 파일경로 (이미지 파일의 크기는 최대 300Kbyte(JPEG), 가로/세로 1000px 이하 권장)
        filePath = './MessageExample/static/image/mms.jpg'

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
                    msg='멀티 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨. 2000Byte 초과시 길이가 조정되어 전송됨.
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
    - 90byte 초과시 LMS(장문)으로 인식 합니다.
    - https://docs.popbill.com/message/python/api#SendXMS
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
    - 90byte 초과시 LMS(장문)으로 인식 합니다.
    - https://docs.popbill.com/message/python/api#SendXMS_Multi
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

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
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
    문자전송요청시 발급받은 접수번호(receiptNum)로 예약문자 전송을 취소합니다.
    - 예약취소는 예약전송시간 10분전까지만 가능합니다.
    - https://docs.popbill.com/message/python/api#CancelReserve
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
    - https://docs.popbill.com/message/python/api#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약문자전송 요청시 할당한 전송요청번호
        requestNum = "20190116-001"

        response = messageService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessages(request):
    """
    문자전송요청시 발급받은 접수번호(receiptNum)로 전송상태를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetMessages
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
    - https://docs.popbill.com/message/python/api#GetMessagesRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자전송 요청 시 할당한 전송요청번호(requestNum)
        requestNum = '20190116-001'

        resultList = messageService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Message/GetMessages.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getStates(request):
    """
    문자 전송내역 요약정보를 확인합니다. (최대 1000건)
    - https://docs.popbill.com/message/python/api#GetStates
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
    - https://docs.popbill.com/message/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20190101"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20190116"

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
    - https://docs.popbill.com/message/python/api#GetSentListURL
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
    - https://docs.popbill.com/message/python/api#GetAutoDenyList
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
    - https://docs.popbill.com/message/python/api#GetChargeURL
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
    - https://docs.popbill.com/message/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 문자유형, [SMS(단문) / LMS(장문) / MMS(포토)]
        MsgType = "SMS"

        response = messageService.getChargeInfo(CorpNum, MsgType, UserID)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    문자메시지 전송단가를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 문자전송유형, [SMS(단문) / LMS(장문) / MMS(포토)]
        MsgType = "SMS"

        result = messageService.getUnitCost(CorpNum, MsgType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    - https://docs.popbill.com/message/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = messageService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPaymentURL(request):
    """
    팝빌 연동회원 포인트 결재내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/message/python/api#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = messageService.getPaymentURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUseHistoryURL(request):
    """
    팝빌 연동회원 포인트 사용내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/message/python/api#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = messageService.getUseHistoryURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - 과금방식이 연동과금인 경우 연동회원 잔여포인트(GetBalance API)를 이용하시기 바랍니다.
    - https://docs.popbill.com/message/python/api#GetPartnerBalance
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
    파트너 포인트 충전 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/message/python/api#GetPartnerURL
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
    - https://docs.popbill.com/message/python/api#CheckIsMember
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
    - https://docs.popbill.com/message/python/api#CheckID
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
    - 아이디 중복확인은 (CheckID API)를 참조하시길 바랍니다.
    - https://docs.popbill.com/message/python/api#JoinMember
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

        response = messageService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    - https://docs.popbill.com/message/python/api#GetAccessURL
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
    - https://docs.popbill.com/message/python/api#RegistContact
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
            searchRole=1,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
        )

        response = messageService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원의 담당자 정보를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = messageService.getContactInfo(CorpNum, contactID, UserID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원의 담당자 목록을 확인합니다.
    - https://docs.popbill.com/message/python/api#ListContact
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
    - https://docs.popbill.com/message/python/api#UpdateCorpInfo
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

        response = messageService.updateCorpInfo(CorpNum, corpInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = messageService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/message/python/api#UpdateContact
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
            searchRole=1,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
        )

        response = messageService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
