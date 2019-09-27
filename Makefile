.PHONY: test unit lint style eslint checkdocs coverage upload outdated

all: test

test:
	py.test --cov=./ --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF
	coverage html

lint:
	py.test --pylint -m pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

black:
	black -S -l 100 -t py36 rstxt.py tests
