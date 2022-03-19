from solutions.CHK import checkout_solution


class TestCheckout():
    # items = [
    #     Item("A", 50, (3, 130)),
    #     Item("B", 30, (2, 45)),
    #     Item("C", 20, None),
    #     Item("D", 15, None)
    # ]

    def test_checkout_illegal_input(self):
        assert checkout_solution.checkout("ABCDE") == -1

    def test_checkout_legal_input(self):
        assert checkout_solution.checkout("ABCD") == 50 + 30 + 20 + 15

    def test_checkout_special_offer(self):
        assert checkout_solution.checkout("AAA") == 130

    def test_checkout_special_offer_plus_regular(self):
        assert checkout_solution.checkout("AAAA") == 130 + 50

    def test_checkout_special_offer_multiple_times(self):
        assert checkout_solution.checkout("AAAAAA") == 130 * 2

    def test_checkout_complicated(self):
        assert checkout_solution.checkout("AAAABBBCCD") == (130 + 50) + (45 + 30) + (20 * 2) + 15 