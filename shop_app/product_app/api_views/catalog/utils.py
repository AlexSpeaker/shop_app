from typing import Any, Dict

from django.db.models import Q


def get_catalog_filters(data: Dict[str, Any]) -> Q:
    """
    Функция создаст фильтр на основе переданных данных.

    :param data: Данные.
    :return: Фильтр.
    """
    filter_data = data["filter"]
    # Создаём простые фильтры.
    filter_params = Q(title__icontains=filter_data["name"])
    filter_params &= Q(free_delivery=filter_data["freeDelivery"])
    filter_params &= Q(count__gt=0) if filter_data["available"] else Q(count=0)
    # А также учитываем категорию и не архивированные продукты.
    if data.get("category"):
        filter_params &= Q(category__id=data["category"])
    filter_params &= Q(archived=False)
    # Если есть tags, то их тоже учитываем.
    tags_list = data.get("tags")
    if tags_list:
        filter_params &= Q(tags__pk__in=tags_list)

    return filter_params


def get_catalog_sort(data: Dict[str, Any]) -> str:
    """
    Функция создаст параметр сортировки на основе переданных данных с некоторой заменой.
    Вместо 'price' будет 'final_price'.
    Вместо 'reviews' будет 'reviews_count'.
    Вместо 'date' будет 'created_at'.

    :param data: Данные.
    :return: Параметр сортировки.
    """

    # Переопределяем названия сортировки,
    # так как эти названия пересекаются с полями продукта или вовсе отсутствуют,
    # например reviews в продукте - это связанная сущность, а не количество отзывов,
    # а price у нас, после применения аннотации, будет final_price...
    if data["sort"] == "price":
        pre_sort = "final_price"
    elif data["sort"] == "reviews":
        pre_sort = "reviews_count"
    elif data["sort"] == "date":
        pre_sort = "created_at"
    else:
        pre_sort = data["sort"]
    # Определяем тип сортировки (убывание/возрастание) и возвращаем.
    return f"-{pre_sort}" if data["sortType"] == "inc" else pre_sort
