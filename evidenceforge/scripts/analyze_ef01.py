
import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

DATA_DIR = BASE / "evidenceforge/EvidenceForge/output-ef01/data"
RESULT_DIR = BASE / "results/evidenceforge/EF-01"

RESULT_DIR.mkdir(parents=True, exist_ok=True)

INICIO = datetime(2024, 5, 14, 12, 0, tzinfo=timezone.utc).timestamp() * 1000
FIM = datetime(2024, 5, 14, 18, 0, tzinfo=timezone.utc).timestamp() * 1000

campos = ["timestamp_ms", "id", "hostname", "object", "action"]

objetos = Counter()
acoes = Counter()
pares = Counter()
ids = Counter()
registros_por_sistema = Counter()
campos_ausentes = Counter()

total = 0
invalidos = 0
sem_id = 0
timestamps_invalidos = 0
fora_janela = 0
inversoes = 0
tempos = []

arquivos = sorted(DATA_DIR.rglob("ecar.json"))

if not arquivos:
    raise SystemExit(f"Nenhum arquivo eCAR encontrado em: {DATA_DIR}")

for arquivo in arquivos:
    anterior = None

    with arquivo.open(encoding="utf-8") as f:
        for linha in f:
            if not linha.strip():
                continue

            try:
                evento = json.loads(linha)
                if not isinstance(evento, dict):
                    invalidos += 1
                    continue
            except json.JSONDecodeError:
                invalidos += 1
                continue

            total += 1
            registros_por_sistema[arquivo.parent.name] += 1

            for campo in campos:
                if campo not in evento or evento[campo] is None:
                    campos_ausentes[campo] += 1

            objetos[evento.get("object")] += 1
            acoes[evento.get("action")] += 1
            pares[(evento.get("object"), evento.get("action"))] += 1

            identificador = evento.get("id")
            if identificador:
                ids[identificador] += 1
            else:
                sem_id += 1

            tempo = evento.get("timestamp_ms")

            if isinstance(tempo, (int, float)) and not isinstance(tempo, bool) and tempo >= 0:
                tempos.append(tempo)

                if anterior is not None and tempo < anterior:
                    inversoes += 1

                anterior = tempo

                if tempo < INICIO or tempo > FIM:
                    fora_janela += 1
            else:
                timestamps_invalidos += 1

duplicados = sum(n - 1 for n in ids.values() if n > 1)

resultado = {
    "experimento": "EF-01",
    "arquivos_ecar": len(arquivos),
    "registros_validos": total,
    "registros_invalidos": invalidos,
    "registros_por_sistema": dict(sorted(registros_por_sistema.items())),
    "objetos": dict(objetos.most_common()),
    "acoes": dict(acoes.most_common()),
    "combinacoes_objeto_acao": [
        {"objeto": obj, "acao": acao, "quantidade": qtd}
        for (obj, acao), qtd in pares.most_common()
    ],
    "campos_ausentes": dict(campos_ausentes),
    "ids_distintos": len(ids),
    "registros_sem_id": sem_id,
    "ids_duplicados": duplicados,
    "timestamps_invalidos": timestamps_invalidos,
    "inversoes_temporais": inversoes,
    "registros_fora_janela": fora_janela,
    "primeiro_evento_utc": (
        datetime.fromtimestamp(min(tempos) / 1000, tz=timezone.utc).isoformat()
        if tempos else None
    ),
    "ultimo_evento_utc": (
        datetime.fromtimestamp(max(tempos) / 1000, tz=timezone.utc).isoformat()
        if tempos else None
    )
}

saida = RESULT_DIR / "analysis_ef01.json"

with saida.open("w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print("Análise concluída!")
print("Arquivos eCAR:", len(arquivos))
print("Registros válidos:", total)
print("Registros inválidos:", invalidos)
print("Objetos diferentes:", len(objetos))
print("Ações diferentes:", len(acoes))
print("Combinações objeto/ação:", len(pares))
print("IDs duplicados:", duplicados)
print("Inversões temporais:", inversoes)
print("Registros fora da janela:", fora_janela)
print("Resultados salvos em:", saida)