#!/usr/bin/python
# -*- coding: utf-8 -*-

# @file         XRP_checking.py
# @breif        XRP coing 시세 체크
# @date         2018-01-09
# @author       batho2n@gmail.com
#
# Copyroght (C) 2018 batho2n
# All Right Reserved

import os
import sys

import threading
import json

from bs4 import BeautifulSoup
import urllib
import re
import requests
import pprint

import pyaudio
import wave

import datetime
import time

#Conins
XRP = 'XRP'
#URL_BASE = 'https://api.bithumb.com/public/ticker/'
URL_BASE = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/lines?code=CRIX.UPBIT.'

URL_CSV = 'https://www.bithumb.com/resources/csv/'
TRADE_ACTION        = '_xcoinTradeAltcoin.json'
TRADE_ACTION_01M    = '_xcoinTradeAltcoin_minute.json'
TRADE_ACTION_01H    = '_xcoinTradeAltcoin_minute_01H.json'
TRADE_ACTION_06H    = '_xcoinTradeAltcoin_minute_06H.json'
TRADE_ACTION_12H    = '_xcoinTradeAltcoin_minute_12H.json'
TRADE_ACTION_30M    = '_xcoinTradeAltcoin_minute_30m.json'

WAV_FILE = 'alarm.wav'

# UTC 시간
utc_time = datetime.datetime.utcnow()
# 현재 로컬 시간
kor_time = datetime.datetime.now()
time_diff = kor_time - utc_time


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

def Check_Old_Coin(file_name):
    print('====All Chart by 1 Hour====')
    #os.system('rm '+ file_name +'*')
    os.system('wget '+URL_CSV + file_name)
    json_data=open(file_name).read()
    datas = json.loads(json_data)
    #os.system('rm '+ file_name +'*')

    # 시간 변환
    # data[i] = [date, open, close, high, low, volume]
    for data in datas :
        time_stamp = data[0]
        time_trans = time.strftime("%a %d %b %Y %H:%M:%S KOT", time.gmtime(time_stamp / 1000.0 + 9 * 3600))
        p_open  = data[1]
        p_close = data[2]
        p_high  = data[3]
        p_low   = data[4]
        print time_trans + ' : ' +  str(p_open) + ' --> ' + str(p_close) ,
        if (p_close - p_open > 0 ):
            print '^'
        else :
            print 'v'

    return


def Check_Curr_Coin():
    #threading.Timer(2, Check_Curr_Coin).start()

    data = urllib.urlopen(URL_BASE+XRP).read(2000)
    json_data = json.loads(data)
    print(json_data)
    time_stamp = int(json_data[u'data'][u'date'])
    time_trans = time.strftime("%a %d %b %Y %H:%M:%S KOT", time.gmtime(time_stamp / 1000.0 + 9 * 3600))
    p_open  = int(json_data[u'data'][u'opening_price'])
    p_close = int(json_data[u'data'][u'closing_price'])
    p_high  = int(json_data[u'data'][u'min_price'])
    p_low   = int(json_data[u'data'][u'max_price'])
    p_avg   = int(round(float(json_data[u'data'][u'average_price'])))
    p_delta = p_close - p_open
    if (p_delta > 0 ):
        p_flag = '^'
    elif (p_delta < 0) :
        p_flag = 'v'
    else:
        p_flag = '-'
    
    print ('{} : {} --> {} {}'.format(time_trans, p_open, p_close, p_flag))


    #Play_Wav()
    
    return

if __name__ == '__main__':
    print(sys.argv)

    print("STARTING...")
    #Check_Old_Coin(XRP + TRADE_ACTION_01H)
    Check_Curr_Coin()
