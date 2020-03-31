#! /usr/bin/python3

from datetime import datetime

class Tracker:
	def __init__(self, client, account_id):
		self.client = client
		self.account_id = account_id
		self.btc_wallet = client.get_account(account_id)

	def calculate_profit_loss(self):
		price_now = float(self.client.get_spot_price(currency_pair="BTC-GBP")["amount"])
		btc_owned = float(str(self.btc_wallet["balance"]).replace("BTC", ""))
		worth_now = price_now * btc_owned
		buys = self.client.get_buys(self.account_id).data
		money_spent = self.calculate_money_spent(buys)
		profit_loss = float((-1 + (worth_now / money_spent)) * 100)

		return profit_loss

	def calculate_money_spent(self, buys):
		money_spent = 0

		for buy in buys:
			buy_date = datetime.strptime(buy["created_at"][:-10], '%Y-%m-%d').date()
			start_date = datetime.strptime('2020-03-28', '%Y-%m-%d').date()
			if buy_date >= start_date and buy["status"] == "completed":
				money_spent += float(str(buy["total"]).replace("GBP", ""))

		return money_spent