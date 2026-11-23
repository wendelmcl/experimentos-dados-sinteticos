
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration
from distilabel.models.llms import OllamaLLM


# Esquema do evento de firewall
class FirewallEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    timestamp: str
    event_type: Literal["firewall_block"]
    source_ip: str
    destination_ip: str
    destination_port: int = Field(ge=1, le=65535)
    action: Literal["block"]


# Integracao experimental com JSON Schema
class OllamaSchemaLLM(OllamaLLM):

    async def _generate_chat_completion(
        self,
        input,
        format="",
        options=None,
        keep_alive=None,
    ):
        return await self._aclient.chat(
            model=self.model,
            messages=input,
            stream=False,
            format=FirewallEvent.model_json_schema(),
            options={
                "temperature": 0,
                "seed": 42,
                "num_predict": 300,
            },
            keep_alive=keep_alive,
            think=False,
        )


BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"
PASTA.mkdir(parents=True, exist_ok=True)


# Entrada controlada
instrucoes = [
    {
        "instruction": (
            "Gere um evento ficticio de firewall que "
            "bloqueou uma conexao TCP na porta 8080. "
            "Use timestamp ISO 8601 e os IPs "
            "192.0.2.10 e 198.51.100.20. "
            "Retorne somente o objeto JSON."
        )
    }
]


# Pipeline Distilabel
with Pipeline(name="DL-01C-Schema-Pipeline") as pipeline:

    carregar = LoadDataFromDicts(
        name="load_firewall_instruction",
        data=instrucoes,
        batch_size=1,
    )

    gerar = TextGeneration(
        name="generate_firewall_schema",
        llm=OllamaSchemaLLM(
            model="qwen3:0.6b",
            host="http://localhost:11434",
            timeout=120,
        ),
        input_batch_size=1,
    )

    carregar >> gerar


if __name__ == "__main__":

    print("Iniciando Pipeline DL-01C...")

    distiset = pipeline.run(use_cache=False)
    registros = distiset["default"]["train"].to_list()

    arquivo = PASTA / "generated_events_schema.json"

    arquivo.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Registros gerados:", len(registros))
    print("Arquivo salvo:", arquivo)
