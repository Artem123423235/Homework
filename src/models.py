from abc import ABC, abstractmethod
import os
from typing import Dict, Iterable, List, Optional, Union


class LoggingMixin:
    """
    Миксин: при создании объекта (после инициализации базового конструктора)
    печатает в stdout информацию о классе и параметрах.
    Также реализует __repr__.
    """

    def __init__(self, *args, **kwargs):
        # вызываем дальше по MRO, чтобы базы инициализировались до печати
        super().__init__(*args, **kwargs)
        # формируем строку в формате: Class('name', 'description', price, quantity)
        name = getattr(self, "name", None)
        description = getattr(self, "description", None)
        # price — property, безопасно получить
        price = getattr(self, "price", None)
        quantity = getattr(self, "quantity", None)
        print(f"{self.__class__.__name__}({name!r}, {description!r}, {price!r}, {quantity!r})")

    def __repr__(self) -> str:
        name = getattr(self, "name", None)
        description = getattr(self, "description", None)
        price = getattr(self, "price", None)
        quantity = getattr(self, "quantity", None)
        return f"{self.__class__.__name__}({name!r}, {description!r}, {price!r}, {quantity!r})"


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Содержит общую логику: инициализация, price property, __str__, total_value,
    сложение и new_product.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = str(name)
        self.description = str(description)
        # внутреннее хранилище цены
        self._price = float(price)
        self.quantity = int(quantity)

    @property
    def price(self) -> float:
        return float(self._price)

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

        if new_price_val < self._price:
            auto_confirm = os.environ.get("AUTO_CONFIRM_PRICE_CHANGE") == "1"
            if auto_confirm:
                confirm = "y"
            else:
                prompt = (
                    f"Вы снижаете цену товара {self.name!r} с {self._price} до "
                    f"{new_price_val}. Подтвердить (y/n)? "
                )
                confirm = input(prompt).strip().lower()

            if confirm == "y":
                self._price = new_price_val
            else:
                print("Действие отменено. Цена не изменена.")
        else:
            self._price = new_price_val

    @property
    def total_value(self) -> float:
        return float(self.price) * int(self.quantity)

    def __str__(self) -> str:
        price_display = (
            f"{self.price:.0f}" if float(self.price).is_integer() else f"{self.price:.2f}"
        )
        return f"{self.name}, {price_display} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Union["BaseProduct", int, float]) -> float:
        if isinstance(other, BaseProduct):
            if type(self) is type(other):
                return self.total_value + other.total_value
            raise TypeError("Нельзя складывать продукты разных типов")
        if isinstance(other, (int, float)):
            return self.total_value + other
        return NotImplemented

    def __radd__(self, other: Union[int, float, "BaseProduct"]) -> float:
        if isinstance(other, BaseProduct):
            if type(self) is type(other):
                return other.total_value + self.total_value
            raise TypeError("Нельзя складывать продукты разных типов")
        if isinstance(other, (int, float)):
            return other + self.total_value
        return NotImplemented

    @classmethod
    def new_product(
        cls, data: Dict[str, object], existing_products: Optional[Iterable["BaseProduct"]] = None
    ) -> "BaseProduct":
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
                # слияние только если тот же точный класс
                if prod.name.strip().lower() == name.lower() and type(prod) is cls:
                    prod.quantity += quantity
                    higher_price = max(prod.price, price)
                    prod.price = higher_price
                    return prod

        return cls(name=name, description=description, price=price, quantity=quantity)

    @abstractmethod
    def product_type(self) -> str:
        """Должен возвращать тип продукта (строка)."""
        raise NotImplementedError()


class Product(LoggingMixin, BaseProduct):
    """
    Базовый (неабстрактный) продукт. Нужен для хранения общих продуктов,
    а также является родителем для Smartphone и LawnGrass.
    """

    def product_type(self) -> str:
        return self.__class__.__name__


class Smartphone(Product):
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


class BaseEntity(ABC):
    """Общий абстрактный класс для сущностей, имеющих name и description."""

    def __init__(self, name: str, description: str):
        self.name = str(name)
        self.description = str(description)

    @abstractmethod
    def summary(self) -> str:
        """Возвращает строку-резюме сущности."""
        raise NotImplementedError()


class Category(BaseEntity):
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[Iterable[Product]] = None
    ):
        super().__init__(name, description)
        self.__products: List[Product] = []
        Category.category_count += 1

        if products:
            for p in products:
                self.add_product(p)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        return list(self.__products)

    @property
    def products_str(self) -> str:
        if not self.__products:
            return "Категория пуста."
        return "\n".join(str(p) for p in self.__products)

    def total_quantity(self) -> int:
        return sum(int(p.quantity) for p in self.__products)

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {self.total_quantity()} шт."

    def _get_products_list(self) -> List[Product]:
        return list(self.__products)

    def summary(self) -> str:
        return self.__str__()

    @classmethod
    def reset_counters(cls) -> None:
        cls.category_count = 0
        cls.product_count = 0


class Order(BaseEntity):
    """
    Заказ: ссылка на товар (один товар), количество купленного товара и итоговая стоимость.
    """

    def __init__(self, product: Product, quantity: int):
        super().__init__(name=f"Order: {product.name}", description=f"Заказ товара {product.name}")
        if not isinstance(product, Product):
            raise TypeError("Order должен содержать объект Product")
        self.product = product
        self.quantity = int(quantity)
        self.total_price = float(product.price) * int(quantity)

    def summary(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.quantity}, итого: {self.total_price} руб."