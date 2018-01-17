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
import threading

import pyaudio
import wave
import datetime
import time


WAV_FILE = 'alarm.wav'


def Usage (argv):
	print argv + " [options]"
	print ""
	print "  [Ex] " + argv + " -t sell -c BTC -u 1.42"
	print "  [options]"
	print "      -c		체크 코인 선택 (BTC, ETH, DASH, LTC, ETC, XRP, BCH, "
	print "        				    XMR, ZEC, QTUM, BTG, EOS)"
        print "      -k		알람을 알고 싶은 기준선!!! (원화)"
        print "      -d		오르는걸 체크할건지(over), 내리는걸 체크할건지(under)"

def Play_Wav():
    #define stream chunk
    chunk = 1024
    #open a wav format music  
    f = wave.open(WAV_FILE,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)  
    #read data  
    wav_data = f.readframes(chunk)  
    while wav_data:  
        stream.write(wav_data)
        wav_data = f.readframes(chunk)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    
    #close PyAudio  
    p.terminate()  
    return

def Print_Api_Error (result):
	print "Status: " + str(result["status"])
	print "Message: " + result["message"]
	return
	
def Check_Curr_Status(private_params):
	API = "/public/ticker/" + private_params['currency']
	result = api.xcoinApiCall(API, private_params);
	
	if result["status"] != "0000":
		Print_Api_Error(result)
		return -1, -1
	else:
		#print "- Closing Price: " + result["data"]["closing_price"]
		#print "- Sell Price: " + result["data"]["sell_price"]
		#print "- Buy Price: " + result["data"]["buy_price"]
		#print ""
		return 0, str( int( (int(result["data"]["closing_price"]) + int(result["data"]["sell_price"]) + int(result["data"]["buy_price"])) / 3))


def API_Init(api_key, api_secret):
	return XCoinAPI(api_key, api_secret);

def Set_Req_Params(coin):
	#API 호출용 파라미터들
	private_params = {
		"currency"			: coin,
	};

	return private_params


if __name__ == '__main__':

	coin = 'XRP'	# 거래 코인 종류
	API = ""		
	un_over = ""
	krw = ""
	err_code = 0
	if len(sys.argv) < 3:
		Usage(sys.argv[0])
		sys.exit(0)

	options, args = getopt.getopt(sys.argv[1:], 'c:k:d:h')
	for opt, p in options:
		if opt == '-c':
		    coin = p
		elif opt == '-k':
		    krw = p
		elif opt == '-d':
                    if p != "under" and p != "over":
                        Usage(sys.argv[0])
                        sys.exit(0)
                    else:
		        un_over = p
		elif opt == '-h':
		    Usage(sys.argv[0])
		    sys.exit(0)
		else:
		    print 'Unknown option'
		    Usage(sys.argv[0])
		    sys.exit(0)

	print ""
	print " BITHUMB API Initialization"
	api_key = "575c2465ffba4a5ecfc834997d7804e5";
	api_secret = "acbc59e9accd146a8bb96b83b65460ef";
	api = API_Init(api_key, api_secret)
	
	# krw=0일때 어떻게 할지 알고리즘 필요함!
	private_params = Set_Req_Params(coin)
	print "     =====Starting Checking======"
	print ""

	while 1:
		err_code, price = Check_Curr_Status(private_params)
                kor_time = datetime.datetime.now()
                print kor_time,
		print " " + coin +" Target: " + krw + " Current Price: " + price
		if un_over == "under" and int(price) <= int(krw) :
			print '%s' % ("* UNDER *\n" * 120)
                        Play_Wav()
                        Play_Wav()
                        Play_Wav()
			break
		elif un_over == "over" and int(price) >= int(krw) :
			print '%s' % ("* OVER *\n" * 120)
                        Play_Wav()
                        Play_Wav()
                        Play_Wav()
			break
		time.sleep(1)


	print ""
	print "     =====Finish Checking======"
	sys.exit(0)
