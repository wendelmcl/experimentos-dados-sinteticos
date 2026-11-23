
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"

def carregar(nome):
    arquivo = PASTA / nome
    return json.loads(arquivo.read_text(encoding="utf-8"))

livres = carregar("generated_events_free.json")
estruturados = carregar("generated_events_structured.json")
validacao = carregar("validation_structured.json")

def contar_json_objetos(registros):
    total = 0

    for registro in registros:
        texto = registro.get("generation")

        try:
            evento = json.loads(texto)
            if isinstance(evento, dict):
                total += 1
        except (TypeError, ValueError):
            pass

    return total

def contar_campos_externos(registros):
    obrigatorios = [
        "instruction",
        "generation",
        "model_name"
    ]

    return sum(
        all(
            isinstance(registro.get(campo), str)
            and registro[campo].strip()
            for campo in obrigatorios
        )
        for registro in registros
    )

relatorio = {
    "experimento": "DL-01",
    "modelo": "qwen3:0.6b",
    "comparacao": {
        "DL-01A": {
            "abordagem": "texto_livre",
            "registros": len(livres),
            "campos_externos_completos":
                contar_campos_externos(livres),
            "respostas_json_objeto":
                contar_json_objetos(livres),
            "thinking": "configuracao_padrao"
        },
        "DL-01B": {
            "abordagem": "json_solicitado",
            "registros": len(estruturados),
            "campos_externos_completos":
                contar_campos_externos(estruturados),
            "respostas_json_objeto":
                contar_json_objetos(estruturados),
            "aprovados_validacao":
                validacao["validos"],
            "reprovados_validacao":
                validacao["invalidos"],
            "thinking": "desativado"
        }
    },
    "limitacoes": [
        "Amostra de apenas tres registros por abordagem.",
        "Configuracoes de geracao diferentes.",
        "A validacao de esquema foi aplicada apenas ao DL-01B.",
        "Qualidade semantica nao foi avaliada integralmente.",
        "Nao houve avaliacao de desempenho de SLMs."
    ]
}

saida = PASTA / "comparison_dl01.json"

saida.write_text(
    json.dumps(relatorio, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(json.dumps(relatorio, indent=2, ensure_ascii=False))
print("\nRelatorio salvo em:", saida)
