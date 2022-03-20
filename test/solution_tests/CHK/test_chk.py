from solutions.CHK import checkout_solution


class TestCheckout():
    # items = [
    #     Item("A", 50, (3, 130)),
    #     Item("B", 30, (2, 45)),
    #     Item("C", 20, None),
    #     Item("D", 15, None)
    # ]

    def test_checkout_illegal_input(self):
        assert checkout_solution.checkout("ABCDEFG ") == -1

    def test_checkout_legal_input(self):
        assert checkout_solution.checkout("ABCDEF") == 50 + 30 + 20 + 15 + 40 + 10

    def test_checkout_volume_discount(self):
        assert checkout_solution.checkout("AAA") == 130

    def test_checkout_volume_discount_plus_regular(self):
        assert checkout_solution.checkout("AAAA") == 130 + 50

    def test_checkout_volume_discount_mixed(self):
        assert checkout_solution.checkout("AAAAAAAA") == 130 + 200

    def test_checkout_volume_discount_multiple_times(self):
        assert checkout_solution.checkout("AAAAAAAAAA") == 200 * 2

    def test_checkout_complicated(self):
        assert checkout_solution.checkout("AAAABBBCCD") == (130 + 50) + (45 + 30) + (20 * 2) + 15 

    def test_checkout_freebie(self):
        assert checkout_solution.checkout("EE") == checkout_solution.checkout("EEB")
        assert checkout_solution.checkout("FF") == checkout_solution.checkout("FFF")
    
    def test_checkout_freebie_with_volume_discount(self):
        assert checkout_solution.checkout("EEBB") == (40 * 2) + 30

    def test_build_items(self):
        table_string = """+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |"""
        items = checkout_solution.build_items(table_string)
        print(items)
        assert items[0].sku == "A"