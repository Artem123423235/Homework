import os
from typing import Dict, Iterable, List, Optional


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

    @classmethod
    def new_product(
        cls, data: Dict[str, object], existing_products: Optional[Iterable["Product"]] = None
    ) -> "Product":
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
                if prod.name.strip().lower() == name.lower():
                    prod.quantity += quantity
                    higher_price = max(prod.price, price)
                    prod.price = higher_price
                    return prod

        return cls(name=name, description=description, price=price, quantity=quantity)


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
        if not isinstance(product, Product):
            raise TypeError("add_product ожидает объект Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """
        Возвращает копию списка Product-ов.
        Используйте len(category.products) для количества товаров.
        """
        return list(self.__products)

    @property
    def products_str(self) -> str:
        """
        Возвращает список товаров как многострочную строку:
        "Название продукта, 80 руб. Остаток: 15 шт."
        """
        if not self.__products:
            return "Категория пуста."

        lines: List[str] = []
        for p in self.__products:
            price_display = (
                f"{p.price:.0f}" if float(p.price).is_integer() else f"{p.price:.2f}"
            )
            lines.append(f"{p.name}, {price_display} руб. Остаток: {p.quantity} шт.")
        return "\n".join(lines)

    def _get_products_list(self) -> List[Product]:
        return list(self.__products)

    @classmethod
    def reset_counters(cls) -> None:
        cls.category_count = 0
        cls.product_count = 0
