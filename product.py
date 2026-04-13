class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price

        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.quantity = quantity
