# -*- coding: utf-8 -*-
from django.shortcuts import render
from popbill import FaxService, PopbillException, ContactInfo, JoinForm, FaxReceiver, CorpInfo

from config import settings

# config/settings.py 작성한 LinkID, SecretKey를 이용해 FaxService 객체 생성
faxService = FaxService(settings.LinkID, settings.SecretKey)

# 연동환경 설정값, 개발용(True), 상업용(False)
faxService.IsTest = settings.IsTest


def index(request):
    return render(request, 'Fax/Index.html', {})


def getURL_SENDER(request):
    """
    팩스 전송내역 / 발신번호 관리 팝업 URL을 반환합니다.
    - 보안정책에 따라 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # BOX-팩스 전송내역 팝업, SENDER-발신번호 관리 팝업
        TOGO = "SENDER"

        url = faxService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getSenderNumberList(request):
    """
    등록된 팩스 발신번호 목록을 확인합니다.
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
    팩스를 전송합니다. (전송할 파일 개수는 최대 5개까지 가능)
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

        # 예약전송일시, None처리시 즉시전송, 작성형태 'yyyyMMddHHmmss'
        ReserveDT = None

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
    팩스를 동보전송 합니다.
    - 동보전송은 한 송신측이 다른 수신단말기를 지정하여 같은 내용을 동시에
      전송하는 것을 말합니다.
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

        # 예약전송시간, None처리시 즉시전송, 작성형태 'yyyyMMddHHmmss'
        ReserveDT = None

        # 팩스제목
        Title = "Python 팩스동보전송 제목"

        Receivers = []  # 수신정보 배열, 최대 1000개
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


def resendFAX(request):
    """
    팩스를 재전송합니다.
    - 전송일기준 180일이 경과되지 않은 팩스전송건만 재전송할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스 접수번호
        ReceiptNum = "018012215343900001"

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ""

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = "발신자명"

        # 수신번호/수신자명 모두 공백처리시 기존전송정보로 재전송
        # 수신번호
        Receiver = ""

        # 수신자명
        ReceiverName = ''

        # 예약전송시간, 공백시 즉시전송, 작성형태 yyyyMMddHHmmss
        ReserveDT = ''

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
    - 전송일로부터 180일이 경과된 경우 재전송할 수 없습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 팩스전송 문서 파일포맷 안내 : http://blog.linkhub.co.kr/2561
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = '20180912105825'

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = '07043042991'

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = '발신자명'

        # 수신번호/수신자명 모두 공백처리시 기존전송정보로 재전송
        # 수신번호
        Receiver = ''

        # 수신자명
        ReceiverName = ''

        # 예약전송시간, 공백시 즉시전송, 작성형태 yyyyMMddHHmmss
        ReserveDT = ''

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
    팩스를 재전송합니다.
    - 전송일기준 180일이 경과되지 않은 팩스전송건만 재전송할 수 있습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 팩스 접수번호
        ReceiptNum = "018012215401700001"

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = ""

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = "발신자명"

        # 예약전송시간, 공백시 즉시전송, 작성형태 yyyyMMddHHmmss
        ReserveDT = ""

        # 수신정보 배열 None 처리시 기존전송정보로 전송
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
    전송요청번호(requestNum)을 할당한 팩스를 재전송합니다.
    - 전송일로부터 180일이 경과된 경우 재전송할 수 없습니다.
    - 팩스 재전송 요청시 포인트가 차감됩니다. (전송실패시 환불처리)
    - 팩스전송 문서 파일포맷 안내 : http://blog.linkhub.co.kr/2561
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # 원본 팩스 전송시 할당한 전송요청번호
        OrgRequestNum = '20180912105825'

        # 발신번호, 공백처리시 기존전송정보로 재전송
        Sender = '07043042991'

        # 발신자명, 공백처리시 기존전송정보로 재전송
        SenderName = '발신자명'

        # 예약전송시간, 공백시 즉시전송, 작성형태 yyyyMMddHHmmss
        ReserveDT = ''

        # 수신정보 배열 None 처리시 기존전송정보로 전송
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
    예약전송 팩스요청건을 취소합니다.
    - 예약전송 취소는 예약전송시간 10분전까지 가능합니다.
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
    - 예약전송 취소는 예약전송시간 10분전까지 가능합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 예약팩스전송 요청시 할당한 전송요청번호
        requestNum = "20180912-004"

        response = faxService.cancelReserveRN(CorpNum, requestNum)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFaxDetail(request):
    """
    팩스 전송요청시 반환받은 접수번호(receiptNum)을 사용하여 팩스전송
    결과를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송 요청시 반환받은 접수번호 (receiptNum)
        receiptNum = "018012914050700001"

        resultList = faxService.getFaxResult(CorpNum, receiptNum)

        return render(request, 'Fax/GetFaxDetail.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getFaxDetailRN(request):
    """
    팩스전송요청시 할당한 전송요청번호(requestNum)으로 전송결과를 확인합니다
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팩스전송요청시 할당한 전송요청번호 (requestNum)
        requestNum = "20180809162125"

        resultList = faxService.getFaxResultRN(CorpNum, requestNum)

        return render(request, 'Fax/GetFaxDetail.html', {'resultList': resultList})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def search(request):
    """
    검색조건을 사용하여 팩스전송 내역을 조회합니다.
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

        # 팩스전송상태 배열, [1-대기 / 2-성공 / 3-실패 / 4-취소]
        State = ["1", "2", "3", "4"]

        # 예약전송 검색여부, [True-예약전송건 조회 / False-전체조회]
        ReserveYN = False

        # 개인조회 여부, [True-개인조회 / False-회사조회]
        SenderOnly = False

        # 페이지 번호
        Page = 1

        # 페이지당 목록갯수, 기본값 500
        PerPage = 10

        # 정렬방향, [D-내림차순 / A-오름차순]
        Order = "D"

        response = faxService.search(CorpNum, SDate, EDate, State, ReserveYN, SenderOnly,
                                     Page, PerPage, Order, UserID)

        return render(request, 'Fax/Search.html', {'response': response})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getURL_BOX(request):
    """
    팩스 전송내역 목록/발신번호 관리 팝업 URL을 반환합니다.
    - 보안정책으로 인해 반환된 URL은 30초의 유효시간을 갖습니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        # BOX-팩스 전송내역 목록 팝업, SENDER-발신번호 관리 팝업
        TOGO = "BOX"

        url = faxService.getURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
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

        url = faxService.getPopbillURL(CorpNum, UserID, TOGO)

        return render(request, 'url.html', {'url': url})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getChargeInfo(request):
    """
    연동회원의 팩스 API 서비스 과금정보를 확인합니다.
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        # 팝빌회원 아이디
        UserID = settings.testUserID

        response = faxService.getChargeInfo(CorpNum, UserID)

        return render(request, 'getChargeInfo.html',
                      {'unitCost': response.unitCost, 'chargeMethod': response.chargeMethod,
                       'rateSystem': response.rateSystem})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


def getUnitCost(request):
    """
    팩스 전송단가를 확인합니다.
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
    """
    try:
        # 팝빌회원 사업자번호
        CorpNum = settings.testCorpNum

        result = faxService.getBalance(CorpNum)

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

        result = faxService.getPartnerBalance(CorpNum)

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

        url = faxService.getPartnerURL(CorpNum, TOGO)

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

        response = faxService.checkIsMember(CorpNum)

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

        response = faxService.checkID(memberID)

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

        response = faxService.joinMember(newMember)

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

        # LOGIN-팝빌 로그인, CHRG-연동회원 포인트충전
        TOGO = "LOGIN"

        url = faxService.getPopbillURL(CorpNum, UserID, TOGO)

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

        response = faxService.registContact(CorpNum, newContact, UserID)

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

        listContact = faxService.listContact(CorpNum, UserID)

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

        response = faxService.updateCorpInfo(CorpNum, corpInfo, UserID)

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

        response = faxService.getCorpInfo(CorpNum, UserID)

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

        response = faxService.updateContact(CorpNum, updateInfo, UserID)

        return render(request, 'response.html', {'code': response.code, 'message': response.message})
    except PopbillException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
