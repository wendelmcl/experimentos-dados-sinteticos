
import json
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration
from distilabel.models.llms import OllamaLLM


# 1. Esquemas dos eventos

class LoginEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    timestamp: str
    event_type: Literal["failed_login"]
    username: str
    source_ip: str
    status: Literal["failure"]


class FirewallEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    timestamp: str
    event_type: Literal["firewall_block"]
    source_ip: str
    destination_ip: str
    destination_port: int = Field(ge=1, le=65535)
    action: Literal["block"]


class ProcessEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    timestamp: str
    event_type: Literal["process_execution"]
    hostname: str
    process_name: str
    username: str
    process_id: int = Field(gt=0)


# 2. Adaptacao experimental do OllamaLLM

class OllamaSchemaLLM(OllamaLLM):
    schema_json: str

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
            format=json.loads(self.schema_json),
            options={
                "temperature": 0,
                "seed": 42,
                "num_predict": 300,
            },
            keep_alive=keep_alive,
            think=False,
        )


# 3. Configuracao dos experimentos

BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"
PASTA.mkdir(parents=True, exist_ok=True)

CASOS = [
    (
        "login",
        LoginEvent,
        "Gere um evento ficticio de login malsucedido. "
        "Use timestamp ISO 8601, usuario ficticio e IP "
        "192.0.2.10. Nao classifique como ataque. "
        "Responda somente JSON."
    ),
    (
        "firewall",
        FirewallEvent,
        "Gere um evento ficticio de firewall bloqueando "
        "uma conexao TCP na porta 8080. "
        "Use IPs 192.0.2.10 e 198.51.100.20. "
        "Responda somente JSON."
    ),
    (
        "process",
        ProcessEvent,
        "Gere um evento ficticio de execucao de processo "
        "em um endpoint. Use hostname ficticio, "
        "usuario, processo e PID inteiro positivo. "
        "Nao classifique como malware. "
        "Responda somente JSON."
    ),
]


# 4. Executar um Pipeline para cada esquema

if __name__ == "__main__":
    resultados = []

    for nome, esquema, instrucao in CASOS:

        print(f"\nExecutando categoria: {nome}")

        # Subclasse isolada para o esquema do caso

        with Pipeline(name=f"DL-01C-{nome}") as pipeline:

            carregar = LoadDataFromDicts(
                name=f"load_{nome}",
                data=[{"instruction": instrucao}],
                batch_size=1,
            )

            gerar = TextGeneration(
                name=f"generate_{nome}",
                llm=OllamaSchemaLLM(
                model="qwen3:0.6b",
                host="http://localhost:11434",
                timeout=120,
                schema_json=json.dumps(esquema.model_json_schema()),
    ),
                input_batch_size=1,
            )

            carregar >> gerar

        distiset = pipeline.run(use_cache=False)
        registros = distiset["default"]["train"].to_list()

        if len(registros) != 1:
            raise RuntimeError(
                f"{nome}: esperado 1 registro, "
                f"recebidos {len(registros)}"
            )

        registro = registros[0]
        texto = registro.get("generation")

        try:
            evento = esquema.model_validate_json(texto)
            valido = True
            erros = []
            print(f"{nome}: APROVADO")
        except Exception as erro:
            evento = None
            valido = False
            erros = [str(erro)]
            print(f"{nome}: REPROVADO")

        resultados.append({
            "categoria": nome,
            "instruction": instrucao,
            "generation": texto,
            "model_name": registro.get("model_name"),
            "schema_valid": valido,
            "validation_errors": erros,
            "validated_event": (
                evento.model_dump() if evento else None
            ),
        })


    # 5. Salvar resultados, inclusive falhas

    saida = PASTA / "generated_events_schema_all.json"

    saida.write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nExperimento DL-01C finalizado.")
    print("Total de registros:", len(resultados))
    print("Aprovados:", sum(r["schema_valid"] for r in resultados))
    print("Arquivo salvo:", saida)
