# -*- coding: utf-8 -*-
"""
업데이트 일자 : 2025-08-05
연동 기술지원 연락처 : 1600-9854
연동 기술지원 이메일 : code@linkhubcorp.com

<테스트 연동개발 준비사항>
1) API Key 변경 (연동신청 시 메일로 전달된 정보)
    - LinkID : 링크허브에서 발급한 링크아이디
    - SecretKey : 링크허브에서 발급한 비밀키
2) SDK 환경설정 옵션 설정
    - IsTest : 연동환경 설정, true-테스트, false-운영(Production), (기본값:true)
    - IPRestrictOnOff : 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
    - UseStaticIP : 통신 IP 고정, true-사용, false-미사용, (기본값:false)
    - UseLocalTimeYN : 로컬시스템 시간 사용여부, true-사용, false-미사용, (기본값:true)
"""
import imp
import os
import sys

imp.reload(sys)
try:
    sys.setdefaultencoding("UTF8")
except Exception as E:
    pass

# 링크아이디
LinkID = "TESTER"

# 비밀키
SecretKey = "SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I="

# 연동환경 설정, true-테스트, false-운영(Production), (기본값:true)
IsTest = True

# 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
IPRestrictOnOff = True

# 통신 IP 고정, true-사용, false-미사용, (기본값:false)
UseStaticIP = False

# 로컬시스템 시간 사용여부, true-사용, false-미사용, (기본값:true).
UseLocalTimeYN = True

# 팝빌회원 사업자번호
testCorpNum = "1234567890"

# 팝빌회원 아아디
testUserID = "testkorea"


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "20m4&@*!_u)h1^atg_zbi+%^bw#d+rb)0&d&%e8)4oc-h@6j)2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = "*"

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "TaxinvoiceExample",  # 전자세금계산서
    "StatementExample",  # 전자명세서
    "CashbillExample",  # 현금영수증
    "MessageExample",  # 문자
    "FaxExample",  # 팩스
    "HTTaxinvoiceExample",  # 홈택스 전자(세금)계산서 연동
    "HTCashbillExample",  # 홈택스 현금영수증 연동
    "ClosedownExample",  # 사업자등록상태조회
    "BizInfoCheckExample",  # 기업정보조회
    "KakaoExample",  # 카카오톡(알림톡/친구톡)
    "EasyFinBankExample",  # 계좌조회
    "AccountCheckExample",  # 예금주조회
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Internationalization
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Project level static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
