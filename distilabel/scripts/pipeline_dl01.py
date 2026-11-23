
import json
from pathlib import Path

from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration
from distilabel.models.llms import OllamaLLM

# Pasta principal dos experimentos
BASE = Path(__file__).resolve().parents[2]

# Local onde os resultados serão armazenados
RESULT_DIR = BASE / "results/distilabel/DL-01"
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# Três instruções de geração
instrucoes = [
    {
        "instruction": (
            "Crie um exemplo fictício de registro de segurança "
            "representando uma tentativa de login malsucedida. "
            "Inclua timestamp, usuário, endereço IP e resultado. "
            "Não afirme que o evento é um ataque sem evidências."
        )
    },
    {
        "instruction": (
            "Crie um exemplo fictício de evento de segurança "
            "representando uma conexão de rede bloqueada por "
            "um firewall. Inclua timestamp, IP de origem, "
            "IP de destino, porta e ação."
        )
    },
    {
        "instruction": (
            "Crie um exemplo fictício de evento de segurança "
            "representando a execução de um processo em um "
            "endpoint. Inclua timestamp, hostname, processo, "
            "usuário e identificador do processo."
        )
    }
]

# Definição do Pipeline
with Pipeline(name="DL-01-Security-Generation") as pipeline:

    carregamento = LoadDataFromDicts(
        name="load_security_instructions",
        data=instrucoes,
        batch_size=1
    )

    geracao = TextGeneration(
        name="generate_security_events",
        llm=OllamaLLM(
            model="qwen3:0.6b",
            host="http://localhost:11434",
            timeout=120
        ),
        input_batch_size=1
    )

    carregamento >> geracao

if __name__ == "__main__":
    print("Iniciando Pipeline DL-01...")

    distiset = pipeline.run(use_cache=False)

    # Extrair os registros produzidos
    registros = distiset["default"]["train"].to_list()

    # Salvar resultados em JSON
    arquivo_saida = RESULT_DIR / "generated_events.json"

    with arquivo_saida.open("w", encoding="utf-8") as f:
        json.dump(
            registros,
            f,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    print("Pipeline concluído!")
    print("Registros gerados:", len(registros))
    print("Arquivo salvo em:", arquivo_saida)
