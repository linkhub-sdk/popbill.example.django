# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import PopbillException, ContactInfo, CorpInfo, JoinForm, KakaoService, KakaoReceiver, \
    KakaoButton

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 KakaoService 객체 생성
kakaoService = KakaoService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
kakaoService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Kakao/Index.html', {})


def getURL_PLUSFRIEND(request):
    """
    플러스친구 계정관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다"
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # PLUSFRIEND(플러스친구계정관리), SENDER(발신번호관리), TEMPLATE(알림톡템플릿관리), BOX(카카오톡전송내역)
        TOGO = "PLUSFRIEND"

        url = kakaoService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listPlusFriendID(request):
    """
    팝빌에 등록된 플러스친구 목록을 반환 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = kakaoService.listPlusFriendID(CorpNum, UserID)

        return render(request, 'Kakao/ListPlusFriendID.html', {'listPlusFriendID': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL_SENDER(request):
    """
    발신번호 관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # PLUSFRIEND(플러스친구계정관리), SENDER(발신번호관리), TEMPLATE(알림톡템플릿관리), BOX(카카오톡전송내역)
        TOGO = "SENDER"

        url = kakaoService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSenderNumberList(request):
    """
    팝빌에 등록된 발신번호 목록을 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        senderList = kakaoService.getSenderNumberList(CorpNum)

        return render(request, 'Kakao/GetSenderNumberList.html', {'senderList': senderList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL_TEMPLATE(request):
    """
    알림톡 템플릿관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # PLUSFRIEND(플러스친구계정관리), SENDER(발신번호관리), TEMPLATE(알림톡템플릿관리), BOX(카카오톡전송내역)
        TOGO = "TEMPLATE"

        url = kakaoService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listATStemplate(request):
    """
    (주)카카오로 부터 승인된 알림톡 템플릿 목록을 확인 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        templateList = kakaoService.listATSTemplate(CorpNum, UserID)

        return render(request, 'Kakao/ListATSTemplate.html', {'templateList': templateList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendATS_one(request):
    """
    단건의 알림톡을 전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿코드
        # 승인된 알림톡 템플릿 코드는 ListATStemplate API, GetURL(TEMPLATE) API, 혹은 팝빌사이트에서 확인이 가능합니다.
        templateCode = "018080000079"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # 알림톡 내용 (최대 1000자)
        content = "테스트 템플릿 입니다."

        # 대체문자 내용 (최대 2000byte)
        altContent = "알림톡 대체 문자"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        # 수신번호
        receiver = "01012341234"

        # 수신자 이름
        receiverName = "partner"

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendATS(CorpNum, templateCode, snd, content, altContent,
                                          altSendType, sndDT, receiver, receiverName, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendATS_same(request):
    """
    동일한 내용의 알림톡을 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿 코드
        # 승인된 알림톡 템플릿 코드는 ListATStemplate API, GetURL(TEMPLATE) API, 혹은 팝빌사이트에서 확인이 가능합니다.
        templateCode = "018080000079"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # [동보] 알림톡 내용 (최대 1000자)
        content = "[테스트] 테스트 템플릿입니다."

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "[테스트] 알림톡 대체 문자"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="010987123",  # 수신번호
                    rcvnm="popbill"  # 수신자 이름
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendATS_multi(CorpNum, templateCode, snd, content, altContent,
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendATS_multi(request):
    """
    개별 내용의 알림톡을 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿 코드
        templateCode = "018080000079"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="010456456",  # 수신번호
                    rcvnm="linkhub",  # 수신자 이름
                    msg="[테스트] 테스트 템플릿입니다. " + str(x) + "번째",  # 알림톡 내용 (최대 1000자)
                    altmsg="수신번호 010-456-456 알림톡 대체문자"  # 대체문자 내용 (최대 2000byte)
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendATS_multi(CorpNum, templateCode, snd, "", "",
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFTS_one(request):
    """
    단건의 친구톡 텍스트를 전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "01083490706"

        # 친구톡 내용 (최대 1000자)
        content = "친구톡 내용"

        # 대체문자 내용 (최대 2000byte)
        altContent = "대체문자 내용"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        # 수신번호
        receiver = "01012349876"

        # 수신자 이름
        receiverName = "partner"

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 1):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # 버튼유형 [WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="메시지전달",
                t="MD",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS(CorpNum, plusFriendID, snd, content, altContent, altSendType, sndDT,
                                          receiver, receiverName, KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFTS_same(request):
    """
    동일한 내용의 친구톡 텍스트를 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # [동보] 친구톡 내용 (최대 1000자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101235678",  # 수신번호
                    rcvnm="팝친"  # 수신자 이름
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 1):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # [버튼유형 WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="봇키워드",
                t="BK",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, content, altContent, altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFTS_multi(request):
    """
    개별 내용의 친구톡 텍스트를 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101234567",
                    rcvnm="김현진",
                    msg="안녕하세요 " + str(x) + "님 링크허브입니다.",
                    altmsg="(친구톡 대체문자) 안녕하세요 링크허브입니다."
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 1):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # [버튼유형 WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="봇키워드",
                t="BK",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, "", "", altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFMS_one(request):
    """
    단건의 친구톡 이미지를 전송합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # 친구톡 내용 (최대 400자)
        content = "친구톡 내용"

        # 대체문자 내용 (최대 2000byte)
        altContent = "대체문자 내용"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        # 파일경로
        # 이미지 전송 규격 (전송포맷-JPG,JPEG / 용량제한-최대 500Kbte / 이미지 가로&세로 비율 : 1.5 미만)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        # 수신번호
        receiver = "01012345678"

        # 수신자 이름
        receiverName = "partner"

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 2):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # 버튼유형 [WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="메시지전달",
                t="MD",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS(CorpNum, plusFriendID, snd, content, altContent,
                                          altSendType, sndDT, filePath, imageURL, receiver, receiverName,
                                          KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFMS_same(request):
    """
    동일한 내용의 친구톡 이미지를 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # [동보] 친구톡 내용 (최대 400자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        # 파일경로
        # 이미지 전송 규격 (전송포맷-JPG,JPEG / 용량제한-최대 500Kbte / 이미지 가로&세로 비율 : 1.5 미만)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101235678",  # 수신번호
                    rcvnm="팝친"  # 수신자 이름
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 2):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # 버튼유형 [WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="봇키워드",
                t="BK",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, content, altContent,
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFMS_multi(request):
    """
    개별 내용의 친구톡 이미지를 대량 전송 합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 플러스 친구 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "010111222"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약일시 (작성형식 : yyyyMMddHHmmss)
        sndDT = ""

        # 파일경로
        # 이미지 전송 규격 (전송포맷-JPG,JPEG / 용량제한-최대 500Kbte / 이미지 가로&세로 비율 : 1.5 미만)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        KakaoMessages = []  # 1회 최대 전송 1,000건 전송 가능
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101234567",  # 수신번호
                    rcvnm="김현진",  # 수신자 이름
                    msg="안녕하세요 " + str(x) + "님 링크허브입니다.",  # 친구톡 내용 (최대 400자)
                    altmsg="(친구톡 대체문자) 안녕하세요 링크허브입니다."  # 대체문자 내용 (최대 2000byte)
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []
        for x in range(0, 2):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",  # 버튼명
                    t="WL",  # 버튼유형 [WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                    u1="http://www.popbill.com",  # [앱링크-Android, 웹링크-Mobile]
                    u2="http://www.popbill.com"  # [앱링크-IOS, 웹링크-PC URL]
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="봇키워드",
                t="BK",
            )
        )

        # 광고여부
        adsYN = False

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, "", "",
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserve(request):
    """
    알림톡/친구톡 예약전송을 취소합니다.
     - 예약취소는 예약전송시간 10분전까지만 가능합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약 알림톡/친구톡 전송 접수번호
        receiptNum = "018030210070700001"

        result = kakaoService.cancelReserve(CorpNum, receiptNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserveRN(request):
    """
    전송요청번호(requestNum)를 할당한 알림톡/친구톡 예약전송건을 취소합니다.
     - 예약취소는 예약전송시간 10분전까지만 가능합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약전송 요청시 할당한 전송요청번호
        requestNum = "20180809151234"

        result = kakaoService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessages(request):
    """
    알림톡/친구톡에 대한 전송결과를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 요청시 반환받은 접수번호
        receiptNum = "018030511103200001"

        kakaoInfo = kakaoService.getMessages(CorpNum, receiptNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessagesRN(request):
    """
    전송요청번호(requestNum)를 할당한 알림톡/친구톡 전송내역 및 전송상태를 확인한다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 전송 요청시 반환받은 접수번호
        requestNum = "20180809151234"

        kakaoInfo = kakaoService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 시작일자, 날짜형식(yyyyMMdd)
        SDate = "20180301"

        # 종료일자, 날짜형식(yyyyMMdd)
        EDate = "20180312"

        # 전송상태 배열 [0-대기, 1-전송중, 2-성공, 3-대체 4-실패, 5-취소]
        State = ["1", "2", "3", "4", "5"]

        # 전송유형 [ATS(알림톡) / ATS(친구톡 텍스트) / FMS(친구톡 이미지)]
        Item = ["ATS", "ATS", "FMS"]

        # 예약전송 검색여부, [공백-전체조회, 0-즉시전송조회, 1-예약전송조회]
        ReserveYN = ""

        # 개인조회여부 [0-전체조회, 1-개인조회]
        SenderYN = "0"

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
        PerPage = 10

        # 정렬방향 [D-내림차순, A-오름차순]
        Order = "D"

        response = kakaoService.search(CorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page, PerPage, Order,
                                       UserID)

        return render(request, 'Kakao/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL_BOX(request):
    """
    카카오톡전송내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.

    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # PLUSFRIEND(플러스친구계정관리), SENDER(발신번호관리), TEMPLATE(알림톡템플릿관리), BOX(카카오톡전송내역)
        TOGO = "BOX"

        url = kakaoService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    알림톡/친구 전송단가를 확인합니다.
    """
    try:
        # 팝빌회원 아이디
        CorpNum = settings.testCorpNum

        # 전송유형 [ATS(알림톡), FTS(친구톡 텍스트), FMS(친구톡 이미지)]
        MsgType = "ATS"

        result = kakaoService.getUnitCost(CorpNum, MsgType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 알림톡,친구톡 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 전송유형 [ATS(알림톡), FTS(친구톡 텍스트), FMS(친구톡 이미지)]
        MsgType = "ATS"

        response = kakaoService.getChargeInfo(CorpNum, MsgType, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

    pass


def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - 과금방식이 파트너과금인 경우 파트너 잔여포인트(GetPartnerBalance API) 를 통해 확인하시기 바랍니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = kakaoService.getBalance(CorpNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopbillURL_CHRG(request):
    """
    팝빌 관련 팝업 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-연동회원 포인트충전
        TOGO = "CHRG"

        url = kakaoService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
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

        result = kakaoService.getPartnerBalance(CorpNum)

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

        url = kakaoService.getPartnerURL(CorpNum, TOGO)

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

        response = kakaoService.checkIsMember(CorpNum)

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

        response = kakaoService.checkID(memberID)

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

        response = kakaoService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getPopbillURL_LOGIN(request):
    """
    팝빌 관련 팝업 URL을 반환합니다. (팝빌 로그인, 포인트충전)
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # LOGIN-팝빌 로그인, CHRG-포인트충전
        TOGO = "LOGIN"

        url = kakaoService.getPopbillURL(CorpNum, UserID, TOGO)

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

        response = kakaoService.registContact(CorpNum, newContact, UserID)

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

        listContact = kakaoService.listContact(CorpNum, UserID)

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

        response = kakaoService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

        response = kakaoService.getCorpInfo(CorpNum, UserID)

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

        response = kakaoService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
