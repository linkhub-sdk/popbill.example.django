# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import PopbillException, ContactInfo, CorpInfo, JoinForm, KakaoService, KakaoReceiver, \
    KakaoButton

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 KakaoService 객체 생성
kakaoService = KakaoService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
kakaoService.IsTest = settings.IsTest

# 인증토큰 IP제한기능 사용여부, 권장(True)
kakaoService.IPRestrictOnOff = settings.IPRestrictOnOff

# 친구톡/알림톡 전송하기 위해 발신번호 사전등록을 합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌 사이트 로그인 > [문자/팩스] > [카카오톡] > [발신번호 사전등록] 메뉴에서 등록
# 2. getSenderNumberMgtURL API를 통해 반환된 URL을 이용하여 발신번호 등록

def index(request):
    return render(request, 'Kakao/Index.html', {})


def getPlusFriendMgtURL(request):
    """
    카카오톡 채널 계정관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getPlusFriendMgtURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listPlusFriendID(request):
    """
    팝빌에 등록된 카카오톡 채널 목록을 반환 합니다.
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


def getSenderNumberMgtURL(request):
    """
    발신번호 관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getSenderNumberMgtURL(CorpNum, UserID)

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


def getATSTemplateMgtURL(request):
    """
    알림톡 템플릿관리 URL을 반환합니다.
     - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getATSTemplateMgtURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def listATStemplate(request):
    """
    (주)카카오로 부터 승인된 알림톡 템플릿 목록을 확인 합니다.
    - 반환항목중 템플릿코드(templateCode)는 알림톡 전송시 사용됩니다.
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
    - 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿코드
        # 승인된 알림톡 템플릿 코드는 ListATStemplate API, GetATSTemplateMgtURL API, 혹은 팝빌사이트에서 확인이 가능합니다.
        templateCode = "019020000163"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # 대체문자 내용 (최대 2000byte)
        altContent = "알림톡 대체 문자"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신번호
        receiver = "01011122"

        # 수신자 이름
        receiverName = "partner"

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        # 알림톡 버튼정보를 템플릿 신청시 기재한 버튼정보와 동일하게 전송하는 경우 btns를 빈 배열로 처리.
        btns = []

        # 알림톡 버튼 URL에 #{템플릿변수}를 기재한경우 템플릿변수 값을 변경하여 버튼정보 구성
        #btns.append(
        #     KakaoButton(
        #         n="템플릿 안내",  # 버튼명
        #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
        #         u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
        #         u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
        #    )
        #)

        receiptNum = kakaoService.sendATS(CorpNum, templateCode, snd, content, altContent,
                                          altSendType, sndDT, receiver, receiverName, UserID, requestNum, btns)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendATS_multi(request):
    """
    [대량전송] 알림톡 전송을 요청합니다.
    - 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿 코드
        templateCode = "019020000163"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="010456456",  # 수신번호
                    rcvnm="linkhub",  # 수신자 이름
                    msg=content,  # 알림톡 내용 (최대 1000자)
                    altmsg="수신번호 010-456-456 알림톡 대체문자"  # 대체문자 내용 (최대 2000byte)
                )
            )

        # 전송요청번호
        # 파트너가 전송 건에 대해 관리번호를 구성하여 관리하는 경우 사용.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        # 알림톡 버튼정보를 템플릿 신청시 기재한 버튼정보와 동일하게 전송하는 경우 btns를 빈 배열로 처리.
        btns = []

        # 알림톡 버튼 URL에 #{템플릿변수}를 기재한경우 템플릿변수 값을 변경하여 버튼정보 구성
        # btns.append(
        #     KakaoButton(
        #         n="템플릿 안내",  # 버튼명
        #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
        #         u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
        #         u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
        #     )
        # )
        receiptNum = kakaoService.sendATS_multi(CorpNum, templateCode, snd, "", "",
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum, btns)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendATS_same(request):
    """
    [동보전송] 알림톡 전송을 요청합니다.
    - 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 알림톡 템플릿 코드
        # 승인된 알림톡 템플릿 코드는 ListATStemplate API, GetATSTemplateMgtURL API, 혹은 팝빌사이트에서 확인이 가능합니다.
        templateCode = "019020000163"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "[테스트] 알림톡 대체 문자"

        # 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
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

        # 알림톡 버튼정보를 템플릿 신청시 기재한 버튼정보와 동일하게 전송하는 경우 btns를 빈 배열로 처리.
        btns = []

        # 알림톡 버튼 URL에 #{템플릿변수}를 기재한경우 템플릿변수 값을 변경하여 버튼정보 구성
        # btns.append(
        #     KakaoButton(
        #         n="템플릿 안내",  # 버튼명
        #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
        #         u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
        #         u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
        #     )
        # )

        receiptNum = kakaoService.sendATS_same(CorpNum, templateCode, snd, content, altContent,
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum, btns)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFTS_one(request):
    """
    친구톡(텍스트) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 친구톡 내용 (최대 1000자)
        content = "친구톡 내용"

        # 대체문자 내용 (최대 2000byte)
        altContent = "대체문자 내용"

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신번호
        receiver = "01012349876"

        # 수신자 이름
        receiverName = "partner"

        # 버튼 목록 (최대 5개)
        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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


def sendFTS_multi(request):
    """
    [대량전송] 친구톡(텍스트) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101234567",  # 수신번호
                    rcvnm="김현진",  # 수신자 이름
                    msg="안녕하세요 " + str(x) + "님 링크허브입니다.",  # 친구톡 내용 (최대 1000자)
                    altmsg="(친구톡 대체문자) 안녕하세요 링크허브입니다."  # 대체문자 내용 (최대 2000byte)
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, "", "", altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFTS_same(request):
    """
    [동보전송] 친구톡(텍스트) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # [동보] 친구톡 내용 (최대 1000자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101235678",  # 수신번호
                    rcvnm="팝친"  # 수신자 이름
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, content, altContent, altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFMS_one(request):
    """
    친구톡(이미지) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    - 이미지 전송규격 / jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 친구톡 내용 (최대 400자)
        content = "친구톡 내용"

        # 대체문자 내용 (최대 2000byte)
        altContent = "대체문자 내용"

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 파일경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        # 수신번호
        receiver = "01012345678"

        # 수신자 이름
        receiverName = "partner"

        # 버튼 목록 (최대 5개)
        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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


def sendFMS_multi(request):
    """
    [대량전송] 친구톡(이미지) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    - 이미지 전송규격 / jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 파일경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
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

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, "", "",
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def sendFMS_same(request):
    """
    [동보전송] 친구톡(이미지) 전송을 요청합니다.
    - 친구톡은 심야 전송(20:00~08:00)이 제한됩니다.
    - 이미지 전송규격 / jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 발신번호 (팝빌에 등록된 발신번호만 이용가능)
        snd = "07043042992"

        # [동보] 친구톡 내용 (최대 400자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 [공백-미전송, C-친구톡내용, A-대체문자내용]
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 파일경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        imageURL = "http://www.linkhub.co.kr"

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101235678",  # 수신번호
                    rcvnm="팝친"  # 수신자 이름
                )
            )

        # 버튼 목록 (최대 5개)
        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",  # 버튼명
                t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                u1="http://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
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

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, content, altContent,
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def cancelReserve(request):
    """
    알림톡/친구톡 전송요청시 발급받은 접수번호(receiptNum)로 예약전송건을 취소합니다.
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

        # 예약전송 요청시 할당한 전송요청번호(requestNum)
        requestNum = "20190116-001"

        result = kakaoService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessages(request):
    """
    알림톡/친구톡 전송요청시 발급받은 접수번호(receiptNum)로 전송결과를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 요청시 반환받은 접수번호
        receiptNum = "019012313433000001"

        kakaoInfo = kakaoService.getMessages(CorpNum, receiptNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getMessagesRN(request):
    """
    전송요청번호(requestNum)를 할당한 알림톡/친구톡 전송내역 및 전송상태를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 전송 요청시 할당한 전송요청번호(requestNum)
        requestNum = "20190123-123"

        kakaoInfo = kakaoService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 알림톡/친구톡 전송 내역을 조회합니다.
     - 최대 검색기간 : 6개월 이내
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

        # 전송상태 배열 [0-대기, 1-전송중, 2-성공, 3-대체 4-실패, 5-취소]
        State = ["1", "2", "3", "4", "5"]

        # 검색대상 [ATS(알림톡) / FTS(친구톡 텍스트) / FMS(친구톡 이미지)]
        Item = ["ATS", "FTS", "FMS"]

        # 예약전송 검색여부, [공백-전체조회, 0-즉시전송조회, 1-예약전송조회]
        ReserveYN = ""

        # 개인조회여부 [0-전체조회, 1-개인조회]
        SenderYN = "0"

        # 페이지 번호, 기본값 ‘1’
        Page = 1

        # 페이지당 검색개수, 기본값 500, 최대값 1000
        PerPage = 10

        # 정렬방향 [D-내림차순, A-오름차순]
        Order = "D"

        # 조회 검색어, 수신자명 기재
        QString = ""

        response = kakaoService.search(CorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page, PerPage, Order,
                                       UserID, QString)

        return render(request, 'Kakao/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSentListURL(request):
    """
    카카오톡전송내역 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getSentListURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    알림톡/친구톡 전송단가를 확인합니다.
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

        return render(request, 'getChargeInfo.html', {'response': response})
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

        url = kakaoService.getChargeURL(CorpNum, UserID)

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
    파트너 포인트 충전 URL을 반환합니다.
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

            # 아이디 (6자 이상 50자 미만)
            ID="join_id_test",

            # 비밀번호 (6자 이상 20자 미만)
            PWD="this_is_password",

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

        response = kakaoService.joinMember(newMember)

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

        url = kakaoService.getAccessURL(CorpNum, UserID)

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

            # 아이디 (6자 이상 50자 미만)
            id="popbill_test_id",

            # 비밀번호 (6자 이상 20자 미만)
            pwd="popbill_test_pwd",

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

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
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

        return render(request, 'getCorpInfo.html', {'response': response})
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

            # 회사조회 권한여부, True(회사조회) False(개인조회)
            searchAllAllowYN=True,

            # 관리자 권한여부, True(관리자), False(사용자)
            mgrYN=True
        )

        response = kakaoService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
