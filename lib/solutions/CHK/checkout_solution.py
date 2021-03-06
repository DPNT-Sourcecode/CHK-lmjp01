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


class TableBuilder():
    table_string = """
        +------+-------+---------------------------------+
        | Item | Price | Special offers                  |
        +------+-------+---------------------------------+
        | A    | 50    | 3A for 130, 5A for 200          |
        | B    | 30    | 2B for 45                       |
        | C    | 20    |                                 |
        | D    | 15    |                                 |
        | E    | 40    | 2E get one B free               |
        | F    | 10    | 2F get one F free               |
        | G    | 20    |                                 |
        | H    | 10    | 5H for 45, 10H for 80           |
        | I    | 35    |                                 |
        | J    | 60    |                                 |
        | K    | 70    | 2K for 120                      |
        | L    | 90    |                                 |
        | M    | 15    |                                 |
        | N    | 40    | 3N get one M free               |
        | O    | 10    |                                 |
        | P    | 50    | 5P for 200                      |
        | Q    | 30    | 3Q for 80                       |
        | R    | 50    | 3R get one Q free               |
        | S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | U    | 40    | 3U get one U free               |
        | V    | 50    | 2V for 90, 3V for 130           |
        | W    | 20    |                                 |
        | X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
        +------+-------+---------------------------------+
    """

    def __init__(self):
        self.items = []
        self.multi_volume_discounts = {}
        for line in self.table_string.splitlines()[4:-2]:
            row = [x.strip() for x in line.split('|')[1:-1]]
            sku = row[0]
            price = row[1]
            offers_string = row[2]
            volume_discounts = []
            freebie_offers = []
            for offer_string in [x.strip() for x in offers_string.split(', ')]:
                offer_string_fields = offer_string.split()
                if offer_string_fields:
                    if offer_string_fields[1] == "for":
                        volume_count = int(offer_string_fields[0].split(sku)[0])
                        volume_price = int(offer_string_fields[2])
                        volume_discounts.append(VolumeDiscount(volume_count, volume_price))
                    if offer_string_fields[1] == "get":
                        freebie_count = int(offer_string_fields[0].split(sku)[0])
                        freebie_sku = offer_string_fields[3]
                        if freebie_sku == sku:
                            freebie_count += 1
                        freebie_offers.append(FreebieOffer(freebie_count, {freebie_sku: 1}))
                    if offer_string_fields[1] == "any":
                        multi_volume_count = int(offer_string_fields[2])
                        multi_volume_price = int(offer_string_fields[-1])
                        multi_volume_skus = offer_string_fields[4][1:-1].split(',')
                        self.multi_volume_discounts[tuple(multi_volume_skus)] = VolumeDiscount(multi_volume_count, multi_volume_price)
            self.items.append(Item(sku, int(price), volume_discounts, freebie_offers))

    
def build_items_wrapper():
    return TableBuilder().items


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


def calc_max_multi_volume_discount(items, multi_volume_discounts, sku_count):
    item_prices = {}
    for item in items:
        item_prices[item.sku] = item.price

    multi_volume_skus_available = ""
    max_multi_volume_discount = 0
    for mvd_skus in multi_volume_discounts.keys():
        sorted_skus = list(mvd_skus)
        sorted_skus.sort(key=lambda x: item_prices[x], reverse=True)
        for sku in sorted_skus:
            multi_volume_skus_available += sku * sku_count[sku]
        mvd_volume = multi_volume_discounts[mvd_skus].volume
        times_applied = len(multi_volume_skus_available) // mvd_volume
        multi_volume_skus_available = multi_volume_skus_available[:(times_applied * mvd_volume)]
        for sku in multi_volume_skus_available:
            sku_count[sku] -= 1
        max_multi_volume_discount += times_applied * multi_volume_discounts[mvd_skus].price

    return max_multi_volume_discount


def calc_price_volume_first(items, sku_count, multi_volume_discounts):
    total_price = 0
    total_price += calc_max_multi_volume_discount(items, multi_volume_discounts, sku_count)
    for item in items:
        max_volume_discount = calc_max_volume_discount(item, sku_count)
        total_price += max_volume_discount
    for item in items:
        calc_eligible_freebies(item, sku_count)
    for item in items:
        total_price += sku_count[item.sku] * item.price
    return total_price


def calc_price_freebies_first(items, sku_count, multi_volume_discounts):
    total_price = 0
    for item in items:
        calc_eligible_freebies(item, sku_count)
    total_price += calc_max_multi_volume_discount(items, multi_volume_discounts, sku_count)
    for item in items:
        max_volume_discount = calc_max_volume_discount(item, sku_count)
        total_price += max_volume_discount
    for item in items:
        total_price += sku_count[item.sku] * item.price
    return total_price


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):

    items = build_items_wrapper()

    sku_count = defaultdict(int)

    multi_volume_discounts = TableBuilder().multi_volume_discounts

    for sku in skus:
        if sku not in [x.sku for x in items]:
            return -1
        sku_count[sku] += 1

    price_volume_first = calc_price_volume_first(items, copy.deepcopy(sku_count), multi_volume_discounts)

    price_freebies_first = calc_price_freebies_first(items, copy.deepcopy(sku_count), multi_volume_discounts)

    return min(price_volume_first, price_freebies_first)
