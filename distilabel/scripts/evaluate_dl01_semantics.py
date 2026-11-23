import json
import ipaddress
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]
ARQUIVO = BASE / (
    "results/distilabel/DL-01/"
    "generated_events_schema_all.json"
)

SAIDA = BASE / (
    "results/distilabel/DL-01/"
    "semantic_evaluation.json"
)

dados = json.loads(ARQUIVO.read_text(encoding="utf-8"))

resultados = []

for registro in dados:
    categoria = registro["categoria"]
    evento = registro.get("validated_event")
    verificacoes = {}

    if not isinstance(evento, dict):
        resultados.append({
            "categoria": categoria,
            "aprovado": False,
            "verificacoes": {
                "evento_presente": False
            }
        })
        continue

    try:
        instante = datetime.fromisoformat(
            evento["timestamp"].replace("Z", "+00:00")
        )
        verificacoes["timestamp_valido"] = (
            instante.tzinfo is not None
        )
    except (KeyError, TypeError, ValueError):
        verificacoes["timestamp_valido"] = False

    if categoria == "login":
        verificacoes["tipo_coerente"] = (
            evento.get("event_type") == "failed_login"
        )
        verificacoes["status_coerente"] = (
            evento.get("status") == "failure"
        )
        verificacoes["usuario_presente"] = bool(
            evento.get("username")
        )

    elif categoria == "firewall":
        verificacoes["tipo_coerente"] = (
            evento.get("event_type") == "firewall_block"
        )
        verificacoes["acao_coerente"] = (
            evento.get("action") == "block"
        )
        porta = evento.get("destination_port")
        verificacoes["porta_valida"] = (
            type(porta) is int and 1 <= porta <= 65535
        )

    elif categoria == "process":
        verificacoes["tipo_coerente"] = (
            evento.get("event_type") == "process_execution"
        )
        verificacoes["processo_presente"] = bool(
            evento.get("process_name")
        )
        pid = evento.get("process_id")
        verificacoes["pid_valido"] = (
            type(pid) is int and pid > 0
        )

    else:
        verificacoes["categoria_reconhecida"] = False

    for campo in ("source_ip", "destination_ip"):
        if campo in evento:
            try:
                ipaddress.ip_address(evento[campo])
                verificacoes[f"{campo}_valido"] = True
            except (ValueError, TypeError):
                verificacoes[f"{campo}_valido"] = False

    aprovado = bool(verificacoes) and all(
        verificacoes.values()
    )

    resultados.append({
        "categoria": categoria,
        "aprovado": aprovado,
        "verificacoes": verificacoes
    })

relatorio = {
    "experimento": "DL-01C",
    "tipo_avaliacao": "coerencia_semantica_basica",
    "total": len(resultados),
    "aprovados": sum(
        r["aprovado"] for r in resultados
    ),
    "resultados": resultados,
    "limitacoes": (
        "Verificacoes deterministicas de coerencia entre campos. "
        "Nao comprovam realismo operacional, fidelidade estatistica "
        "ou qualidade semantica integral."
    )
}

SAIDA.write_text(
    json.dumps(relatorio, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(json.dumps(
    relatorio,
    ensure_ascii=False,
    indent=2
))

print("\nRelatorio salvo em:", SAIDA)