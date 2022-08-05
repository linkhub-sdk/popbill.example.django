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

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
kakaoService.UseStaticIP = settings.UseStaticIP

#로컬시스템 시간 사용여부, 권장(True)
kakaoService.UseLocalTimeYN = settings.UseLocalTimeYN

# 알림톡/친구톡 전송하기 위해 발신번호 사전등록을 합니다. (등록방법은 사이트/API 두가지 방식이 있습니다.)
# 1. 팝빌 사이트 로그인 > [문자/팩스] > [카카오톡] > [발신번호 사전등록] 메뉴에서 등록
# 2. getSenderNumberMgtURL API를 통해 반환된 URL을 이용하여 발신번호 등록

def index(request):
    return render(request, 'Kakao/Index.html', {})

def getPlusFriendMgtURL(request):
    """
    카카오톡 채널을 등록하고 내역을 확인하는 카카오톡 채널 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetPlusFriendMgtURL
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
    팝빌에 등록한 연동회원의 카카오톡 채널 목록을 확인합니다.
    - https://docs.popbill.com/kakao/python/api#ListPlusFriendID
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = kakaoService.listPlusFriendID(CorpNum)

        return render(request, 'Kakao/ListPlusFriendID.html', {'listPlusFriendID': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkSenderNumber(request):
    '''
    카카오톡 발신번호 등록여부를 확인합니다.
    - 발신번호 상태가 '승인'인 경우에만 리턴값 'Response'의 변수 'code'가 1로 반환됩니다.
    - https://docs.popbill.com/kakao/python/api#CheckSenderNumber
    '''

    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 확인할 발신번호
        senderNumber = ""

        response = kakaoService.checkSenderNumber(CorpNum, senderNumber)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getSenderNumberMgtURL(request):
    """
    발신번호를 등록하고 내역을 확인하는 카카오톡 발신번호 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetSenderNumberMgtURL
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
    팝빌에 등록한 연동회원의 카카오톡 발신번호 목록을 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetSenderNumberList
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
    알림톡 템플릿을 신청하고 승인심사 결과를 확인하며 등록 내역을 확인하는 알림톡 템플릿 관리 페이지 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - 승인된 알림톡 템플릿은 수정이 불가하고, 변경이 필요한 경우 새롭게 템플릿 신청을 해야합니다.
    - https://docs.popbill.com/kakao/python/api#GetATSTemplateMgtURL
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

def getATSTemplate(request):
    """
    승인된 알림톡 템플릿의 정보를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetATSTemplate
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        #템플릿 코드
        templateCode = "021010000076"

        templateInfo = kakaoService.getATSTemplate(CorpNum, templateCode)

        return render(request, 'Kakao/GetATSTemplateS.html', {'templateInfo' : templateInfo })
    except PopbillException as PE :
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listATStemplate(request):
    """
    승인된 알림톡 템플릿 목록을 확인합니다.
    - https://docs.popbill.com/kakao/python/api#ListATSTemplate
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        templateList = kakaoService.listATSTemplate(CorpNum)

        return render(request, 'Kakao/ListATSTemplate.html', {'templateList': templateList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendATS_one(request):
    """
    승인된 템플릿의 내용을 작성하여 1건의 알림톡 전송을 팝빌에 접수합니다.
    - 전송실패시 사전에 지정한 변수 'AltSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendATS_one
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 승인된 알림톡 템플릿코드
        # └ 알림톡 템플릿 관리 팝업 URL(GetATSTemplateMgtURL API) 함수, 알림톡 템플릿 목록 확인(ListATStemplate API) 함수를 호출하거나
        #   팝빌사이트에서 승인된 알림톡 템플릿 코드를  확인 가능.
        templateCode = "019020000163"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # 대체문자 유형(altSendType)이 "A"일 경우, 대체문자로 전송할 내용 (최대 2000byte)
        # └ 팝빌이 메시지 길이에 따라 단문(90byte 이하) 또는 장문(90byte 초과)으로 전송처리
        altContent = "알림톡 대체 문자"

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신번호
        receiver = ""

        # 수신자 이름
        receiverName = "partner"

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
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
                                            altSendType, sndDT, receiver, receiverName, UserID, requestNum, btns, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendATS_multi(request):
    """
    승인된 템플릿의 내용을 작성하여 다수건의 알림톡 전송을 팝빌에 접수하며, 수신자 별로 개별 내용을 전송합니다. (최대 1,000건)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendATS_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 승인된 알림톡 템플릿코드
        # └ 알림톡 템플릿 관리 팝업 URL(GetATSTemplateMgtURL API) 함수, 알림톡 템플릿 목록 확인(ListATStemplate API) 함수를 호출하거나
        #   팝빌사이트에서 승인된 알림톡 템플릿 코드를  확인 가능.
        templateCode = "019020000163"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        # - 수신정보 배열에 대체문자 제목이 입력되지 않은 경우 적용.
        # - 모든 수신자에게 다른 제목을 보낼 경우 altsjt 를 이용.
        altSubject = "대체문자 제목"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",  # 수신번호
                    rcvnm="linkhub",  # 수신자 이름
                    msg=content,  # 알림톡 내용 (최대 400자)

                    # 대체문자 제목
                    # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
                    # - 모든 수신자에게 동일한 제목을 보낼 경우 배열의 모든 원소에 동일한 값을 입력하거나
                    #   값을 입력하지 않고 altSubject 를 이용
                    altsjt="(알림톡 대체문자 제목) [링크허브]",

                    # 대체문자 내용 (최대 2000byte)
                    altmsg="(알림톡 대체문자) 안녕하세요 링크허브입니다.",

                    interOPRefKey ="2021-"+str(x), # 파트너 지정키, 수신자 구분용 메모
                )
            )

            # 수신자별 개별 버튼내용 전송하는 경우
            # 개별 버튼의 개수는 템플릿 신청 시 승인받은 버튼의 개수와 동일하게 생성, 다를 경우 전송실패 처리
            # 버튼링크URL에 #{템플릿변수}를 기재하여 승인받은 경우 URL 수정가능.
            # 버튼명 , 버튼 유형 수정 불가능.

            # #개별 버튼정보 리스트 생성
            # btns = []
            # # # 수신자별 개별 전송할 버튼 정보
            # btns.append(
            #     KakaoButton(
            #         n="템플릿 안내",  # 버튼명
            #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
            #         u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
            #         u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
            #     )
            # )
            # btns.append(
            #     KakaoButton(
            #         n="버튼명",  # 버튼명
            #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
            #         u1="https://www.popbill" + str(x) + ".com",  # [앱링크-iOS, 웹링크-Mobile]
            #         u2="https://www.popbill" + str(x) + ".com"  # [앱링크-Android, 웹링크-PC URL]
            #     )
            # )
            # # 개별 버튼정보 리스트 수신정보에 추가
            # KakaoMessages[x].btns = btns

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        # 동일 버튼정보 리스트, 수신자별 동일 버튼내용 전송하는경우
        # 버튼링크URL에 #{템플릿변수}를 기재하여 승인받은 경우 URL 수정가능.
        # 버튼의 개수는 템플릿 신청 시 승인받은 버튼의 개수와 동일하게 생성, 다를 경우 전송실패 처리
        # 알림톡 버튼정보를 템플릿 신청시 기재한 버튼정보와 동일하게 전송하는 경우 btns를 빈 리스트 처리.
        btns = []
        # btns.append(
        #     KakaoButton(
                # n="템플릿 안내",  # 버튼명
                # t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
                # u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
                # u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
        #     )
        # )
        receiptNum = kakaoService.sendATS_multi(CorpNum, templateCode, snd, "", "",
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum, btns)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendATS_same(request):
    """
    승인된 템플릿 내용을 작성하여 다수건의 알림톡 전송을 팝빌에 접수하며, 모든 수신자에게 동일 내용을 전송합니다. (최대 1,000건)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendATS_same
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 승인된 알림톡 템플릿코드
        # └ 알림톡 템플릿 관리 팝업 URL(GetATSTemplateMgtURL API) 함수, 알림톡 템플릿 목록 확인(ListATStemplate API) 함수를 호출하거나
        #   팝빌사이트에서 승인된 알림톡 템플릿 코드를  확인 가능.
        templateCode = "019020000163"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 알림톡 내용 (최대 1000자)
        # 사전에 승인된 템플릿의 내용과 알림톡 전송내용(content)이 다를 경우 전송실패 처리됩니다.
        content = "[ 팝빌 ]\n"
        content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        content += "해당 템플릿으로 전송 가능합니다.\n\n"
        content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        content += "팝빌 파트너센터 : 1600-8536\n"
        content += "support@linkhub.co.kr"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "[테스트] 알림톡 대체 문자"

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",  # 수신번호
                    rcvnm="popbill",  # 수신자 이름
                    interOPRefKey="20220805" + str(x) # 파트너 지정키
                )
            )

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
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
                                                altSendType, sndDT, KakaoMessages, UserID, requestNum, btns, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFTS_one(request):
    """
    텍스트로 구성된 1건의 친구톡 전송을 팝빌에 접수합니다.
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendFTS_one
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 친구톡 내용 (최대 1000자)
        content = "친구톡 내용"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # 대체문자 유형(altSendType)이 "A"일 경우, 대체문자로 전송할 내용 (최대 2000byte)
        # └ 팝빌이 메시지 길이에 따라 단문(90byte 이하) 또는 장문(90byte 초과)으로 전송처리
        altContent = "대체문자 내용"

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신번호
        receiver = ""

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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS(CorpNum, plusFriendID, snd, content, altContent, altSendType, sndDT,
                                            receiver, receiverName, KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFTS_multi(request):
    """
    텍스트로 구성된 다수건의 친구톡 전송을 팝빌에 접수하며, 수신자 별로 개별 내용을 전송합니다. (최대 1,000건)
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendFTS_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        # - 수신정보 배열에 대체문자 제목이 입력되지 않은 경우 적용.
        # - 모든 수신자에게 다른 제목을 보낼 경우 altsjt 를 이용.
        altSubject = "대체문자 제목"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="0101234567",  # 수신번호
                    rcvnm="TESTER",  # 수신자 이름
                    msg="안녕하세요 " + str(x) + "님 링크허브입니다.",  # 친구톡 내용 (최대 1000자)

                    # 대체문자 제목
                    # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
                    # - 모든 수신자에게 동일한 제목을 보낼 경우 배열의 모든 원소에 동일한 값을 입력하거나
                    #   값을 입력하지 않고 altSubject 를 이용
                    altsjt="(친구톡 대체문자 제목) [링크허브]",

                    # 대체문자 내용 (최대 2000byte)
                    altmsg="(친구톡 대체문자) 안녕하세요 링크허브입니다.",

                    interOPRefKey="20220805-"+str(x)    # 파트너 지정키, 수신자 구별용 메모
                )
            )
            # 수신자별 개별 버튼내용 전송하는 경우
            # 버튼 목록 (최대 5개)

            # #개별 버튼정보 리스트 생성
            # btns = []
            # # 수신자별 개별 전송할 버튼 정보
            # btns.append(
            #     KakaoButton(
            #         n="템플릿 안내",  # 버튼명
            #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
            #         u1="https://www.popbill.com",  # [앱링크-iOS, 웹링크-Mobile]
            #         u2="http://www.popbill.com"  # [앱링크-Android, 웹링크-PC URL]
            #     )
            # )
            # btns.append(
            #     KakaoButton(
            #         n="버튼명",  # 버튼명
            #         t="WL",  # 버튼유형 [DS-배송조회, WL-웹링크, AL-앱링크, MD-메시지전달, BK-봇키워드]
            #         u1="https://www.popbill" + str(x) + ".com",  # [앱링크-iOS, 웹링크-Mobile]
            #         u2="https://www.popbill" + str(x) + ".com"  # [앱링크-Android, 웹링크-PC URL]
            #     )
            # )
            # # 개별 버튼정보 리스트 수신정보에 추가
            # KakaoMessages[x].btns = btns

        # 동일 버튼정보 리스트
        # 버튼내용을 전송하지 않는 경우 빈 리스트 처리
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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, "", "", altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFTS_same(request):
    """
    텍스트로 구성된 다수건의 친구톡 전송을 팝빌에 접수하며, 모든 수신자에게 동일 내용을 전송합니다. (최대 1,000건)
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - https://docs.popbill.com/kakao/python/api#SendFTS_same
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # [동보] 친구톡 내용 (최대 1000자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # [동보] 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",  # 수신번호
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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFTS_multi(CorpNum, plusFriendID, snd, content, altContent, altSendType,
                                                sndDT, KakaoMessages, KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFMS_one(request):
    """
    이미지가 첨부된 1건의 친구톡 전송을 팝빌에 접수합니다.
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - 대체문자의 경우, 포토문자(MMS) 형식은 지원하고 있지 않습니다.
    - https://docs.popbill.com/kakao/python/api#SendFMS_one
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 친구톡 내용 (최대 400자)
        content = "친구톡 내용"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # 대체문자 유형(altSendType)이 "A"일 경우, 대체문자로 전송할 내용 (최대 2000byte)
        # └ 팝빌이 메시지 길이에 따라 단문(90byte 이하) 또는 장문(90byte 초과)으로 전송처리
        altContent = "대체문자 내용"

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 첨부이미지 파일 경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        # └ 수신자가 친구톡 상단 이미지 클릭시 호출되는 URL
        # 미입력시 첨부된 이미지를 링크 기능 없이 표시
        imageURL = "http://www.linkhub.co.kr"

        # 수신번호
        receiver = ""

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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS(CorpNum, plusFriendID, snd, content, altContent,
                                            altSendType, sndDT, filePath, imageURL, receiver, receiverName,
                                            KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFMS_multi(request):
    """
    이미지가 첨부된 다수건의 친구톡 전송을 팝빌에 접수하며, 수신자 별로 개별 내용을 전송합니다. (최대 1,000건)
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - 대체문자의 경우, 포토문자(MMS) 형식은 지원하고 있지 않습니다.
    - https://docs.popbill.com/kakao/python/api#SendFMS_multi
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        # - 수신정보 배열에 대체문자 제목이 입력되지 않은 경우 적용.
        # - 모든 수신자에게 다른 제목을 보낼 경우 altsjt 를 이용.
        altSubject = "대체문자 제목"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 첨부이미지 파일 경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        # └ 수신자가 친구톡 상단 이미지 클릭시 호출되는 URL
        # 미입력시 첨부된 이미지를 링크 기능 없이 표시
        imageURL = "http://www.linkhub.co.kr"

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",  # 수신번호
                    rcvnm="",  # 수신자 이름
                    msg="안녕하세요 " + str(x) + "님 링크허브입니다.",  # 친구톡 내용 (최대 400자)

                    # 대체문자 제목
                    # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
                    # - 모든 수신자에게 동일한 제목을 보낼 경우 배열의 모든 원소에 동일한 값을 입력하거나
                    #   값을 입력하지 않고 altSubject 를 이용
                    altsjt="(친구톡 대체문자 제목) [링크허브]",

                    # 대체문자 내용 (최대 2000byte)
                    altmsg="(친구톡 대체문자) 안녕하세요 링크허브입니다.",

                    interOPRefKey="20220805-"+str(x)    # 파트너 지정키, 수신자 구별용 메모
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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, "", "",
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def sendFMS_same(request):
    """
    이미지가 첨부된 다수건의 친구톡 전송을 팝빌에 접수하며, 모든 수신자에게 동일 내용을 전송합니다. (최대 1,000건)
    - 친구톡의 경우 야간 전송은 제한됩니다. (20:00 ~ 익일 08:00)
    - 전송실패시 사전에 지정한 변수 'altSendType' 값으로 대체문자를 전송할 수 있고, 이 경우 문자(SMS/LMS) 요금이 과금됩니다.
    - 대체문자의 경우, 포토문자(MMS) 형식은 지원하고 있지 않습니다.
    - https://docs.popbill.com/kakao/python/api#SendFMS_same
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팝빌에 등록된 카카오톡 채널 아아디
        plusFriendID = "@팝빌"

        # 팝빌에 사전 등록된 발신번호
        snd = ""

        # [동보] 친구톡 내용 (최대 400자)
        content = "안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 제목
        # - 메시지 길이(90byte)에 따라 장문(LMS)인 경우에만 적용.
        altSubject = "대체문자 제목"

        # [동보] 대체문자 내용 (최대 2000byte)
        altContent = "(친구톡 대체문자) 안녕하세요 팝빌 플친님 파이썬입니다."

        # 대체문자 유형 (null , "C" , "A" 중 택 1)
        # null = 미전송, C = 알림톡과 동일 내용 전송 , A = 대체문자 내용(altContent)에 입력한 내용 전송
        altSendType = "A"

        # 예약전송시간, 작성형식:yyyyMMddHHmmss, 공백 기재시 즉시전송
        sndDT = ""

        # 첨부이미지 파일 경로
        # 이미지 전송규격 (jpg 포맷, 용량 최대 500KByte, 이미지 높이/너비 비율 1.333 이하, 1/2 이상)
        filePath = "./KakaoExample/static/image/test.jpg"

        # 이미지 링크 URL
        # └ 수신자가 친구톡 상단 이미지 클릭시 호출되는 URL
        # 미입력시 첨부된 이미지를 링크 기능 없이 표시
        imageURL = "http://www.linkhub.co.kr"

        # 수신정보 배열 (최대 1000개 가능)
        KakaoMessages = []
        for x in range(0, 10):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",  # 수신번호
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

        # 광고성 메시지 여부 ( true , false 중 택 1)
        # └ true = 광고 , false = 일반
        # - 미입력 시 기본값 false 처리
        adsYN = False

        # 전송요청번호
        # 팝빌이 접수 단위를 식별할 수 있도록 파트너가 부여하는 식별번호.
        # 1~36자리로 구성. 영문, 숫자, 하이픈(-), 언더바(_)를 조합하여 팝빌 회원별로 중복되지 않도록 할당.
        requestNum = ""

        receiptNum = kakaoService.sendFMS_multi(CorpNum, plusFriendID, snd, content, altContent,
                                                altSendType, sndDT, filePath, imageURL, KakaoMessages,
                                                KakaoButtons, adsYN, UserID, requestNum, altSubject)

        return render(request, 'Kakao/ReceiptNum.html', {'receiptNum': receiptNum})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def cancelReserve(request):
    """
    팝빌에서 반환받은 접수번호를 통해 예약접수된 카카오톡을 전송 취소합니다. (예약시간 10분 전까지 가능)
    - https://docs.popbill.com/kakao/python/api#CancelReserve
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
    파트너가 할당한 전송요청 번호를 통해 예약접수된 카카오톡을 전송 취소합니다. (예약시간 10분 전까지 가능)
    - https://docs.popbill.com/kakao/python/api#CancelReserveRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약전송 요청시 할당한 전송요청번호(requestNum)
        requestNum = ""

        result = kakaoService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getMessages(request):
    """
    팝빌에서 반환받은 접수번호를 통해 알림톡/친구톡 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetMessages
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 요청시 반환받은 접수번호
        receiptNum = "020072814430000001"

        kakaoInfo = kakaoService.getMessages(CorpNum, receiptNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getMessagesRN(request):
    """
    파트너가 할당한 전송요청 번호를 통해 알림톡/친구톡 전송상태 및 결과를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetMessagesRN
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 알림톡/친구톡 전송 요청시 할당한 전송요청번호(requestNum)
        requestNum = ""

        kakaoInfo = kakaoService.getMessagesRN(CorpNum, requestNum)

        return render(request, 'Kakao/GetMessages.html', {'kakaoInfo': kakaoInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def search(request):
    """
    검색조건을 사용하여 알림톡/친구톡 전송 내역을 조회합니다. (조회기간 단위 : 최대 2개월)
    - 카카오톡 접수일시로부터 6개월 이내 접수건만 조회할 수 있습니다.
    - https://docs.popbill.com/kakao/python/api#Search
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

        # 전송상태 배열 ("0" , "1" , "2" , "3" , "4" , "5" 중 선택, 다중 선택 가능)
        # └ 0 = 전송대기 , 1 = 전송중 , 2 = 전송성공 , 3 = 대체문자 전송 , 4 = 전송실패 , 5 = 전송취소
        # - 미입력 시 전체조회
        State = ["0", "1", "2", "3", "4", "5"]

        # 검색대상 배열 ("ATS", "FTS", "FMS" 중 선택, 다중 선택 가능)
        # └ ATS = 알림톡 , FTS = 친구톡(텍스트) , FMS = 친구톡(이미지)
        # - 미입력 시 전체조회
        Item = ["ATS", "FTS", "FMS"]

        # 전송유형별 조회 (null , "0" , "1" 중 택 1)
        # └ null = 전체 , 0 = 즉시전송건 , 1 = 예약전송건
        # - 미입력 시 전체조회
        ReserveYN = "0"

        # 사용자권한별 조회 (true / false 중 택 1)
        # └ false = 접수한 카카오톡 전체 조회 (관리자권한)
        # └ true = 해당 담당자 계정으로 접수한 카카오톡만 조회 (개인권한)
        # 미입력시 기본값 false 처리
        SenderYN = "0"

        # 페이지 번호
        Page = 1

        # 페이지당 목록개수
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
    카카오톡 전송내역을 확인하는 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetSentListURL
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

def getBalance(request):
    """
    연동회원의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetBalance
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
    연동회원 포인트 충전을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetChargeURL
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

def getPaymentURL(request):
    """
    연동회원 포인트 결제내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetPaymentURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getPaymentURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getUseHistoryURL(request):
    """
    연동회원 포인트 사용내역 확인을 위한 페이지의 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetUseHistoryURL
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        url = kakaoService.getUseHistoryURL(CorpNum, UserID)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getPartnerBalance(request):
    """
    파트너의 잔여포인트를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetPartnerBalance
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
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetPartnerURL
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

def getUnitCost(request):
    """
    카카오톡 전송시 과금되는 포인트 단가를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetUnitCost
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 카카오톡 전송유형 : ATS / FTS / FMS 중 택 1
        # └ ATS = 알림톡, FTS = 친구톡(텍스트) , FMS = 친구톡(이미지)
        MsgType = "ATS"

        result = kakaoService.getUnitCost(CorpNum, MsgType)

        return render(request, 'result.html', {'result': result})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getChargeInfo(request):
    """
    팝빌 카카오톡 API 서비스 과금정보를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetChargeInfo
    """
    try:
        # 팝빌회원 사업자번호 (하이픈 '-' 제외 10자리)
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 카카오톡 전송유형 : ATS / FTS / FMS 중 택 1
        # └ ATS = 알림톡, FTS = 친구톡(텍스트) , FMS = 친구톡(이미지)
        MsgType = "ATS"

        response = kakaoService.getChargeInfo(CorpNum, MsgType)

        return render(request, 'getChargeInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def checkIsMember(request):
    """
    사업자번호를 조회하여 연동회원 가입여부를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#CheckIsMember
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
    사용하고자 하는 아이디의 중복여부를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#CheckID
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
    사용자를 연동회원으로 가입처리합니다.
    - https://docs.popbill.com/kakao/python/api#JoinMember
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

        response = kakaoService.joinMember(newMember)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getAccessURL(request):
    """
    팝빌에 로그인 상태로 접근할 수 있는 팝업 URL을 반환합니다.
    - 반환되는 URL은 보안 정책상 30초 동안 유효하며, 시간을 초과한 후에는 해당 URL을 통한 페이지 접근이 불가합니다.
    - https://docs.popbill.com/kakao/python/api#GetAccessURL
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

def getCorpInfo(request):
    """
    연동회원의 회사정보를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetCorpInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        response = kakaoService.getCorpInfo(CorpNum)

        return render(request, 'getCorpInfo.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateCorpInfo(request):
    """
    연동회원사의 회사정보를 수정 합니다.
    - https://docs.popbill.com/kakao/python/api#UpdateCorpInfo
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

        response = kakaoService.updateCorpInfo(CorpNum, corpInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def registContact(request):
    """
    연동회원 사업자번호에 담당자(팝빌 로그인 계정)를 추가합니다.
    - https://docs.popbill.com/kakao/python/api#RegistContact
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

        response = kakaoService.registContact(CorpNum, newContact)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def getContactInfo(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 정보를 확인합니다.
    - https://docs.popbill.com/kakao/python/api#GetContactInfo
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 담당자 아이디
        contactID = 'testkorea'

        contactInfo = kakaoService.getContactInfo(CorpNum, contactID)

        return render(request, 'getContactInfo.html', {'contactInfo' : contactInfo})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def listContact(request):
    """
    연동회원 사업자번호에 등록된 담당자(팝빌 로그인 계정) 목록을 확인합니다.
    - https://docs.popbill.com/kakao/python/api#ListContact
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        listContact = kakaoService.listContact(CorpNum)

        return render(request, 'listContact.html', {'listContact': listContact})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

def updateContact(request):
    """
    연동회원의 담당자 정보를 수정합니다.
    - https://docs.popbill.com/kakao/python/api#UpdateContact
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

        response = kakaoService.updateContact(CorpNum, updateInfo)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
