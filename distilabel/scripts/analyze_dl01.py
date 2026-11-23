
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"

entrada = PASTA / "generated_events.json"
saida = PASTA / "analysis_dl01.json"

dados = json.loads(entrada.read_text(encoding="utf-8"))

campos = ["instruction", "generation", "model_name"]
resultados = []

for indice, registro in enumerate(dados, 1):
    faltantes = [
        campo for campo in campos
        if not isinstance(registro.get(campo), str)
        or not registro[campo].strip()
    ]

    texto = registro.get("generation") or ""
    json_estruturado = False

    try:
        conteudo = json.loads(texto)
        json_estruturado = isinstance(conteudo, dict)
    except (ValueError, TypeError):
        pass

    resultados.append({
        "registro": indice,
        "campos_ausentes": faltantes,
        "caracteres": len(texto),
        "resposta_json_objeto": json_estruturado,
        "modelo": registro.get("model_name")
    })

relatorio = {
    "experimento": "DL-01",
    "tipo": "geracao_textual_livre",
    "total_registros": len(dados),
    "registros_completos": sum(
        not r["campos_ausentes"] for r in resultados
    ),
    "respostas_json_objeto": sum(
        r["resposta_json_objeto"] for r in resultados
    ),
    "resultados": resultados,
    "observacao": (
        "Avalia campos externos e formato das respostas. "
        "Nao comprova qualidade semantica ou realismo."
    )
}

saida.write_text(
    json.dumps(relatorio, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(json.dumps(relatorio, ensure_ascii=False, indent=2))
print("\nRelatorio salvo em:", saida)