.PHONY: init test install install-dev help clean install-dependencies

PYTHON3_OK := $(shell python --version 2>&1)
BREW_OK := $(shell brew -v 2>&1)

#init: venv/bin/activate
#	./venv/bin/pip install -r requirements.txt

#setup: requirements.txt
#	./venv/bin/pip install -r requirements.txt

# This will check for the correct brew and python3 packages, and
#  attempt to install them if they aren't found.
install-dependencies:
ifeq ('$(PYTHON3_OK)','')
ifeq ('$(BREW_OK)','')
	@echo "Installing brew.."
	curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh | bash
	@echo "-----------------"
	@echo $(shell brew -v 2>&1)
	@echo "-----------------"
endif
	@echo "Installing python.."
	brew install python@3.13
	pyenv install 3.13.1
	pyenv local 3.13.1
	@echo "-----------------"
	@echo $(shell python --version 2>&1)
	@echo "-----------------"
endif
	@echo $(shell brew -v 2>&1)
	@echo $(shell python --version 2>&1)

# After the dependencies are installed/verified, this will actiate
# the environment just using venv/bin/activate
install:
	make install-dependencies
	make venv/bin/activate
#	pyenv install 3.13.1
	pyenv local 3.13.1
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install -e .
	make venv/bin/activate

install-dev:
	make install-dependencies
	make venv/bin/activate
#	pyenv install 3.13.1
	pyenv local 3.13.1
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install -e .[dev]
	make venv/bin/activate

# Enter the python3 environment, then install the packages in the
# requirements/common.txtfile.
venv/bin/activate:
	python3.13 -m venv venv

# Just a simple help output. Not sure this is even necessary
help:
	@echo "\\033[1mmake \\033[3minstall\\033[0m       \\033[2mInstalls the dependencies (python3, pip packages, etc)\\033[0m"
	@echo "\\033[1mmake \\033[3minstall-dev\\033[0m   \\033[2mInstalls the dev dependencies (regular packages, plus pytest, etc)\\033[0m"
	@echo "\\033[1mmake \\033[3mrun\\033[0m           \\033[2mRuns script with regular output\\033[0m"
	@echo "\\033[1mmake \\033[3mrun-debug\\033[0m     \\033[2mRuns script with debugging output\\033[0m"
	@echo "\\033[1mmake \\033[3mtest\\033[0m          \\033[2mRuns unit tests (must run make install-dev first)\\033[0m"
	@echo "\\033[1mmake \\033[3mclean\\033[0m         \\033[2mRemoves the pyenv and all python dependencies\\033[0m"

# Run the main script, once the packages are verified
run: venv/bin/activate
ifeq ('$(PYTHON3_OK)','')
	@echo "No python3 version found - run 'make install' first"
	exit 1
else
	./venv/bin/python -O main.py
endif

# Run the test cases - this does nothing right now
test: venv/bin/activate
	make install-dev
	@echo "\\nStarting tests...\\n"
	# venv/bin/python -m pytest -svvv tests/test_search_factory.py
	venv/bin/python -m pytest -vvv tests

# Remove anything installed via pip in this env.
clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf bin include build
