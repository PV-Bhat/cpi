
.PHONY: setup sanitize traces harness figures all docker

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .

sanitize:
	cpi-kit sanitize logs_raw public_logs --names Pruthvi MAMATHA

traces:
	cpi-kit traces --out traces --audit audit

harness:
	cpi-kit harness --config docs/example_config.yml --out traces/runs --audit audit/runs.audit.jsonl

figures:
	cpi-kit figures

all: sanitize traces harness figures
