####
popbill.sdk.example.django
####
================================
팝빌 API Example for Django.
================================

* requirements

  * Python 2.7+
  * Django 1.11+
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
* 전자세금계산서 API 연동가이드 `<https://linkhub.tistory.com/146/>`_
* 전자명세서 API
* 현금영수증 API
* 문자메시지 API
* 팩스 API
* 홈택스 전자(세금)계산서 연계 API
* 홈택스 현금영수증 연계 API
* 휴폐업조회 API
* 카카오톡 API
* 계좌조회 API
* 예금주조회 API

사이트
-------------------------------
`링크허브(Linkhub) <https://www.linkhub.co.kr/>`_,
`팝빌(Popbill) <https://www.popbill.com/>`_,
`팝빌 테스트배드(Test Popbill) <https://www.test.popbill.com/>`_,
