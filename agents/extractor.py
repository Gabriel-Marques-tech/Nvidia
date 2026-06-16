import json
from pathlib import Path
from models.startup import Startup
from groq import Groq
from config.settings import settings
from models.startup import Startup, AIClassification, Evidence

client = Groq(api_key=settings.groq_api_key)

def extract_startup(raw_json_path: str) -> Startup:
	data = json.loads(Path(raw_json_path).read_text())
	text = "\n\n".join(p["text"] for p in data["pages"])

	client.chat


if __name__ == "__main__":
	result = extract_startup("data/raw/creditas.json")
	print(result)