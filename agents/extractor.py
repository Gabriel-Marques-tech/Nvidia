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
	Schema = Startup.model_json_schema()

	response = client.chat.completions.create(
		model=settings.llm_model,
		messages= [
			{
			"role": "system",
			"content": """Você é um analista técnico especializado em avaliar startups de IA brasileiras.

Pergunta norteadora do projeto: Como a NVIDIA pode identificar, atrair e nutrir startups brasileiras AI-native num contexto onde grandes labs (OpenAI, Anthropic, Google) ameaçam startups dependentes apenas de wrappers de LLM?

Seu objetivo é extrair informações técnicas que permitam identificar gaps na stack de IA da startup e recomendar tecnologias NVIDIA adequadas.

Critérios de classificação:
- AI-native: IA é o produto principal, tem dados proprietários, modelos próprios ou pipeline de ML em produção, não depende exclusivamente de APIs externas de LLM
- AI-enabled: usa IA como feature auxiliar, produto principal não é IA
- non-AI: IA ausente ou superficial

Sempre retorna JSON válido. Seja preciso com founders (apenas fundadores da empresa, não clientes). Para tech_stack, liste linguagens de programação, frameworks, ferramentas de ML/AI e infraestrutura identificados."""
			},
			{
				"role": "user",
				"content": f"""Analise o texto abaixo coletado do site e GitHub da startup e extraia as informações técnicas.

TEXTO COLETADO:
{text}

Retorne JSON seguindo exatamente este schema:
{json.dumps(Schema, ensure_ascii=False, indent=2)}

Para evidence, inclua trechos específicos do texto que justifiquem a classificação e a tech_stack identificada."""
			}
		],
		response_format={"type": "json_object"}


	)

	result = json.loads(response.choices[0].message.content)
	return Startup(**result)


if __name__ == "__main__":
	result = extract_startup("data/raw/cortex_intelligence.json")
	print(result)