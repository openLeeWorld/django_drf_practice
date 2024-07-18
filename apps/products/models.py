from django.db import models
from django.db.models import TextChoices


# Create your models here.

class Product(models.Model):
    class ProductType(TextChoices):
        GROCERY = "grocery", "식료품",
        FURNITURE = "furniture", "가구"
        BOOKS = "books", "책"
        FOOD = "food", "음식"

    name = models.CharField(max_length=128, help_text="상품명")
    price = models.IntegerField(help_text="상품 가격")
    created_at = models.DateTimeField(auto_now_add=True, )
    update_at = models.DateTimeField(auto_now_add=True, )
    product_type = models.CharField(choices=ProductType.choices, max_length=32)
    store = models.ForeignKey(
        to="stores.Store",
        on_delete=models.CASCADE,
        null=True,
        help_text="이 상품을 판매 하는 가게",
        related_name="product_new",
    )

    class Meta:
        db_table = "product"
        db_table_comment = "상품 테이블입니다."
        ordering = ("-created_at",)
        indexes = (
            models.Index(  # 장고는 DB에 인덱스 생성 가능
                fields=["created_at"],
                name="created_at_index",
            ),
            models.Index(fields=["name", "product_type"], name="name_pt_composite_index"),
            # Hash(fields=["name"], name="name_hash_index"), 는 postgresql만 있음
        )
        constraints = (
            models.CheckConstraint(
                check=models.Q(price__lte=100_000_000),
                name="check_unreasonable_price",
            ),
            models.UniqueConstraint(fields=["store", "name", "product_type"], name="unique_in_store"),
        )


class GroceryProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.GROCERY)


class GroceryProduct(Product):
    objects = GroceryProductManager()

    class Meta:
        proxy = True

    # 각종 식료품 관련 메서드 들 선언 가능 ex) is_3days_before_to_expired()


class FurnitureProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.FURNITURE)


class FurnitureProduct(Product):
    objects = FurnitureProductManager()

    class Meta:
        proxy = True

    # 각종 가구 관련 메서드 들 ex) is_heavy()?


class BooksProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.BOOKS)


class BooksProduct(Product):
    objects = BooksProductManager()

    class Meta:
        proxy = True
