# allow specification of python version for devs. Examples:
#    make autoformat PYTHON_VERSION=python3.6
PYTHON_VERSION?=python3
VIRTUALENV=.venv

.PHONY: docs test autoformat clean

$(VIRTUALENV):
	virtualenv --python=$(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install -U pip setuptools
	$(VIRTUALENV)/bin/pip install -e '.[development]'

# run outside of tox because specifying a tox environment for py3.6+ is awkward
autoformat: $(VIRTUALENV)
	$(VIRTUALENV)/bin/isort --recursive tests/ globus_sdk_tokenstorage/ setup.py
	if [ -f "$(VIRTUALENV)/bin/black" ]; then $(VIRTUALENV)/bin/black tests/ globus_sdk_tokenstorage/ setup.py; fi

test: $(VIRTUALENV)
	$(VIRTUALENV)/bin/tox
docs: $(VIRTUALENV)
	$(VIRTUALENV)/bin/tox -e docs

clean:
	rm -rf $(VIRTUALENV) dist build *.egg-info .tox
