import pytest
from src.models import Product, Category


def test_product_initialization():
    """Тест корректности инициализации объектов класса Product."""
    # Создаем тестовый продукт
    product = Product("Тест продукт", "Тестовое описание", 1000.0, 10)

    # Проверяем корректность инициализации
    assert product.name == "Тест продукт", "Название продукта должно соответствовать"
    assert product.description == "Тестовое описание", "Описание продукта должно соответствовать"
    assert product.price == 1000.0, "Цена продукта должна соответствовать"
    assert product.quantity == 10, "Количество продукта должно соответствовать"


def test_category_initialization():
    """Тест корректности инициализации объектов класса Category."""
    # Сбрасываем счетчики класса перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создаем тестовые продукты
    product1 = Product("Продукт 1", "Описание 1", 100.0, 5)
    product2 = Product("Продукт 2", "Описание 2", 200.0, 3)

    # Создаем тестовую категорию
    category = Category("Тест категория", "Тестовое описание категории", [product1, product2])

    # Проверяем корректность инициализации
    assert category.name == "Тест категория", "Название категории должно соответствовать"
    assert category.description == "Тестовое описание категории", "Описание категории должно соответствовать"
    assert len(category.products) == 2, "Количество продуктов в категории должно соответствовать"
    assert category.products[0].name == "Продукт 1", "Первый продукт в категории должен быть корректным"
    assert category.products[1].name == "Продукт 2", "Второй продукт в категории должен быть корректным"


def test_category_count():
    """Тест подсчета количества категорий."""
    # Сбрасываем счетчики класса перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Проверяем начальное значение
    assert Category.category_count == 0, "Начальное количество категорий должно быть 0"

    # Создаем первую категорию
    product1 = Product("Продукт 1", "Описание 1", 100.0, 1)
    category1 = Category("Категория 1", "Описание 1", [product1])
    assert Category.category_count == 1, "После создания первой категории счетчик должен быть 1"

    # Создаем вторую категорию
    product2 = Product("Продукт 2", "Описание 2", 200.0, 2)
    category2 = Category("Категория 2", "Описание 2", [product2])
    assert Category.category_count == 2, "После создания второй категории счетчик должен быть 2"


def test_product_count():
    """Тест подсчета количества товаров."""
    # Сбрасываем счетчики класса перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Проверяем начальное значение
    assert Category.product_count == 0, "Начальное количество товаров должно быть 0"

    # Создаем первую категорию с 2 товарами
    product1 = Product("Продукт 1", "Описание 1", 100.0, 1)
    product2 = Product("Продукт 2", "Описание 2", 200.0, 2)
    category1 = Category("Категория 1", "Описание 1", [product1, product2])
    assert Category.product_count == 2, "После создания категории с 2 товарами счетчик должен быть 2"

    # Создаем вторую категорию с 1 товаром
    product3 = Product("Продукт 3", "Описание 3", 300.0, 3)
    category2 = Category("Категория 2", "Описание 2", [product3])
    assert Category.product_count == 3, "После создания второй категории с 1 товаром счетчик должен быть 3"


def test_category_attributes_access():
    """Тест доступа к атрибутам класса через экземпляры."""
    # Сбрасываем счетчики класса перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создаем категории
    product1 = Product("Продукт 1", "Описание 1", 100.0, 1)
    category1 = Category("Категория 1", "Описание 1", [product1])

    product2 = Product("Продукт 2", "Описание 2", 200.0, 2)
    category2 = Category("Категория 2", "Описание 2", [product2])

    # Проверяем доступ к атрибутам класса через экземпляры
    assert category1.category_count == 2, "Атрибут класса должен быть доступен через экземпляр"
    assert category1.product_count == 2, "Атрибут класса должен быть доступен через экземпляр"
    assert category2.category_count == 2, "Атрибут класса должен быть доступен через экземпляр"
    assert category2.product_count == 2, "Атрибут класса должен быть доступен через экземпляр"


@pytest.fixture
def sample_products():
    """Фикстура для создания тестовых продуктов."""
    return [
        Product("Телефон", "Смартфон", 50000.0, 10),
        Product("Ноутбук", "Игровой", 100000.0, 5),
        Product("Наушники", "Беспроводные", 10000.0, 20)
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории."""
    # Сбрасываем счетчики класса перед созданием категории
    Category.category_count = 0
    Category.product_count = 0
    return Category("Электроника", "Техника", sample_products)


def test_category_with_fixture(sample_category, sample_products):
    """Тест категории с использованием фикстур."""
    # Проверяем корректность инициализации
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Техника"
    assert len(sample_category.products) == 3
    assert sample_category.products == sample_products


def test_product_count_with_fixture(sample_category):
    """Тест подсчета товаров с использованием фикстур."""
    assert Category.product_count == 3, "Должно быть 3 товара в категории"
    assert Category.category_count == 1, "Должна быть 1 категория"
