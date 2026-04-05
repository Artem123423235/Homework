import os
import pytest
from src.models import (
    BaseProduct,
    Product,
    Smartphone,
    LawnGrass,
    Category,
    Order,
    LoggingMixin,
)


def test_baseproduct_is_abstract():
    # Нельзя инстанцировать BaseProduct напрямую
    with pytest.raises(TypeError):
        BaseProduct("a", "b", 1.0, 1)


def test_logging_mixin_prints_on_creation(capsys):
    # Устанавливаем автоматическое подтверждение изменения цены, чтобы сеттер не блокировал ввод
    os.environ["AUTO_CONFIRM_PRICE_CHANGE"] = "1"
    p = Product("Продукт1", "Описание продукта", 1200, 10)
    captured = capsys.readouterr()
    assert "Product('Продукт1', 'Описание продукта', 1200.0, 10)" in captured.out
    # Также проверим смартфон и трава
    s = Smartphone("Phone", "Smart", 30000.0, 2, model="X")
    g = LawnGrass("Grass", "Lawn", 50.0, 5, country="NL")
    captured = capsys.readouterr()
    assert "Smartphone('Phone', 'Smart', 30000.0, 2)" in captured.out
    assert "LawnGrass('Grass', 'Lawn', 50.0, 5)" in captured.out
    del os.environ["AUTO_CONFIRM_PRICE_CHANGE"]


def test_addition_and_type_restriction():
    os.environ["AUTO_CONFIRM_PRICE_CHANGE"] = "1"
    a = Smartphone("S1", "", 100.0, 10)
    b = Smartphone("S2", "", 200.0, 2)
    c = LawnGrass("L1", "", 10.0, 50)

    assert a + b == a.total_value + b.total_value

    with pytest.raises(TypeError):
        _ = a + c

    with pytest.raises(TypeError):
        _ = c + a
    del os.environ["AUTO_CONFIRM_PRICE_CHANGE"]


def test_category_and_order_baseentity_and_add_protects():
    cat = Category("C", "desc")
    p = Product("P", "", 10.0, 1)
    s = Smartphone("S", "", 100.0, 1)
    cat.add_product(p)
    cat.add_product(s)
    assert len(cat.products) == 2

    with pytest.raises(TypeError):
        cat.add_product(123)

    # Order requires Product
    order = Order(product=s, quantity=3)
    assert order.total_price == s.price * 3
    assert "Order" in order.name


def test_new_product_merging_by_type():
    os.environ["AUTO_CONFIRM_PRICE_CHANGE"] = "1"
    existing = [Smartphone("Phone", "", 30000.0, 2)]
    data_same = {"name": "Phone", "description": "", "price": 31000.0, "quantity": 1}
    prod = Smartphone.new_product(data_same, existing_products=existing)
    assert prod is existing[0]
    assert prod.quantity == 3
    assert prod.price == 31000.0
    del os.environ["AUTO_CONFIRM_PRICE_CHANGE"]