

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
	@nohup sh -c "$(ACTIVATE) && suno run --token=$$(cat .token) --pidfile=$(PIDFILE) 2>&1 &"

dev:
	@$(ACTIVATE) && suno run --token=$$(cat .token) --pidfile=$(PIDFILE) --dev

raw_test:
	$(ACTIVATE) && pytest -v -s --show-capture=all

test:$(addprefix do-,$(shell ls tests/test_*))

./do-tests/test_%:
	@for func in $(shell \
		grep -Po "async def test_[a-zA-Z0-9_]+" tests/test_$* \
		| cut -d ' ' -f 3 \
	); do \
		$(MAKE) ./test-function-tests/test_$* func=$${func} --no-print-directory ; \
	done
./test-function-tests/test_%:
	@export x="$(shell \
		$(ACTIVATE) \
		&& pytest -q tests/test_$* -k $(func) 2> /dev/null \
		| grep -Po 'passed|failed' \
	)" && [ "$${x}" = "passed" ] && color="32" || color="31" \
		&& echo "\033[$${color}m[$${x}]\033[m $(func)" \
	;

stop:
	@if [ -f "$(PIDFILE)" ];then \
		echo "[pid=$$(cat $(PIDFILE))] Killing TiCu" ; \
		kill $$(cat $(PIDFILE)) ; \
	else \
		echo "Not running." ; \
	fi

kill:
	@echo "Killing all instances of Supernova"
	@-killall suno

.PHONY:tests/test_* test-function-*