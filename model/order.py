
class Order:

    def __init__(self):
        self.order_id = 0
        self.status = 0
        self.price = 0
        self.deal_amount = 0
        self.avg_price = 0


    def __str__(self):
        return "order_id:%s, status:%s, price %.2f, deal_amount:%.4f, total_price:%.4f" \
                %(self.order_id, self.status, self.price, self.deal_amount, self.avg_price * self.deal_amount)