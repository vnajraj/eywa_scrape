DESTDIR := build/scraper
BUILD := runscraperzip
VENV := venv

build: clean_build
	mkdir -p $(DESTDIR)
	echo -e "from scrape import main\nmain()" > $(DESTDIR)/__main__.py 
	cp *.py $(DESTDIR)
	python -m zipapp $(DESTDIR) -o $(BUILD)

clean_build:
	rm -rf $(shell dirname $(DESTDIR))

clean: 
	$(MAKE) clean_build
	rm -rf venv __pycache__

resetenv:
	rm -rf $(VENV)
	python -m venv $(VENV)
	$(VENV)/bin/python -m pip install -r requirements.txt

run: 
	$(VENV)/bin/python $(BUILD)

test: build resetenv run
