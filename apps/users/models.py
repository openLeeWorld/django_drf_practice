from __future__ import annotations

from functools import cached_property
# 클래스의 속성을 캐싱할 때 사용함
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Model, QuerySet
from django_stubs_ext.db.models import TypedModelMeta
from rest_framework import status
from rest_framework.exceptions import APIException


class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "도메인 로직상 문제 발생..."}
    default_code = "invalid"


class User(AbstractUser):
    # objects = UserManager() 기본값입니다.

    class UserStatus(models.TextChoices):
        ACTIVE = "active", "활성화"
        DORMANT = "dormant", "휴면"
        SUSPENSION = "suspension", "정지"

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "고객"
        OWNER = "store_owner", "사장님"
        STAFF = "staff", "직원"

    user_type = models.CharField(
        db_comment="고객 유형",
        default=UserType.CUSTOMER,
        max_length=16,
        choices=UserType.choices,
    )
    phone = models.CharField(max_length=64, blank=True, db_comment="전화번호")
    name_kor = models.CharField(max_length=64, db_comment="회원 성함(한국어)")
    # registration_number = custom_fields.EncryptedField(
    #     max_length=custom_fields.encrypt_max_length(16),
    #     db_comment="주민등록번호",
    #     blank=True,
    # )

    department = models.ForeignKey(
        to="Department",
        db_comment="소속부서",
        null=True,
        on_delete=models.CASCADE,
    )

    @property # 메서드를 속성처럼 사용할 수 있음, 호출될 때마다 DB 접근할 때마다 실행됨
    def full_name(self) -> str:
        return self.last_name + self.first_name

    @cached_property # 메서드를 속성처럼 사용할 수 있음, 한 번 호출되고 캐시된 값 리턴함
    def owned_store_count(self) -> int:
        return self.store_set.count()

    # def has_welcome_coupon(self) -> None:
    #     if not # (실제 쿠폰을 가지고있는지 확인하는 로직) :
    #         raise DomainExcpetion({"message": "이미 해당 계정은 쿠폰을 가지고 있습니다."})
    #
    # def check_already_use_welcome_coupon(self)-> bool:
    #     if not  # (이미 쿠폰을 사용했는지 확인하는 로직) :
    #         raise DomainExcpetion({"message": "이미 쿠폰을 사용했습니다."})

    class Meta(TypedModelMeta):
        db_table = "user"


class StoreOwner(User):
    @property
    def has_multi_store(self) -> bool:
        """
        상점 여러개 소유한 사장님인가?
        """

        return True

    class Meta:
        proxy = True


class Customer(User):
    @property
    def is_init_user(self) -> bool:
        """
        아직 첫 주문을 완료하지 않은 고객인가?
        """
        return False

    class Meta:
        proxy = True


class StaffManager(UserManager["Staff"]):
    def get_queryset(self) -> QuerySet["Staff"]:
        return super().get_queryset().filter(user_type=User.UserType.STAFF.value)


class Staff(User):
    objects = StaffManager()

    class Meta(TypedModelMeta):
        proxy = True


class Department(models.Model):
    parent1_name = models.CharField(max_length=32, db_comment="최상위 소속 부서명")
    parent2_name = models.CharField(max_length=32, db_comment="중간 소속 부서명")
    parent3_name = models.CharField(max_length=32, db_comment="상세 소속 부서명")

    def __str__(self): # str(department)시 호출됨
        return f"{self.parent1_name}>{self.parent2_name}>{self.parent3_name}"

    class Meta:
        db_table = "department"