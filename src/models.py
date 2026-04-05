import os
from typing import Dict, Iterable, List, Optional, Union


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = str(name)
        self.description = str(description)
        self.__price = float(price)
        self.quantity = int(quantity)

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, price={self.price!r}, "
            f"quantity={self.quantity!r})"
        )

    def __str__(self) -> str:
        """
        "Название продукта, 80 руб. Остаток: 15 шт."
        """
        price_display = (
            f"{self.price:.0f}" if float(self.price).is_integer() else f"{self.price:.2f}"
        )
        return f"{self.name}, {price_display} руб. Остаток: {self.quantity} шт."

    @property
    def price(self) -> float:
        return float(self.__price)

    @price.setter
    def price(self, new_price: float) -> None:
        try:
            new_price_val = float(new_price)
        except (TypeError, ValueError):
            print("Неверный формат цены. Цена не изменена.")
            return

        if new_price_val <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price_val < self.__price:
            auto_confirm = os.environ.get("AUTO_CONFIRM_PRICE_CHANGE") == "1"
            if auto_confirm:
                confirm = "y"
            else:
                prompt = (
                    f"Вы снижаете цену товара {self.name!r} с {self.__price} до "
                    f"{new_price_val}. Подтвердить (y/n)? "
                )
                confirm = input(prompt).strip().lower()

            if confirm == "y":
                self.__price = new_price_val
            else:
                print("Действие отменено. Цена не изменена.")
        else:
            self.__price = new_price_val

    @property
    def total_value(self) -> float:
        """Полная стоимость данного товара на складе (price * quantity)."""
        return float(self.price) * int(self.quantity)

    def __add__(self, other: Union["Product", int, float]) -> float:
        """
        Складывать можно:
        - Product + Product (только одинакового класса) -> сумма total_value
        - Product + число -> total_value + число
        В противном случае — TypeError или NotImplemented.
        """
        if isinstance(other, Product):
            # разрешаем сложение только если оба ровно одного класса
            if type(self) is type(other):
                return self.total_value + other.total_value
            raise TypeError("Нельзя складывать продукты разных типов")
        if isinstance(other, (int, float)):
            return self.total_value + other
        return NotImplemented

    def __radd__(self, other: Union[int, float, "Product"]) -> float:
        """
        Обратное сложение, чтобы поддерживать sum(products, 0).
        При other == Product — проверяем типы аналогично __add__.
        """
        if isinstance(other, Product):
            if type(self) is type(other):
                return other.total_value + self.total_value
            raise TypeError("Нельзя складывать продукты разных типов")
        if isinstance(other, (int, float)):
            return other + self.total_value
        return NotImplemented

    @classmethod
    def new_product(
        cls, data: Dict[str, object], existing_products: Optional[Iterable["Product"]] = None
    ) -> "Product":
        """
        Создаёт продукт из словаря. При наличии existing_products — ищет
        продукт с тем же именем и тем же классом (type == cls), если найден —
        суммирует quantity и обновляет цену (берёт максимальную).
        """
        name = str(data.get("name", "")).strip()
        description = str(data.get("description", "")).strip()
        try:
            price = float(data.get("price", 0))
        except (TypeError, ValueError):
            price = 0.0
        try:
            quantity = int(data.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0

        if existing_products:
            for prod in existing_products:
                if prod.name.strip().lower() == name.lower() and type(prod) is cls:
                    prod.quantity += quantity
                    higher_price = max(prod.price, price)
                    prod.price = higher_price
                    return prod

        return cls(name=name, description=description, price=price, quantity=quantity)


class Smartphone(Product):
    """
    Наследник Product для смартфонов.
    Дополнительные атрибуты: efficiency, model, memory, color
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: Optional[float] = None,
        model: Optional[str] = None,
        memory: Optional[int] = None,
        color: Optional[str] = None,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Наследник Product для травы газонной.
    Дополнительные атрибуты: country, germination_period, color
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: Optional[str] = None,
        germination_period: Optional[int] = None,
        color: Optional[str] = None,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[Iterable[Product]] = None
    ):
        self.name = str(name)
        self.description = str(description)
        self.__products: List[Product] = []
        Category.category_count += 1

        if products:
            for p in products:
                self.add_product(p)

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию. Разрешено только добавление объектов класса
        Product или его наследников. В противном случае — TypeError.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """Возвращает копию списка продуктов (для безопасного чтения)."""
        return list(self.__products)

    @property
    def products_str(self) -> str:
        """Многострочная строка со списком продуктов (использует __str__ каждого продукта)."""
        if not self.__products:
            return "Категория пуста."
        return "\n".join(str(p) for p in self.__products)

    def total_quantity(self) -> int:
        """Суммарное количество всех штук во всех продуктах категории."""
        return sum(int(p.quantity) for p in self.__products)

    def __str__(self) -> str:
        """"Название категории, количество продуктов: 200 шт." (сумма quantity всех продуктов)."""
        return f"{self.name}, количество продуктов: {self.total_quantity()} шт."

    def _get_products_list(self) -> List[Product]:
        return list(self.__products)

    @classmethod
    def reset_counters(cls) -> None:
        cls.category_count = 0
        cls.product_count = 0


class CategoryIterator:
    """Итератор для перебора товаров одной категории."""

    def __init__(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("CategoryIterator ожидает объект Category")
        self._products = category.products  # копия списка
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        item = self._products[self._index]
        self._index += 1
        return item