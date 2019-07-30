help:
	@echo "Please use \`make <CMD>' where <CMD> is one of"
	@echo "  build"
	@echo "  up"

build:
	docker build -t btc-producer .

up:
	docker run -d btc-producer -e CLIENT_ID='khame' BOOSTRAP_SERVER=localhost:$(PORT)

BOOSTRAP_SERVER ?= 9091