
class Account:

    def __init__(self):
        self.cny_balance = 0
        self.btc_balance = 0
        self.btc_frozen = 0
        self.cny_frozen = 0

    def __str__(self):
        return "cny_balance:%.4f, btc_balance:%.4f, btc_frozen:%.4f, cny_frozen:%.4f" \
                %(self.cny_balance, self.btc_balance, self.btc_frozen, self.cny_frozen)