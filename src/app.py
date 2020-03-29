from tracker import Tracker
import json

def main():
	tracker = Tracker()
	profit_loss = tracker.calculate_profit_loss()
	print("Current profit/loss: %.4f%%" % profit_loss)

if __name__ == "__main__":
	main()