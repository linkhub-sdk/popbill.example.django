####
popbill.sdk.example.django
####
================================
팝빌 API Example for Django.
================================

* requirements

  * Python 2.7+
  * Django 2.2+
  * popbill [ https://github.com/linkhub-sdk/popbill.py ]

* install pip by

::

    $ pip install -r requirements.txt

* ..or install easy_install by

::

    $ easy_install popbill django==1.11

how to test ?
------------------------------
* modify config/settings.py with LinkID/SecretKey issued by Linkhub.
* And test with console like...

::

    $ python manage.py runserver

* Visit localhost:8000 in your web browser


연동 API 목차
------------------------------
* 전자세금계산서 API 연동가이드
* 현금영수증 API
* 전자명세서 API
* 홈택스수집 전자세금계산서 API
* 홈택스수집 현금영수증 API
* 사업자등록상태조회 (휴폐업조회) API
* 기업정보조회 API
* 계좌조회 API
* 예금주조회 API
* 카카오톡 API
* 문자메시지 API
* 팩스 API

사이트
-------------------------------
`링크허브(Linkhub) <https://www.linkhub.co.kr/>`_,
`팝빌(Popbill) <https://www.popbill.com/>`_,
`팝빌 테스트배드(Test Popbill) <https://www.test.popbill.com/>`_,
