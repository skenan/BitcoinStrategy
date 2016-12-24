class Depth:

    def __init__(self):

        self.sell_price = 0
        self.sell_amount = 0
        self.buy_price = 0
        self.buy_amount = 0

    def __str__(self):
        return "sell_price:%.4f, sell_amount:%.4f, buy_price:%.4f, buy_amout:%.4f" \
               % (self.sell_price, self.sell_amount, self.buy_price, self.buy_amount)
