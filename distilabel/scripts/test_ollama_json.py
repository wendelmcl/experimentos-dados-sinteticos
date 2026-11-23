
import json
from pathlib import Path
from distilabel.models.llms import OllamaLLM

BASE = Path(__file__).resolve().parents[2]
SAIDA = BASE / "results/distilabel/DL-01/json_mode_probe.json"

llm = OllamaLLM(
    model="qwen3:0.6b",
    host="http://localhost:11434",
    timeout=120
)

instrucao = """
Gere exatamente um evento FICTÍCIO de login malsucedido.

Responda somente com um objeto JSON, sem Markdown.

Utilize exatamente os campos:
- timestamp: data e hora em formato ISO 8601
- event_type: "failed_login"
- username: identificador fictício do usuário
- source_ip: endereço IPv4 de documentação
- status: "failure"

Não acrescente outros campos.
Não classifique o evento como ataque.
"""

llm.load()

try:
    resultado = llm.generate_outputs(
        inputs=[[{"role": "user", "content": instrucao}]],
        num_generations=1,
        format="json",
        options={
            "temperature": 0,
            "seed": 42,
            "num_predict": 200
        }
    )
finally:
    llm.unload()

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(
    json.dumps(resultado, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Resultado da geração:")
print(json.dumps(resultado, ensure_ascii=False, indent=2))
print("\nArquivo salvo em:", SAIDA)