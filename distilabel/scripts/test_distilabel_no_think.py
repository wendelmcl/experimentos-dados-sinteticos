
import json
from pathlib import Path

from distilabel.models.llms import OllamaLLM


class OllamaNoThinkLLM(OllamaLLM):
    """Adaptacao experimental para desativar Thinking."""

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
            format=format,
            options=options,
            keep_alive=keep_alive,
            think=False,
        )


BASE = Path(__file__).resolve().parents[2]
SAIDA = BASE / "results/distilabel/DL-01/json_no_think_probe.json"

llm = OllamaNoThinkLLM(
    model="qwen3:0.6b",
    host="http://localhost:11434",
    timeout=120,
)

instrucao = (
    "Gere um evento ficticio de login malsucedido. "
    "Retorne apenas um objeto JSON com exatamente os campos: "
    "timestamp, event_type, username, source_ip e status. "
    "Use event_type='failed_login' e status='failure'. "
    "Use um IP reservado para documentacao, como 192.0.2.10. "
    "Nao classifique o evento como ataque."
)

llm.load()

try:
    resultado = llm.generate_outputs(
        inputs=[[{"role": "user", "content": instrucao}]],
        num_generations=1,
        format="json",
        options={
            "temperature": 0,
            "seed": 42,
            "num_predict": 200,
        },
    )
finally:
    llm.unload()

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(
    json.dumps(resultado, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(json.dumps(resultado, ensure_ascii=False, indent=2))
print("Arquivo salvo em:", SAIDA)