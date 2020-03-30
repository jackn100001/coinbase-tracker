#! /usr/bin/python3

from coinbase.wallet.client import Client
from datetime import datetime
from dotenv import load_dotenv
import os

class Tracker:
	def __init__(self):
		load_dotenv()
		self.api_key = os.getenv("API_KEY")
		self.api_secret = os.getenv("API_SECRET")
		self.account_id = os.getenv("ACCOUNT_ID")
		self.client = Client(self.api_key, self.api_secret)
		self.accounts = self.client.get_accounts()

	def calculate_profit_loss(self):
		btc_wallet = self.get_btc_wallet()
		price_now = float(self.client.get_spot_price(currency_pair="BTC-GBP")["amount"])
		btc_owned = float(str(btc_wallet["balance"]).replace("BTC", ""))
		worth_now = price_now * btc_owned
		buys = self.client.get_buys(self.account_id).data
		money_spent = self.calculate_money_spent(buys)
		profit_loss = float((-1 + (worth_now / money_spent)) * 100)

		return profit_loss

	def get_btc_wallet(self):
		for wallet in self.accounts.data:
			if wallet["currency"] == "BTC":
				return wallet

	def calculate_money_spent(self, buys):
		money_spent = 0

		for buy in buys:
			buy_date = datetime.strptime(buy["created_at"][:-10], '%Y-%m-%d').date()
			start_date = datetime.strptime('2020-03-28', '%Y-%m-%d').date()
			if buy_date >= start_date and buy["status"] == "completed":
				money_spent += float(str(buy["total"]).replace("GBP", ""))

		return money_spent