# -*- coding: utf-8 -*-
import os
import sys
import imp

imp.reload(sys)
try:
    sys.setdefaultencoding('UTF8')
except Exception as E:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '20m4&@*!_u)h1^atg_zbi+%^bw#d+rb)0&d&%e8)4oc-h@6j)2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = '*'

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TaxinvoiceExample',  # 전자세금계산서
    'StatementExample',  # 전자명세서
    'CashbillExample',  # 현금영수증
    'MessageExample',  # 문자
    'FaxExample',  # 팩스
    'HTTaxinvoiceExample',  # 홈택스 전자(세금)계산서 연계
    'HTCashbillExample',  # 홈택스 현금영수증 연계
    'ClosedownExample',  # 휴폐업조회
    'KakaoExample'  # 카카오톡
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Project level static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

"""
 - Django SDK 연동환경 설정방법 안내 : http://blog.linkhub.co.kr/
 - 업데이트 일자 : 2018-01-16
 - 연동 기술지원 연락처 : 1600-9854 / 070-4304-2991
 - 연동 기술지원 이메일 : code@linkhub.co.kr

 <테스트 연동개발 준비사항>
 1) 링크아이디(LinkID)와 비밀키(SecretKey)를
    링크허브 가입시 메일로 발급받은 인증정보를 참조하여 변경합니다.
 2) 팝빌 개발용 사이트(test.popbill.com)에 연동회원으로 가입합니다.
 
 * [전자세금계산서]를 발행하기 위해서는 공인인증서를 등록하셔야합니다.
    - 팝빌사이트 로그인 > [전자세금계산서] > [환경설정] > [공인인증서 관리]
    - 공인인증서 등록 팝업 URL (GetPopbillURL API)을 이용하여 등록
"""
# 링크아이디
LinkID = "TESTER"

# 발급받은 비밀키, 유출에 주의하시기 바랍니다.
SecretKey = "SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I="

# 연동환경 설정값, 개발용(True), 상업용(False)
IsTest = True

# 팝빌회원 사업자번호
testCorpNum = "1234567890"

# 팝빌회원 아아디
testUserID = "testkorea"
