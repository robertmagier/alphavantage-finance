all:
	echo "Nothing to do"
freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt
test:
	pytest -v ./tests
install:
	pip install -r requirements.txt

