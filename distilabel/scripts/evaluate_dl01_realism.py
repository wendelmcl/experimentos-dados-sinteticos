import json
import ipaddress
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

ENTRADA = BASE / (
    "results/distilabel/DL-01/"
    "generated_events_schema_all.json"
)

SAIDA = BASE / (
    "results/distilabel/DL-01/"
    "realism_evaluation.json"
)

dados = json.loads(ENTRADA.read_text(encoding="utf-8"))

resultados = []

for registro in dados:
    categoria = registro["categoria"]
    evento = registro.get("validated_event")

    observacoes = []

    if not isinstance(evento, dict):
        resultados.append({
            "categoria": categoria,
            "observacoes": ["Evento ausente ou inválido"]
        })
        continue

    for campo in ("source_ip", "destination_ip"):
        if campo in evento:
            try:
                ip = ipaddress.ip_address(evento[campo])

                if ip.is_private:
                    observacoes.append(
                        f"{campo}: endereço não global "
                        "ou reservado"
                    )
                else:
                    observacoes.append(
                        f"{campo}: endereço global"
                    )

            except ValueError:
                observacoes.append(
                    f"{campo}: endereço inválido"
                )

    if categoria == "login":
        observacoes.append(
            "Evento de autenticação malsucedida "
            "sem contexto adicional de tentativas"
        )

    elif categoria == "firewall":
        observacoes.append(
            "Evento de bloqueio com origem, destino, "
            "porta e ação identificados"
        )

    elif categoria == "process":
        observacoes.append(
            "Execução de processo sem informações "
            "sobre executável, caminho ou processo pai"
        )

    resultados.append({
        "categoria": categoria,
        "observacoes": observacoes
    })

relatorio = {
    "experimento": "DL-01C",
    "avaliacao": "plausibilidade_operacional_exploratoria",
    "total": len(resultados),
    "resultados": resultados,
    "limitacao": (
        "Analise descritiva automatizada. "
        "Nao estabelece uma pontuacao validada "
        "de realismo operacional."
    )
}

SAIDA.write_text(
    json.dumps(
        relatorio,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(json.dumps(
    relatorio,
    indent=2,
    ensure_ascii=False
))

print("\nRelatorio salvo em:", SAIDA)