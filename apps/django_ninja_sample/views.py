#from django.shortcuts import render

from ninja import NinjaAPI

# Create your views here.

ninja_api = NinjaAPI(
    title="Ninja Sample API 문서",
    description="핸즈온 장고 실습 예제"
)


@ninja_api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
