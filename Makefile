PYTHON3_OK := $(shell python3 --version 2>&1)
BREW_OK := $(shell brew -v 2>&1)

init: venv/bin/activate
	./venv/bin/pip install -r requirements.txt

setup: requirements.txt
	./venv/bin/pip install -r requirements.txt
	
install:
ifeq ('$(PYTHON3_OK)','')
ifeq ('$(BREW_OK)','')
	@echo "Installing brew.."
	curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh | bash
endif
	@echo "Installing python.."
	brew install python
endif
	@echo $(shell python3 --version 2>&1)
	@echo $(shell brew -v 2>&1)
	

venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

run: venv/bin/activate
	./venv/bin/python3 main.py

test: venv/bin/activate
	python3 -m pytest tests

clean:
	rm -rf __pycache__ 
	rm -rf venv
	rm -rf bin include build

.PHONY: init test