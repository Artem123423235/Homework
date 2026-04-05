import pytest
from src.models import Product, Smartphone, LawnGrass, Category


def test_subclasses_are_products_and_have_specific_attrs():
    s = Smartphone("Phone", "Smart", 30000.0, 5, efficiency=9.5, model="X1", memory=128, color="black")
    g = LawnGrass("Газонная", "Трава", 200.0, 20, country="NL", germination_period=14, color="green")

    assert isinstance(s, Product)
    assert isinstance(g, Product)

    # дополнительные атрибуты присутствуют
    assert s.efficiency == 9.5
    assert s.model == "X1"
    assert s.memory == 128
    assert s.color == "black"

    assert g.country == "NL"
    assert g.germination_period == 14
    assert g.color == "green"


def test_addition_only_same_type_allowed():
    a = Smartphone("S1", "", 100.0, 10)
    b = Smartphone("S2", "", 200.0, 2)
    c = LawnGrass("L1", "", 10.0, 50)

    # Smartphone + Smartphone -> ok
    assert a + b == a.total_value + b.total_value

    # Smartphone + LawnGrass -> TypeError
    with pytest.raises(TypeError):
        _ = a + c

    # LawnGrass + Smartphone -> TypeError
    with pytest.raises(TypeError):
        _ = c + a


def test_category_add_product_type_enforcement():
    cat = Category("Катег", "desc")
    p = Product("P", "", 10.0, 1)
    s = Smartphone("S", "", 100.0, 1)
    g = LawnGrass("G", "", 5.0, 10)

    cat.add_product(p)
    cat.add_product(s)
    cat.add_product(g)

    assert len(cat.products) == 3

    # Попытка добавить не-продукт -> TypeError
    with pytest.raises(TypeError):
        cat.add_product(123)

    with pytest.raises(TypeError):
        cat.add_product("not a product")


def test_new_product_merging_respects_type():
    existing = [Smartphone("Phone", "", 30000.0, 2)]
    data_same = {"name": "Phone", "description": "", "price": 31000.0, "quantity": 1}
    data_diff = {"name": "Phone", "description": "", "price": 50.0, "quantity": 5}

    # merging with same class -> will update existing smartphone
    prod = Smartphone.new_product(data_same, existing_products=existing)
    assert prod is existing[0]
    assert prod.quantity == 3
    assert prod.price == 31000.0  # higher price chosen

    # merging with different class (Product) should not merge into Smartphone list
    existing2 = [Product("Phone", "", 50.0, 10)]
    new_phone = Smartphone.new_product(data_diff, existing_products=existing2)
    # new_phone should be a new Smartphone instance (not merged into Product)
    assert isinstance(new_phone, Smartphone)
    assert new_phone is not existing2[0]