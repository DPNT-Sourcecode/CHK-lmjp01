from collections import defaultdict
import copy


class Item():
    def __init__(self, sku, price, volume_discounts, freebie_offers):
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


def calc_max_volume_discount(item, sku_count):
    price = 0
    if item.volume_discounts:
        for volume_discount in sorted(item.volume_discounts, key=lambda x:x.get_price_per_item()):
            times_applied = sku_count[item.sku] // volume_discount.volume
            price += times_applied * volume_discount.price
            sku_count[item.sku] -= times_applied * volume_discount.volume

    return price


def calc_eligible_freebies(items, sku_count):
    for item in items:
        if item.freebie_offers:
            pass


def calc_price_volume_first(items, sku_count):
    total_price = 0
    for item in items:
        max_volume_discount = calc_max_volume_discount(item, sku_count)
        calc_eligible_freebies(items, sku_count)
        total_price += max_volume_discount + (sku_count[item.sku] * item.price)
    return total_price


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

    """
    for item
    calc maximum volume discount savings
    calc freebies possible
    calc price and save
    invert, calc price, compare
    """
    price_volume_first = calc_price_volume_first(items, copy.deepcopy(sku_count))

    price_freebies_first = 0

    return min(price_volume_first, price_freebies_first)




