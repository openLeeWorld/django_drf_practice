from __future__ import annotations
# __future__ 모듈: 앞으로 도입될 기능을 현재의 Python 버전에서도 쓸 수 있음
# annotations 기능 활성화 시 타입 힌트에서 문자열로 처리되던 타입 주석을 지연 평가함

from django.db import models

from typing import List


# typing 모듈에서 List 타입 힌트를 가져옴 (타입 힌트 기능 확장 및 정교한 타입 주석 작성)

# Create your models here.

class OrderedProduct(models.Model):
    order = models.ForeignKey(to="orders.Order", on_delete=models.CASCADE)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    count = models.IntegerField(help_text="주문한 해당 메뉴의 갯수", default=1)

    class Meta:
        db_table = "ordered_product"
        db_table_comment = "주문된 상품, Order와 Product사이 매핑 테이블"


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "주문 수락 대기중"
        ACCEPTED = "accepted", "주문 접수 완료"
        REJECTED = "rejected", "주문 거절"
        DELIVERY_COMPLETE = "delivery complete", "배달 완료"

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        help_text="주문 상태 값",
        default=Status.WAITING
    )
    total_price = models.IntegerField(default=0)
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)

    product_set = models.ManyToManyField(
        to="products.Product",
        through="orderedProduct",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="주문이 생성된 시간")

    address = models.CharField(max_length=256, help_text="주문 배송지")


class DailyReportManager(models.Manager):
    # 통계 쿼리 매니저
    def get_list_by_created_at(self, created_at__gte, created_at__lte) -> List[DailyReport]:
        return list(
            self.raw(
                raw_query="""
                SELECT DATE_TRUNC('day', 0.created_at) AS day,
                    COUNT(*) AS total_cnt,
                    SUM(0.total_price) as total_sales
                FROM orders_order 0 
                WHERE 0.created_at >= %s AND 0.created_at < %s
                group by DATE_TRUNC('day', 0.created_at);
                """,
                params=[created_at__gte, created_at__lte],
            ),
        )


class DailyReport(models.Model):  # 일별 통계
    day = models.DateField(help_text="날짜", primary_key=True)
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")
    total_sales = models.IntegerField(help_text="일 주문 총 매출")

    objects = DailyReportManager()

    class Meta:
        managed = False
        # 장고에서 관리하고 생성하지 않음

    def __repr__(self) -> str:
        return (  # 어떤 객체의 출력될 수 있는 표현을 문자열의 형태로 반환
            f" {self.day.strftime('%Y-%m-%d')}:DailyReport(total_cnt:{self.total_cnt} total_sales: {self.total_sales})"
        )


class DailyReportVModel(models.Model):
    day = models.DateField(help_text="날짜", primary_key=True)
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")
    total_sales = models.IntegerField(help_text="일 주문 총 매출")

    class Meta:
        db_table = "daily_report_view_table"
