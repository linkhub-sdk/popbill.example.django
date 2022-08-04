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

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
messageService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
messageService.UseLocalTimeYN = settings.UseLocalTimeYN

# 문자를 전송하기 위해 발신번호 사전등록을 합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌 사이트 로그인 > [문자/팩스] > [문자] > [발신번호 사전등록] 메뉴에서 등록
# 2. getSenderNumberMgtURL API를 통해 반환된 URL을 이용하여 발신번호 등록


def index(request):
    return render(request, 'Message/Index.html', {})

def getSenderNumberMgtURL(request):
    """
    발신번호를 등록하고 내역을 확인하는 문자 발신번호 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    팝빌에 등록한 연동회원의 문자 발신번호 목록을 확인합니다.
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
    최대 90byte의 단문(SMS) 메시지 1건 전송을 팝빌에 접수합니다.
    - https://docs.popbill.com/message/python/api#SendSMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        ReceiverNum = ""

        # 수신자명
        ReceiverName = "수신자명"

        # 단문메시지 내용, 90Byte 초과시 길이가 조정되 전송됨
        Contents = "문자 API 단건전송 테스트"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendSMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendSMS_multi(request):
    """
    최대 90byte의 단문(SMS) 메시지 다수건 전송을 팝빌에 접수합니다. (최대 1,000건)
    - 모든 수신자에게 동일한 내용을 전송하거나(동보전송), 수신자마다 개별 내용을 전송할 수 있습니다(대량전송).
    - https://docs.popbill.com/message/python/api#SendSMS_Multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = ""

        # 단문메시지 내용(동보전송용)
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 개별수신정보 배열(최대 10000건)
        messages = []
        for x in range(0, 10):
            messages.append(
                MessageReceiver(
                    snd='',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='단문 문자 API TEST'  # 메시지 내용, msg값이 없는경우 동보전송 메시지로 전송됨, 90Byte 초과시 길이가 조정되 전송됨
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendSMS_multi(CorpNum, Sender, Contents, messages,
                                                    reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendLMS(request):
    """
    최대 2,000byte의 장문(LMS) 메시지 1건 전송을 팝빌에 접수합니다.
    - https://docs.popbill.com/message/python/api#SendLMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        ReceiverNum = ""

        # 수신자명
        ReceiverName = "수신자명"

        # 장문 메시지 제목
        Subject = "장문 문자 제목"

        # 장문 메시지 내용, 길이가 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "장문메시지 단건전송 테스트"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendLMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Subject, Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendLMS_multi(request):
    """
    최대 2,000byte의 장문(LMS) 메시지 다수건 전송을 팝빌에 접수합니다. (최대 1,000건)
    - 모든 수신자에게 동일한 내용을 전송하거나(동보전송), 수신자마다 개별 내용을 전송할 수 있습니다(대량전송).
    - https://docs.popbill.com/message/python/api#SendLMS_Multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = ""

        # 장문 메시지 제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 장문 메시지 내용, 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 개별 전송정보 배열 (최대 1000건)
        messages = []
        for x in range(0, 100):
            messages.append(
                MessageReceiver(
                    snd='',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='장문 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨. 2000Byte 초과시 길이가 조정되어 전송됨.
                    sjt='장문문자제목'  # 장문 메시지 제목
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendLMS_multi(CorpNum, Sender, Subject, Contents,
                                                messages, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendMMS(request):
    """
    최대 2,000byte의 메시지와 이미지로 구성된 포토문자(MMS) 1건 전송을 팝빌에 접수합니다.
    - 이미지 파일 포맷/규격 : 최대 300Kbyte(JPEG, JPG), 가로/세로 1,000px 이하 권장
    - https://docs.popbill.com/message/python/api#SendMMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        ReceiverNum = ""

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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
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
    최대 2,000byte의 메시지와 이미지로 구성된 포토문자(MMS) 다수건 전송을 팝빌에 접수합니다. (최대 1,000건)
    - 이미지 파일 포맷/규격 : 최대 300Kbyte(JPEG), 가로/세로 1,000px 이하 권장
    - 모든 수신자에게 동일한 내용을 전송하거나(동보전송), 수신자마다 개별 내용을 전송할 수 있습니다(대량전송).
    - https://docs.popbill.com/message/python/api#SendMMS_Multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = ""

        # 장문 메시지 제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 장문 메시지 내용, 2000Byte 초과시 길이가 조정되어 전송됨.
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 전송할 파일경로 (이미지 파일의 크기는 최대 300Kbyte(JPEG), 가로/세로 1000px 이하 권장)
        filePath = './MessageExample/static/image/mms.jpg'

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 개별 전송정보 배열 (최대 1000건)
        messages = []
        for x in range(0, 5):
            messages.append(
                MessageReceiver(
                    snd='',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='멀티 문자 API TEST',  # msg값이 없는 경우 동보전송용 메시지로 전송됨. 2000Byte 초과시 길이가 조정되어 전송됨.
                    sjt='멀티 문자제목'  # 장문 메시지 제목
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendMMS_Multi(CorpNum, Sender, Subject, Contents,
                                                messages, filePath, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendXMS(request):
    """
    메시지 길이(90byte)에 따라 단문/장문(SMS/LMS)을 자동으로 인식하여 1건의 메시지를 전송을 팝빌에 접수합니다.
    - https://docs.popbill.com/message/python/api#SendXMS
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호
        Sender = ""

        # 발신자명
        SenderName = "발신자명"

        # 수신번호
        ReceiverNum = ""

        # 수신자명
        ReceiverName = "수신자명"

        # 메시지 내용, 90Byte 기준으로 단/장문 자동인식
        Contents = "장문메시지 단건전송 테스트"

        # 메시지 제목
        Subject = "장문 문자 제목"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendXMS(CorpNum, Sender, ReceiverNum, ReceiverName,
                                            Subject, Contents, reserveDT, adsYN, UserID, SenderName, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendXMS_multi(request):
    """
    메시지 길이(90byte)에 따라 단문/장문(SMS/LMS)을 자동으로 인식하여 다수건의 메시지 전송을 팝빌에 접수합니다. (최대 1,000건)
    - 모든 수신자에게 동일한 내용을 전송하거나(동보전송), 수신자마다 개별 내용을 전송할 수 있습니다(대량전송).
    - 단문(SMS) = 90byte 이하의 메시지, 장문(LMS) = 2000byte 이하의 메시지.
    - https://docs.popbill.com/message/python/api#SendXMS_Multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 발신번호(동보전송용)
        Sender = ""

        # 메시지제목(동보전송용)
        Subject = "동보전송용 메시지 제목"

        # 메시지 내용(동보전송용)
        Contents = "동보전송용 메시지 내용"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        reserveDT = ""

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        adsYN = False

        messages = []  # 개별 전송정보 배열, 최대 1000건

        for x in range(0, 10):
            messages.append(
                MessageReceiver(
                    snd='',  # 발신번호
                    sndnm='발신자명',  # 발신자명
                    rcv='',  # 수신번호
                    rcvnm='수신자명' + str(x),  # 수신자명
                    msg='문자 API TEST',  # 90Byte를 기준으로 단/장문을 자동으로 인식하여 전송
                    sjt='장문문자제목'  # 장문메시지 제목
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        RequestNum = ""

        receiptNum = messageService.sendXMS_multi(CorpNum, Sender, Subject, Contents,
                                                    messages, reserveDT, adsYN, UserID, RequestNum)

        return render(request, 'Message/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def cancelReserve(request):
    """
    팝빌에서 반환받은 접수번호를 통해 예약접수된 문자 메시지 전송을 취소합니다. (예약시간 10분 전까지 가능)
    - https://docs.popbill.com/message/python/api#CancelReserve
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약문자 전송요청시 팝빌로부터 반환 받은 접수번호
        receiptNum = "018012213000000035"

        response = messageService.cancelReserve(CorpNum, receiptNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def cancelReserveRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 예약접수된 문자 전송을 취소합니다. (예약시간 10분 전까지 가능)
    - https://docs.popbill.com/message/python/api#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약문자 전송요청시 파트너가 할당한 전송요청 번호
        requestNum = ""

        response = messageService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getMessages(request):
    """
    팝빌에서 반환받은 접수번호를 통해 문자 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetMessages
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자 전송요청시 팝빌로부터 반환 받은 접수번호
        receiptNum = "018012213000000035"

        resultList = messageService.getMessages(CorpNum, receiptNum)

        return render(request, 'Message/GetMessages.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getMessagesRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 문자 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetMessagesRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 문자 전송요청시 파트너가 할당한 전송요청 번호
        requestNum = ''

        resultList = messageService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Message/GetMessages.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def search(request):
    """
    검색조건을 사용하여 문자전송 내역을 조회합니다. (조회기간 단위 : 최대 2개월)
    - 문자 접수일시로부터 6개월 이내 접수건만 조회할 수 있습니다.
    - https://docs.popbill.com/message/python/api#Search
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 최대 검색기간 : 6개월 이내
        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20220701"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20220731"

        # 전송상태 배열 ("1" , "2" , "3" , "4" 중 선택, 다중 선택 가능)
        # └ 1 = 대기 , 2 = 성공 , 3 = 실패 , 4 = 취소
        # - 미입력 시 전체조회
        State = ['1', '2', '3', '4']

        # 검색대상 배열 ("SMS" , "LMS" , "MMS" 중 선택, 다중 선택 가능)
        # └ SMS = 단문 , LMS = 장문 , MMS = 포토문자
        # - 미입력 시 전체조회
        Item = ['SMS', 'LMS', 'MMS']

        # 예약여부 (false , true 중 택 1)
        # └ false = 전체조회, true = 예약전송건 조회
        # - 미입력시 기본값 false 처리
        ReserveYN = '0'

        # 개인조회 여부 (false , true 중 택 1)
        # false = 접수한 문자 전체 조회 (관리자권한)
        # true = 해당 담당자 계정으로 접수한 문자만 조회 (개인권한)
        # 미입력시 기본값 false 처리
        SenderYN = '0'

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향, D-내림차순, A-오름차순
        Order = "D"

        # 조회하고자 하는 발신자명 또는 수신자명
        # - 미입력시 전체조회
        QString = ""

        response = messageService.search(CorpNum, SDate, EDate, State, Item, ReserveYN,
                                            SenderYN, Page, PerPage, Order, UserID, QString)

        return render(request, 'Message/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getSentListURL(request):
    """
    문자 전송내역 확인 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    전용 080 번호에 등록된 수신거부 목록을 반환합니다.
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

def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetBalance
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = messageService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeURL(request):
    """
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getUnitCost(request):
    """
    문자 전송시 과금되는 포인트 단가를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 문자전송 유형 : SMS / LMS / MMS 중 택 1
        # └ SMS = 단문, LMS = 장문, MMS = 포토문자
        MsgType = "SMS"

        result = messageService.getUnitCost(CorpNum, MsgType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeInfo(request):
    """
    팝빌 문자 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum
        
        # 문자전송 유형 : SMS / LMS / MMS 중 택 1
        # └ SMS = 단문, LMS = 장문, MMS = 포토문자
        MsgType = "SMS"

        response = messageService.getChargeInfo(CorpNum, MsgType)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
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
    사용하고자 하는 아이디의 중복여부를 확인합니다.
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
    사용자를 연동회원으로 가입처리합니다.
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
            ContactEmail="",

            # 담당자 연락처 (최대 20자)
            ContactTEL=""
        )

        response = messageService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
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

def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = messageService.getCorpInfo(CorpNum, UserID)

        return render(request, 'getCorpInfo.html', {'response': response})
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

        response = messageService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
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
            tel="",

            # 담당자 이메일 (최대 100자)
            email="",

            #담당자 조회권한, 1(개인) 2(읽기) 3(회사)
            searchRole=1
        )

        response = messageService.registContact(CorpNum, newContact, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://docs.popbill.com/message/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = messageService.getContactInfo(CorpNum, contactID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://docs.popbill.com/message/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = messageService.listContact(CorpNum)

        return render(request, 'listContact.html', {'listContact': listContact})
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

        response = messageService.updateContact(CorpNum, updateInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# def getStates(request):
#     """
#     문자 전송내역 요약정보를 확인합니다. (최대 1000건)
#     """
#     try:
#         # 팝빌회원 사업자번호
#         CorpNum = settings.testCorpNum

#         # 문자전송 요청시 반환받은 접수번호
#         receiptNumList = []
#         receiptNumList.append("018041717000000018")
#         receiptNumList.append("018041717000000019")

#         resultList = messageService.getStates(CorpNum, receiptNumList)

#         return render(request, 'Message/GetStates.html', {'resultList': resultList})
#     except PopbillException as PE:
#         return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
