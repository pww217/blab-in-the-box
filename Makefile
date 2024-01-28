dev:
	uvicorn api:app --reload --log-level info

debug:
	uvicorn api:app --reload --log-level debug

run:
	python cli.py