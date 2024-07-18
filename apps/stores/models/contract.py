from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from stores.models.store import Store
# 타입 힌트와 관련된 코드를 실행시점에 무시하고 타입 검사 도구에서만 인식하기 위해서 사용
# 타입 힌트를 위한 코드가 런타임에서 실행되지 않도록 함


class ContractManger(models.Manager):
    def current_valid(self, store: Store):  # 현재 유효한 계약
        today = date.today()
        return self.filter(start_date__gte=today, end_date__lt=today, store=store)

    def recently_expired(self, store: Store):  # 가장 최근에 만료된 계약 순서대로
        return self.filter(store=store).order_by("-end_date")

    def tomorrow_start(self):  # 내일부터 시작되는 계약
        today = date.today()
        return self.filter(start_date=today + timedelta(days=1))

    def tomorrow_expired(self):  # 내일 계약 만료일이 도래하는
        today = date.today()
        return self.filter(end_date=today + timedelta(days=1))


class Contract(models.Model):  # 상점 계약
    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    sales_commission = models.DecimalField(decimal_places=2, max_digits=5, db_comment="판매 수수료(%)")

    start_date = models.DateField(null=True, db_comment="계약 시작 날짜")
    end_date = models.DateField(null=True, db_comment="계약 종료 날짜")

    objects = ContractManger()

















