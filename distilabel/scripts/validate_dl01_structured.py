
import json
import ipaddress
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PASTA = BASE / "results/distilabel/DL-01"

ENTRADA = PASTA / "generated_events_structured.json"
SAIDA = PASTA / "validation_structured.json"

ESQUEMAS = {
    "failed_login": {
        "timestamp": str,
        "event_type": str,
        "username": str,
        "source_ip": str,
        "status": str,
    },
    "firewall_block": {
        "timestamp": str,
        "event_type": str,
        "source_ip": str,
        "destination_ip": str,
        "destination_port": int,
        "action": str,
    },
    "process_execution": {
        "timestamp": str,
        "event_type": str,
        "hostname": str,
        "process_name": str,
        "username": str,
        "process_id": int,
    },
}

REDES_DOCUMENTACAO = [
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
]

dados = json.loads(ENTRADA.read_text(encoding="utf-8"))
resultados = []

for numero, registro in enumerate(dados, 1):
    erros = []
    texto = registro.get("generation")

    try:
        evento = json.loads(texto)
    except (TypeError, ValueError):
        evento = None
        erros.append("Resposta nao e JSON valido")

    if isinstance(evento, dict):
        tipo = evento.get("event_type")
        esquema = ESQUEMAS.get(tipo)

        if esquema is None:
            erros.append("Tipo de evento desconhecido")
        else:
            faltantes = set(esquema) - set(evento)
            extras = set(evento) - set(esquema)

            for campo in sorted(faltantes):
                erros.append(f"Campo ausente: {campo}")

            for campo in sorted(extras):
                erros.append(f"Campo adicional: {campo}")

            for campo, esperado in esquema.items():
                if campo in evento:
                    valor = evento[campo]
                    if type(valor) is not esperado:
                        erros.append(
                            f"Tipo incorreto: {campo}; "
                            f"esperado {esperado.__name__}"
                        )
                    elif esperado is str and not valor.strip():
                        erros.append(f"Campo vazio: {campo}")

        # Verificar formato da data
        try:
            data = evento["timestamp"]
            datetime.fromisoformat(data.replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError, AttributeError):
            erros.append("Timestamp invalido")

        # Verificar enderecos IP
        for campo in ("source_ip", "destination_ip"):
            if campo in evento:
                try:
                    ip = ipaddress.ip_address(evento[campo])
                    if ip.version != 4:
                        erros.append(f"IPv4 esperado: {campo}")
                    elif not any(
                        ip in rede for rede in REDES_DOCUMENTACAO
                    ):
                        erros.append(
                            f"IP fora dos blocos de documentacao: {campo}"
                        )
                except (TypeError, ValueError):
                    erros.append(f"IP invalido: {campo}")

        # Verificar valores especificos
        if tipo == "failed_login":
            if evento.get("status") != "failure":
                erros.append("Status diferente de failure")

        if tipo == "firewall_block":
            if evento.get("action") != "block":
                erros.append("Acao diferente de block")

            porta = evento.get("destination_port")
            if type(porta) is int and not 1 <= porta <= 65535:
                erros.append("Porta fora do intervalo valido")

        if tipo == "process_execution":
            pid = evento.get("process_id")
            if type(pid) is int and pid <= 0:
                erros.append("PID deve ser positivo")

    elif not erros:
        erros.append("Resposta JSON nao e objeto")

    resultados.append({
        "registro": numero,
        "event_type": (
            evento.get("event_type")
            if isinstance(evento, dict) else None
        ),
        "valido": len(erros) == 0,
        "erros": erros,
    })

relatorio = {
    "experimento": "DL-01B",
    "total": len(resultados),
    "validos": sum(r["valido"] for r in resultados),
    "invalidos": sum(not r["valido"] for r in resultados),
    "resultados": resultados,
    "limitacao": (
        "Validacao de esquema e algumas regras de dominio. "
        "Nao comprova realismo ou qualidade semantica integral."
    ),
}

SAIDA.write_text(
    json.dumps(relatorio, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(json.dumps(relatorio, indent=2, ensure_ascii=False))
print("\nRelatorio salvo em:", SAIDA)
