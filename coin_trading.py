#! /usr/bin/env python
#
# @brief XCoin API-call sample script (for Python 2.x, 3.x)
#
# @author btckorea
# @date 2017-04-14
#
# @details
# First, Build and install pycurl with the following commands::
# (if necessary, become root)
#
# https://pypi.python.org/pypi/pycurl/7.43.0#downloads
#
# tar xvfz pycurl-7.43.0.tar.gz
# cd pycurl-7.43.0
# python setup.py --libcurl-dll=libcurl.so install
# python setup.py --with-openssl install
# python setup.py install
#
# @note
# Make sure current system time is correct.
# If current system time is not correct, API request will not be processed normally.
#
# rdate -s time.nist.gov
#

import sys
from xcoin_api_client import *
import pprint
import getopt

#575c2465ffba4a5ecfc834997d7804e5	acbc59e9accd146a8bb96b83b65460ef
api_key = "575c2465ffba4a5ecfc834997d7804e5";
api_secret = "acbc59e9accd146a8bb96b83b65460ef";
api = XCoinAPI(api_key, api_secret);
rgParams = {
	"order_currency" 	: "XRP",
	"payment_currency" 	: "KRW",
	"offset"			: 0,
	"count"				: 1,
	"searchGb"			: "1",
	"currency"			: "XRP",
	"units"				: 10
};


#
# Public API
# /public/ticker
# /public/recent_ticker
# /public/orderbook
# /public/recent_transactions

def Check_Curr_Status(API):
	print(type(rgParams))
	print("Bithumb Public API URI('/public/ticker') Request...");
	result = api.xcoinApiCall(API, rgParams);
	print result
	print "- Status Code: " + result["status"]
	print "- Opening Price: " + result["data"]["opening_price"]
	print "- Closing Price: " + result["data"]["closing_price"]
	print "- Sell Price: " + result["data"]["sell_price"]
	print "- Buy Price: " + result["data"]["buy_price"]
	print ""
	return 0


#
# Private API
#
# endpoint => parameters
# /info/current
# /info/account
# /info/balance
# /info/wallet_address

#print("Bithumb Private API URI('/info/account') Request...");
#result = api.xcoinApiCall("/info/account", rgParams);
#print("- Status Code: " + result["status"]);
#print("- Created: " + result["data"]["created"]);
#print("- Account ID: " + result["data"]["account_id"]);
#print("- Trade Fee: " + result["data"]["trade_fee"]);
#print("- Balance: " + result["data"]["balance"]);
#
#
#print("Bithumb Private API URI('/info/balance') Request...");
#result = api.xcoinApiCall("/info/balance", rgParams);
#print(result)
#print("- Status Code: " + result["status"]);
#print result["data"]
#print("- Total KRW " + result["data"]);

def User_Transactions(API):
	print "Bithumb Private API URI(" + API + ") Request..."
	result = api.xcoinApiCall(API, rgParams)
	print result

	return 0

def User_Transactions(API):
	print "Bithumb Private API URI(" + API + ") Request..."
	result = api.xcoinApiCall(API, rgParams)
	print result

	return 0

def Market_Sell():
	print "Bithumb Private API URI('/info/market_sell') Request..."
	result = api.xcoinApiCall("/info/market_sell", rgParams)
	if result["status"] != "0000":
		print "Status: " + result["status"]
		print "Message: " + result["message"]
		return -1
	else:
		print "order_id: " + result["data"]["order_id"]
		print "cont_id: " + result["data"]["cont_id"]
		print "units: " + result["data"]["units"]
		print "price: " + result["data"]["price"] + " KRW / 1 " +  rParams["currency"]
		print "total: " + result["data"]["total"] + " KRW"

	return 0

def Market_Buy():
	print "Bithumb Private API URI('/info/market_sell') Request..."
	result = api.xcoinApiCall("/info/market_sell", rgParams)
	if result["status"] != "0000":
		print "Status: " + result["status"]
		print "Message: " + result["message"]
		return -1
	else:
		print "order_id: " + result["data"]["order_id"]
		print "cont_id: " + result["data"]["cont_id"]
		print "units: " + result["data"]["units"]
		print "price: " + result["data"]["price"] + " KRW / 1 " +  rParams["currency"]
		print "total: " + result["data"]["total"] + " KRW"

	return 0

if __name__ == '__main__':

	coin = 'XRP'
	vol = ''
	sale = ''
	
	options, args = getopt.getopt(sys.argv[1:], 'c:w:m:')
	for opt, p in options:
		if opt == '-c':
			coin = p
		elif opt == '-w':
			vol = p
		elif opt == '-m':
			sale = p
		else:
			print 'Unknown option'
			sys.exit(0)

	print ""
	print "	[Trading Coin: " + coin + ",  Trading mode: " + sale + ", Trading volume: " + krw + "KRW]"
	print ""
	print "=====Starting Trading======"
	print ""
	
	if sale == "sell":
		err_code = Market_Sell()
		if err_code != 0:
			print "[ERR] Market_Sell() " + str(err_code)
			sys.exit(0)
	elif sale == "buy":
		err_code = Market_buy
		if err_code != 0:
			print "[ERR] Market_Buy() " + str(err_code)
			sys.exit(0)

	sys.exit(0)
