.PHONY: build start

PYTHON := python3
EXEC   := main.py

DEPS   := helper_func
LIBS   := $(DEPS)/loginc

all: build

build: $(LIBS)
	make -C $(DEPS)

start: build
	$(PYTHON) $(EXEC)
