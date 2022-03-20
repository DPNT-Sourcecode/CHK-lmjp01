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
    items = []
    for line in table_string.splitlines()[3:-1]:
        row = [x.strip() for x in line.split('|')[1:-1]]
        sku = row[0]
        price = row[1]
        offers_string = row[2]
        volume_discounts = []
        freebie_offers = []
        for offer_string in [x.strip() for x in offers_string.split(',')]:
            offer_string_fields = offer_string.split()
            if ' for ' in offer_string:
                volume_count = int(offer_string_fields[0].split(sku)[0])
                volume_price = int(offer_string_fields[2])
                volume_discounts.append(VolumeDiscount(volume_count, volume_price))
            if ' get ' in offer_string:
                freebie_count = int(offer_string_fields[0].split(sku)[0])
                freebie_sku = offer_string_fields[3]
                if freebie_sku == sku:
                    freebie_count += 1
                freebie_offers.append(FreebieOffer(freebie_count, {freebie_sku: 1}))
        items.append(Item(sku, int(price), volume_discounts, freebie_offers))
    return items


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):

    with open('./price_table.txt') as table_string:
        items = build_items(table_string)

    sku_count = defaultdict(int)

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1
        sku_count[sku] += 1

    price_volume_first = calc_price_volume_first(items, copy.deepcopy(sku_count))

    price_freebies_first = calc_price_freebies_first(items, copy.deepcopy(sku_count))

    return min(price_volume_first, price_freebies_first)
