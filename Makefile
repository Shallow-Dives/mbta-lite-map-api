.PHONY: devel-install install format format-check devel-start devel-build devel-install test

devel-install:
	@pip install -r requirements.txt -r develop/requirements.txt

install:
	@pip install -r requirements.txt

format:
	@black api
	@black tests
	@isort api
	@isort tests

format-check:
	@black api --check
	@flake8 api --count --show-source --statistics --ignore=E203,W503 --max-line-length 88

devel-start:
	@bash ./start.sh

devel-build:
	@docker build . -t mbta-lite-map-api

devel-run:
	@docker run --rm -t -i -p 8080:8080 mbta-lite-map-api

test:
	@pytest tests
