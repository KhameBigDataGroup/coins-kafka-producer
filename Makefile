help:
	@echo "Please use \`make <CMD>' where <CMD> is one of"
	@echo "  build"
	@echo "  up"

build:
	docker build -t btc-producer .

up:
	docker run -d btc-producer -v ./checkpoints:/opt/producer/checkpoints -e CLIENT_ID='khame' BOOSTRAP_SERVER=172.17.0.1:$(PORT)

PORT ?= 9091