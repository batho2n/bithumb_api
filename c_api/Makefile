

all: build exec

build:
	g++ -I/usr/include -L/usr/lib64 -L/usr/lib64/openssl -lcurl -lcrypto -o xcoin_api_client xcoin_api_client.cpp

exec:
	./xcoin_api_client
