from collections import defaultdict
from email.policy import default


class Item():
    def __init__(self, sku, price, special_offer, volume_discounts, freebie_offers):
        self.sku = sku
        self.price = price
        self.volume_discounts = volume_discounts
        self.freebie_offers = freebie_offers


class VolumeDiscount():
    def __init__(self, volume, price):
        self.volume = volume
        self.price = price

    def get_price_per_item(self):
        return self.price / self.volume


class FreebieOffer():
    def __init__(self, count, freebies):
        self.count = count
        self.freebies = freebies


def calc_max_volume_discount(sku_count, item):
    price = 0



# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    items = [
        Item("A", 50, [VolumeDiscount(3, 130), VolumeDiscount(5, 200)], None),
        Item("B", 30, [VolumeDiscount(2, 45)], None),
        Item("C", 20, None, None),
        Item("D", 15, None, None),
        Item("E", 40, None, [FreebieOffer(2, {"B": 1})])
    ]

    sku_count = defaultdict(int)

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1
        sku_count[sku] += 1

    total_price = 0

    """
    for item
    calc maximum volume discount savings
    calc freebies possible
    calc price and save
    invert, calc price, compare
    """

    for item in items:
        pass

    return total_price




