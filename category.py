class Category:
    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

    def middle_price(self):
        try:
            total_price = sum(product.price for product in self.products)
            return total_price / len(self.products)
        except ZeroDivisionError:
            return 0
