

class Item():
    def __init__(self, sku, price, special_offer):
        self.sku = sku
        self.price = price
        self.special_offer = special_offer

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    items = [
        Item("A", 50, (3, 130)),
        Item("B", 30, (2, 45)),
        Item("C", 20, None),
        Item("D", 15, None)
    ]

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1

    return 0


