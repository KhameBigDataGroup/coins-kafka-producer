help:
	@echo "Please use \`make <CMD>' where <CMD> is one of"
	@echo "  build"
	@echo "  up"

build:
	docker build -t btc-producer .

up:
	docker rm -f btc-producer
	docker run --name btc-producer --restart always -idt -v ./checkpoints:/opt/producer/checkpoints -e CLIENT_ID='khame' -e BOOSTRAP_SERVER=172.17.0.1:$(PORT) btc-producer

PORT ?= 9092