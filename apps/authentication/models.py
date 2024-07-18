from django.db import models

# Create your models here.
"""
인증 로직의 경우
대부분 rest_framework_simplejwt의 구현체 (RefreshToken, Token)을 사용하였기 때문에
다시 구현할 model은 없음
from rest_framework_simplejwt.tokens import RefreshToken, Token 모델 참조
"""