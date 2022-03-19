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

    for item in items:
        item_count = sku_count[item.sku]
        if item.special_offer:
            special_offer_count = item_count / item.special_offer[0]
            regular_price_count = item_count % item.special_offer[0]
            special_offer_price = item.special_offer[1]
        else:
            special_offer_count = 0
            regular_price_count = item_count
            special_offer_price = 0
        total_price += (special_offer_count * special_offer_price) + (regular_price_count * item.price)
        

    return total_price

