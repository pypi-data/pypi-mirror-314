test:
	python3 runtests.py

testc:
	coverage run runtests.py
	coverage report -m

lint:
	pylint vanityurls

clean:
	rm -rf dist
	rm -rf django_vanityurls.egg-info

build: clean
	python -m build

publish: build
	twine upload dist/*
