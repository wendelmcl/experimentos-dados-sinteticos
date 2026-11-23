
import json
from pathlib import Path

from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration
from distilabel.models.llms import OllamaLLM


class OllamaNoThinkLLM(OllamaLLM):
    """Adaptacao local: JSON e Thinking desativado."""

    async def _generate_chat_completion(
        self, input, format="", options=None, keep_alive=None
    ):
        return await self._aclient.chat(
            model=self.model,
            messages=input,
            stream=False,
            format="json",
            options={
                "temperature": 0,
                "seed": 42,
                "num_predict": 250,
            },
            keep_alive=keep_alive,
            think=False,
        )


BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"
PASTA.mkdir(parents=True, exist_ok=True)

instrucoes = [
    {
        "instruction": (
            "Gere um evento FICTICIO de login malsucedido. "
            "Retorne somente JSON com exatamente: "
            "timestamp, event_type, username, source_ip, status. "
            "event_type deve ser failed_login e status failure. "
            "Use um IPv4 de documentacao, como 192.0.2.10. "
            "Nao classifique como ataque."
        )
    },
    {
        "instruction": (
            "Gere um evento FICTICIO de conexao bloqueada por firewall. "
            "Retorne somente JSON com exatamente: "
            "timestamp, event_type, source_ip, destination_ip, "
            "destination_port, action. "
            "event_type deve ser firewall_block e action block. "
            "Use IPs de documentacao, como 192.0.2.10 e 198.51.100.20. "
            "Nao invente causas ou consequencias."
        )
    },
    {
        "instruction": (
            "Gere um evento FICTICIO de execucao de processo. "
            "Retorne somente JSON com exatamente: "
            "timestamp, event_type, hostname, process_name, "
            "username, process_id. "
            "event_type deve ser process_execution. "
            "process_id deve ser um numero inteiro. "
            "Nao afirme que o processo e malicioso."
        )
    }
]

with Pipeline(name="DL-01B-Structured-Generation") as pipeline:
    carregar = LoadDataFromDicts(
        name="load_structured_instructions",
        data=instrucoes,
        batch_size=1,
    )

    gerar = TextGeneration(
        name="generate_structured_events",
        llm=OllamaNoThinkLLM(
            model="qwen3:0.6b",
            host="http://localhost:11434",
            timeout=120,
        ),
        input_batch_size=1,
    )

    carregar >> gerar


if __name__ == "__main__":
    print("Iniciando DL-01B...")

    distiset = pipeline.run(use_cache=False)
    registros = distiset["default"]["train"].to_list()

    arquivo = PASTA / "generated_events_structured.json"

    arquivo.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Registros retornados:", len(registros))
    print("Arquivo salvo:", arquivo)

    for numero, registro in enumerate(registros, 1):
        texto = registro.get("generation")
        try:
            evento = json.loads(texto)
            valido = isinstance(evento, dict)
        except (TypeError, ValueError):
            valido = False

        print(f"Registro {numero}: JSON objeto valido = {valido}")
