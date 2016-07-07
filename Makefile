.PHONY: all clean-pyc test doc

all: clean-pyc test doc

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	@echo 'Tests'
	nosetests -v --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=vision vision

doc:
	@echo 'Docs'
	sphinx-apidoc -fe -o docs/source/ vision vision/tests
	cd docs && $(MAKE) html