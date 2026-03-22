class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Класс для представления товара.

        :param name: Название товара
        :param description: Описание товара
        :param price: Цена товара
        :param quantity: Количество товара в наличии
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0  # Атрибут класса для подсчета категорий
    product_count = 0  # Атрибут класса для подсчета товаров

    def __init__(self, name: str, description: str, products: list):
        """
        Класс для представления категории товаров.

        :param name: Название категории
        :param description: Описание категории
        :param products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счетчик категорий при создании нового объекта
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в категории
        Category.product_count += len(products)