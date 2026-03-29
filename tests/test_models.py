import os
import pytest
from src.models import Product, Category, CategoryIterator


def test_product_str_and_total_value():
    p = Product("Хлеб", "Свежий", 80.0, 15)
    assert str(p) == "Хлеб, 80 руб. Остаток: 15 шт."
    assert p.total_value == 80.0 * 15


def test_product_addition_and_sum():
    a = Product("A", "", 100.0, 10)  # total 1000
    b = Product("B", "", 200.0, 2)   # total 400
    assert a + b == 1400
    # Проверка суммирования через sum
    products = [a, b]
    total = sum(products, 0)
    assert total == 1400


def test_category_str_and_products_str():
    p1 = Product("Товар1", "", 10.0, 2)
    p2 = Product("Товар2", "", 5.0, 3)
    cat = Category("Категория", "Описание", [p1, p2])
    # __str__ должен показывать суммарное количество: 2 + 3 = 5
    assert str(cat) == "Категория, количество продуктов: 5 шт."
    # products_str использует __str__ продуктов
    expected = f"{str(p1)}\n{str(p2)}"
    assert cat.products_str == expected


def test_category_iterator():
    p1 = Product("T1", "", 1.0, 1)
    p2 = Product("T2", "", 2.0, 2)
    cat = Category("C", "D", [p1, p2])
    it = CategoryIterator(cat)
    collected = [x for x in it]
    assert collected == [p1, p2]


def test_price_setter_negative_and_confirmation(monkeypatch):
    p = Product("X", "", 100.0, 1)
    # отрицательная цена — не изменяется
    p.price = -10
    assert p.price == 100.0

    # понижение с подтверждением: симулируем ввод 'n' (отмена)
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")
    p.price = 50.0
    assert p.price == 100.0

    # симулируем 'y' (подтверждение)
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")
    p.price = 50.0
    assert p.price == 50.0

    # автоподтверждение через переменную окружения (для CI)
    os.environ["AUTO_CONFIRM_PRICE_CHANGE"] = "1"
    p.price = 40.0  # автоматически подтверждается
    assert p.price == 40.0
    del os.environ["AUTO_CONFIRM_PRICE_CHANGE"]
