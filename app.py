from coinbase.wallet.client import Client
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
account_id = os.getenv("ACCOUNT_ID")
client = Client(api_key, api_secret)
accounts = client.get_accounts()

def calculate_profit_loss():
	btc_wallet = get_btc_wallet()
	price_now = float(client.get_spot_price(currency_pair="BTC-GBP")["amount"])
	btc_owned = float(str(btc_wallet["balance"]).replace("BTC", ""))
	worth_now = price_now * btc_owned
	buys = client.get_buys(account_id).data
	money_spent = calculate_money_spent(buys)
	profit_loss = float((-1 + (worth_now / money_spent)) * 100)

	return profit_loss

def get_btc_wallet():
	for wallet in accounts.data:
		if wallet["currency"] == "BTC":
			return wallet

def calculate_money_spent(buys):
	money_spent = 0
	for buy in buys:
		buy_date = datetime.strptime(buy["created_at"][:-10], '%Y-%m-%d').date()
		start_date = datetime.strptime('2020-03-28', '%Y-%m-%d').date()
		if buy_date >= start_date and buy["status"] == "completed":
			money_spent += float(str(buy["total"]).replace("GBP", ""))

	return money_spent

profit_loss = calculate_profit_loss()

print("Current profit/loss: %.4f%%" % profit_loss)