
import json
from pathlib import Path

from ollama import Client
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class FirewallEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    timestamp: str
    event_type: Literal["firewall_block"]
    source_ip: str
    destination_ip: str
    destination_port: int = Field(ge=1, le=65535)
    action: Literal["block"]


BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"
PASTA.mkdir(parents=True, exist_ok=True)

cliente = Client(host="http://localhost:11434")

resposta = cliente.chat(
    model="qwen3:0.6b",
    messages=[{
        "role": "user",
        "content": (
            "Gere um evento ficticio de firewall que "
            "bloqueou uma conexao TCP na porta 8080. "
            "Use timestamp ISO 8601 e IPs de documentacao: "
            "192.0.2.10 e 198.51.100.20. "
            "Responda somente com o objeto JSON."
        ),
    }],
    format=FirewallEvent.model_json_schema(),
    think=False,
    stream=False,
    options={
        "temperature": 0,
        "seed": 42,
        "num_predict": 300,
    },
)

texto = resposta.message.content or ""

resultado = {
    "experimento": "DL-01C-schema-probe",
    "modelo": "qwen3:0.6b",
    "resposta": texto,
    "tokens_saida": resposta.eval_count,
    "motivo_encerramento": resposta.done_reason,
}

arquivo = PASTA / "json_schema_probe.json"
arquivo.write_text(
    json.dumps(resultado, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("Resposta gerada:")
print(texto)

print("\nValidacao Pydantic:")
try:
    evento = FirewallEvent.model_validate_json(texto)
    print("APROVADO")
    print(evento.model_dump_json(indent=2))
except Exception as erro:
    print("REPROVADO:", erro)

print("\nArquivo salvo em:", arquivo)
