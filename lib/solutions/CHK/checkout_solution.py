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


def calc_eligible_freebies(item, sku_count):
    if item.freebie_offers:
        for freebie_offer in item.freebie_offers:
            times_applied = sku_count[item.sku] // freebie_offer.count
            for freebie_sku in freebie_offer.freebies.keys():
                sku_count[freebie_sku] -= times_applied * freebie_offer.freebies[freebie_sku]
                sku_count[freebie_sku] = max(sku_count[freebie_sku], 0)


def calc_price_volume_first(items, sku_count):
    total_price = 0
    for item in items:
        max_volume_discount = calc_max_volume_discount(item, sku_count)
        total_price += max_volume_discount
    for item in items:
        calc_eligible_freebies(item, sku_count)
    for item in items:
        total_price += sku_count[item.sku] * item.price
    return total_price


def calc_price_freebies_first(items, sku_count):
    total_price = 0
    for item in items:
        calc_eligible_freebies(item, sku_count)
    for item in items:
        max_volume_discount = calc_max_volume_discount(item, sku_count)
        total_price += max_volume_discount
    for item in items:
        total_price += sku_count[item.sku] * item.price
    return total_price


def build_items(table_string):
    for line in table_string.splitlines()[3:-1]:
        print([x.strip() for x in line.split('|')[1:-1]])


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    items = [
        Item("A", 50, [VolumeDiscount(3, 130), VolumeDiscount(5, 200)], None),
        Item("B", 30, [VolumeDiscount(2, 45)], None),
        Item("C", 20, None, None),
        Item("D", 15, None, None),
        Item("E", 40, None, [FreebieOffer(2, {"B": 1})]),
        Item("F", 10, None, [FreebieOffer(3, {"F": 1})])
    ]

    sku_count = defaultdict(int)

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1
        sku_count[sku] += 1

    price_volume_first = calc_price_volume_first(items, copy.deepcopy(sku_count))

    price_freebies_first = calc_price_freebies_first(items, copy.deepcopy(sku_count))

    return min(price_volume_first, price_freebies_first)
