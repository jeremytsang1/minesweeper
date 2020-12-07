run: install clean test
	python main.py

install:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*__pycache__' -exec rm -r --force {} +

test: clean
	python -m unittest discover -b
