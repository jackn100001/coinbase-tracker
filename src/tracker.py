#! /usr/bin/python3

from datetime import datetime

class Tracker:
	def __init__(self, client, account_id):
		self.client = client
		self.account_id = account_id

		self.btc_wallet = client.get_account(account_id)
		self.buys = client.get_buys(account_id).data
		self.price_now = float(client.get_spot_price(currency_pair="BTC-GBP")["amount"])
		self.btc_owned = float(str(self.btc_wallet["balance"]).replace("BTC", ""))

		self.profit_loss_percentage = self.calculate_profit_loss_percentage()
		self.profit_loss_difference = self.calculate_profit_loss_difference()

	def calculate_profit_loss_percentage(self):
		self.worth_now = self.price_now * self.btc_owned
		self.money_spent = self.calculate_money_spent()

		profit_loss_percentage = float((-1 + (self.worth_now / self.money_spent)) * 100)
		return profit_loss_percentage

	def calculate_profit_loss_difference(self):
		profit_loss_difference = self.worth_now - self.money_spent
		return profit_loss_difference

	def calculate_money_spent(self):
		money_spent = 0

		for buy in self.buys:
			buy_date = datetime.strptime(buy["created_at"][:-10], '%Y-%m-%d').date()
			start_date = datetime.strptime('2020-03-28', '%Y-%m-%d').date()
			if buy_date >= start_date and buy["status"] == "completed":
				money_spent += float(str(buy["total"]).replace("GBP", ""))

		return money_spent

	def show_profit_loss_percentage(self):
		print("Current profit/loss (%%): %.4f%%" % self.profit_loss_percentage)

	def show_profit_loss_difference(self):
		print("Current profit/loss (GBP): {:.2f}".format(self.profit_loss_difference))

	def show_spent_worth(self):
		print("Total spent (GBP): {:.2f}".format(self.money_spent))
		print("Current worth (GBP): {:.2f}".format(self.worth_now))