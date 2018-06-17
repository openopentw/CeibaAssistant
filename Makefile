.PHONY: build start

PYTHON := python3
EXEC   := main.py
CONF   := config.ini

DEPS   := helper_func
LIBS   := $(DEPS)/loginc

all: build

build:
	make -C $(DEPS)

start: build
	$(PYTHON) $(EXEC) --config $(CONF)
