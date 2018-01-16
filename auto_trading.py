#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @brief 	Coint Trading File using XCoin API-call(for Python 2.x, 3.x)
# @author	batho2n
# @date		2018.01.14
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
import time

def Usage (argv):
	print argv + " [options]"
	print ""
	print "  [Ex] " + argv + " -t sell -c BTC -u 1.42"
	print "  [options]"
	print "      -t		거래 방법 선택 (sell, buy, wallet)"
	print "      -c		거래 코인 선택 (BTC, ETH, DASH, LTC, ETC, XRP, BCH, "
	print "        						XMR, ZEC, QTUM, BTG, EOS)"
	print "      -u		거래량(코인 기준, 거래최소량 있음, 소수4자리까지 가능)"
	
def Check_Curr_Status(private_params):
	API = "/public/ticker/" + private_params['currency']
	print("Bithumb Public API URI('" + API + "') Request...");
	result = api.xcoinApiCall(API, private_params);
	print result
	print "- Status Code: " + result["status"]
	print "- Sell Price: " + result["data"]["sell_price"]
	print "- Buy Price: " + result["data"]["buy_price"]
	print ""
	return 0


def Print_Api_Error (result):
	print "Status: " + str(result["status"])
	print "Message: " + result["message"]
	return

def Print_Wallet(result, currency):
	print ""
	print " = = = Wallet = = ="
	print currency + ": " + result["data"]["available_"+currency.lower()]
	print "KRW: " + str(format(result["data"]["available_krw"], ","))
	return

def Print_Market_Result(result):
	print "units: " + result["data"][0]["units"]
	print "price: " + result["data"][0]["price"] + " KRW / 1 " +  private_params["currency"]
	return

def API_Init(api_key, api_secret):
	return XCoinAPI(api_key, api_secret);

def Set_Req_Params(trading, coin, unit, krw, order_id):
	API = ""
	how = ""
	if trading == "sell":
		API = "/trade/market_sell"
	elif trading == "buy":
		API = "/trade/market_buy"
	elif trading == "order_sell":
		API = "/trade/place"
		how = "ask"
	elif trading == "order_buy":
		API = "/trade/place"
		how = "bid"
	elif trading == "cancel_sell":
		API = "/trade/cancel"
		how = "ask"
	elif trading == "cancel_buy":
		API = "/trade/cancel"
		how = "bid"
	
	#API 호출용 파라미터들
	private_params = {
		"currency"			: coin,
		"units"				: float(unit),
		"order_currency"	: coin,
		"payment_currency"	: "KRW",
		"price"				: int(krw),
		"type"				: how,
		"order_id"			: order_id
	};

	return API, private_params


def Check_Wallet(api, private_params, API):
	result = api.xcoinApiCall(API, private_params)
	if result["status"] != "0000":
		Print_Api_Error(result)
		return -1
	else:
		Print_Wallet(result, private_params["currency"])
		return 0

def Trading(api, private_params, API):
	print "Bithumb Private API URI(" + API + ") Request..."
	result = api.xcoinApiCall(API, private_params)
	print result

	if result["status"] != "0000":			# Request Error 일때
		Print_Api_Error(result)
		if result["message"] == "Please try again":						# Connetion 에러인 경우 !! 다시 시도하기위해서 에러코드 분리
			return -1
		else:															# 일반적인 에러인 경우 정상 종료를 위한 에러코드 분리 
		    return -2
	else:									# Request 성공일 경우
		if API == "/trade/market_buy" or API == "/trade/market_sell":	# market_buy, market_sell 일 경우
			Print_Market_Result (result)
		elif API == "/trade/place":										# order 주문일 경우
			print "order_id: " + result["order_id"]
			print("Order Succes !! ")
		elif API == "/trade/cancel":									# order 취소일 경우
			print("Cancel Succes !! ")
	return 0

if __name__ == '__main__':

	coin = 'XRP'	# 거래 코인 종류
	sale = ""		# 주문 방법 sell: 시장가 판매, buy: 시장가 구매, order: 가격책정후 등록, cancel: 등록 구매 취소
	API = ""		#
	unit = "0"		# 구매및 판매 코인 양소수점 4자리까지
	krw = "0"		# order에서 사용할 코인당 단가
	how = ""		# order에서 사용할 거래 방법, bid: 살때, ask: 팔때
	order_id = ""	# order_id(구매/판매 등록시 나온 id 이를 통해서 취소나 조회 가능)
	err_code = 0
	if len(sys.argv) < 5:
		Usage(sys.argv[0])
		sys.exit(0)

	options, args = getopt.getopt(sys.argv[1:], 'c:u:t:k:o:h')
	for opt, p in options:
		if opt == '-c':
			coin = p
		elif opt == '-u':
			unit = p
		elif opt == '-t':
			trading = p
		elif opt == '-k':
			krw = p
		elif opt == '-o':
			order_id = p
		elif opt == '-h':
			Usage(sys.argv[0])
			sys.exit(0)
		else:
			print 'Unknown option'
			Usage(sys.argv[0])
			sys.exit(0)


	print ""
	print " Trading Coin: " + coin + ",  Trading mode: " + trading+ ", Trading volume: " + unit + " " + coin
	print " BITHUMB API Initialization"
	api_key = "575c2465ffba4a5ecfc834997d7804e5";
	api_secret = "acbc59e9accd146a8bb96b83b65460ef";
	api = API_Init(api_key, api_secret)
		
	
	# krw=0일때 어떻게 할지 알고리즘 필요함!
	API, private_params = Set_Req_Params(trading, coin, unit, krw, order_id)
	
	print "     =====Starting Trading======"
	print ""
	
	if trading != "wallet":

		print ""
		print " Trading !!! "
		for i in range(10):
			err_code = Trading(	api, private_params, API)
			if err_code == -1:                  # Connect error, 다시 시작 GoGo
				print "[ERR] Trading() " + str(err_code)
				time.sleep(0.05)
			elif err_code != 0:                 # Other error, 돈이부족, 없는 구매 오더등등 등 얼른 멈춰
				print "[ERR] Trading() Stop " + str(err_code)
				break
			else:
				break
		
	wallet_params = {
		"currency"				: coin
	};
	err_code = Check_Wallet(api, wallet_params, "/info/balance")
	if err_code != 0:
		print "[ERR] Check_Wallet() " + str(err_code)

	print ""
	print "     =====Finish Trading======"
	sys.exit(0)
