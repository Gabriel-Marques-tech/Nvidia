install:
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

scraping-install:
	.venv/bin/playwright install chromium

run-api:
	.venv/bin/uvicorn api.main:app --reload

neo4j-up:
	docker compose up neo4j -d

neo4j-down:
	docker compose down neo4j
