#! /usr/bin/python3

from coinbase.wallet.client import Client
from tracker import Tracker
from dotenv import load_dotenv
import os
import json

def main():
	load_dotenv()

	client = initialize_client()
	account_id = os.getenv("BTC_ACCOUNT_ID")
	tracker = Tracker(client, account_id)
	show_tracker_info(tracker)
	
def show_tracker_info(tracker):
	tracker.show_spent_worth()
	print()
	tracker.show_profit_loss_percentage()
	tracker.show_profit_loss_difference()

def initialize_client():
	api_key = os.getenv("API_KEY")
	api_secret = os.getenv("API_SECRET")

	return Client(api_key, api_secret)

if __name__ == "__main__":
	main()