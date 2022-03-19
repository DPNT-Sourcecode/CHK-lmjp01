from collections import defaultdict
from email.policy import default


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

    sku_count = defaultdict(int)

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1
        sku_count[sku] += 1

    total_price = 0

    return total_price

