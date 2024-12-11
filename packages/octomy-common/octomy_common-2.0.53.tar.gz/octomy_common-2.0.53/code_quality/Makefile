ROOT_DIR:=$(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")
APP_DIR:=${ROOT_DIR}/..

TESTS_DIR:=${APP_DIR}/tests

.PHONY: h all flake pylint mypy coverage black low-hanging help

h: help

all: black flake
# mypy detects some false positives, disabled for now
#pylint is broken, disabled for now

black:
	black -l 999 -t py37 "${APP_DIR}"
	black -l 999 -t py37 "${TESTS_DIR}"

flake:
	flake8 --exit-zero --config .flake8 "${APP_DIR}"
	flake8 --exit-zero --config .flake8 "${TESTS_DIR}"

pylint:
	pylint --exit-zero --rcfile pylintrc --output-format=colorized "${APP_DIR}"
	pylint --exit-zero --rcfile pylintrc --output-format=colorized "${TESTS_DIR}"

mypy:
	mypy --ignore-missing-imports "${APP_DIR}"
	mypy --ignore-missing-imports "${TESTS_DIR}"


coverage:
	python -m pytest --junitxml=junit-results.xml --cov="${APP_DIR}" --cov-report=xml --cov-report=html unit

low-hanging:
	flake8 --select=F401 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=F403 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=F821 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=F841 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=W0107 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=W0706 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"
	flake8 --select=W0105 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"

unused:
	flake8 --select=F401 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"

undefined:
	flake8 --select=F821 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"

space:
	flake8 --select=E101 --max-complexity 10 --exclude build,junk --exit-zero "${APP_DIR}"

############### Help ####################

help:
	@echo ""
	@echo " Available targets:"
	@echo ""
	@echo " + make help          Show this help"
	@echo " + make all           Run all targets"
	@echo " + make black         Run black"
	@echo " + make flake         Run flake"
	@echo " + make mypy          Run mypy"
	@echo " + make pylint        Run pylint"
	@echo " + make coverage      Run coverage"
	@echo " + make low-hanging   Run flake with most low-hanging warnings only"
	@echo " + make unused        Run flake with unused warnings only"
	@echo " + make undefined     Run flake with undefined warnings only"
	@echo " + make space         Run flake with space warnings only"
	@echo ""

