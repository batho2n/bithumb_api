.SUFFIXES: .c.cpp.o

GCC				= gcc
GXX				= g++
AR				= ar
MKDIR			= mkdir -p
CD				= cd
CP				= cp -R
RM				= rm -rf
LN				= ln -f -s

CFLAGS			= -std=c++11 -Wall -I. -DTTS_DEBUG -DRAW_FEATURE -DUNIX -DLINUX -D_REENTRAN

LIBS			= -L/usr/lib64 -L/usr/lib64/openssl -lcurl -lcrypto
INCS			= -I/usr/include

TRADING_OBJS	= xcoin_api_client.o jsoncpp.o
TRADING			= coin_trading.exe


all: build

build: $(TRADING_OBJS) 
	$(GXX) -o $(TRADING) $(TRADING_OBJS) $(LIBS)

.c.o:
	$(GCC) $(INCS) $(CFLAGS) -o $@ -c $<

.cpp.o:
	$(GXX) $(INCS) $(CFLAGS) -o $@ -c $<

exec:
	./$(TRADING) -t sell -c ETH -u 0.0000001

clean:
	$(RM) $(TRADING_OBJS) $(TRADING_EXE)

#sudo yum install -y openssl-devel

.PHONY: all build exec clean; 
