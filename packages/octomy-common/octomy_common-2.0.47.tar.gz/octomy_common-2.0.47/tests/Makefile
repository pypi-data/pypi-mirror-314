ROOT_DIR:=$(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")
APP_DIR:=${ROOT_DIR}/..
TESTS_DIR:=${APP_DIR}/tests
TEST_CMD:=python -m pytest

.PHONY: h all devops unit integration load help

h: help

all: unit integration load

devops: unit

unit:
	$(TEST_CMD) -vv unit

integration:
	$(TEST_CMD) -vv integration

load:
	$(TEST_CMD) -vv load
############### Shortcuts ####################

utils:
	$(TEST_CMD) -vv unit/test_utils.py

openscad:
	$(TEST_CMD) -vv unit/test_openscad.py

parts:
	$(TEST_CMD) -vv unit/test_parts.py

############### Help ####################

help:
	@echo ""
	@echo " General targets:"
	@echo ""
	@echo " + make help            Show this help"
	@echo " + make all             Run all tests"
	@echo " + make devops          Run devops tests"
	@echo " + make load            Run load tests (WIP)"
	@echo ""
	@echo "Unit targets:"
	@echo ""
	@echo " + make unit            Run unit tests"
	@echo " + make utils           Run unit tests for utils"
	@echo " + make openscad        Run openscad unit tests"
	@echo " + make parts           Run parts unit tests"
	@echo ""
	@echo "Integration targets:"
	@echo ""
	@echo " + make integration     Run integration tests"
	@echo ""
	@echo "Component targets:"
	@echo ""
