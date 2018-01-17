####
popbill.sdk.example.django
####
================================
팝빌 API Example for Django.
================================

* requirements

  * Python 2.7+
  * Django 1.11+
  * popbill [ https://github.com/linkhub-sdk/]


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