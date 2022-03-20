

VENV_DIR = .venv
ACTIVATE = . ./$(VENV_DIR)/bin/activate
PIDFILE = $(abspath .pid)

flags=

install: $(VENV_DIR)
	@$(ACTIVATE) && python3 -m pip install --upgrade pip
	@$(ACTIVATE) && pip install -e .

$(VENV_DIR):
	@[ "$(shell which virtualenv)" = '' ] && ( \
		echo sudo apt install python3-virtualenv \
		&& sudo apt install python3-virtualenv \
	) || true
	@python3 -m virtualenv $(VENV_DIR)

start:
	@$(ACTIVATE) && ticu run --token=$$(cat .token) --pidfile=$(PIDFILE) &

dev:
	@$(ACTIVATE) && ticu run --token=$$(cat .token) --pidfile=$(PIDFILE) --dev

test:
	@$(ACTIVATE) && pytest -v -s --show-capture=all $(flags)

stop:
	@if [ -f "$(PIDFILE)" ];then \
		echo "[pid=$$(cat $(PIDFILE))] Killing TiCu" ; \
		kill $$(cat $(PIDFILE)) ; \
	else \
		echo "Not running." ; \
	fi

kill:
	@echo "Killing all instances of TiCu"
	@-killall ticu