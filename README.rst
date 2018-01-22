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


* Python versions available in Django

+------------------+---------------------+
|  Django version  |   Python versions   |
+==================+=====================+
| 1.11             | 2.7, 3.4, 3.5, 3.6  |
+------------------+---------------------+
| 2.0              | 3.4, 3.5, 3.6       |
+------------------+---------------------+
| 2.1              | 3.5, 3.6, 3.7       |
+------------------+---------------------+

* install pip by
::

    $ pip install -r requirements.txt

* how to test ?

  * modify config/settings.py with LinkID/SecretKey issued by Linkhub.
  * And test with console like...

::

    $ python manage.py runserver

* Visit localhost:8000 in your web browser


* 매뉴얼 목차
    ..[1] 전자세금계산서 API
    ..[2] 전자명세서 API
    ..[3] 현금영수증 API
    ..[4] 문자메시지 API
    ..[5] 팩스 API
    ..[6] 홈택스 전자(세금)계산서 연계 API
    ..[7] 홈택스 현금영수증 연계 API
    ..[8] 휴폐업조회 API


`링크허브(Linkhub) <https://www.linkhub.co.kr/>`_.
`팝빌(Popbill) <https://www.popbill.com/>`_.