
# Relatório Técnico EF-01 — EvidenceForge

## 1. Identificação do Experimento

- Projeto: EvidenceForge
- Versão: 2.1.2
- Cenário: branch-office-example
- Sistema operacional: macOS
- Processador: Apple M1
- Memória: 8 GB
- Python: 3.12.16
- Identificador: EF-01

## 2. Objetivo

Reproduzir o cenário oficial branch-office-example do
EvidenceForge e avaliar a qualidade, diversidade,
consistência e reprodutibilidade dos dados sintéticos
gerados.

## 3. Metodologia

O experimento foi realizado por meio das seguintes etapas:

1. Configuração do ambiente Python com uv.
2. Validação do cenário YAML.
3. Execução da geração de logs sintéticos.
4. Avaliação de qualidade pelo EvidenceForge.
5. Reprodução controlada da geração.
6. Comparação dos arquivos e do Ground Truth.
7. Análise independente dos registros eCAR.
8. Automatização da análise utilizando Python.

## 4. Resultados da Geração

- Total de registros: 42.736
- Fontes de evidência: 18
- Arquivos de evidências: 40
- Qualidade geral: 97/100
- Resultado da avaliação: PASS

## 5. Avaliação de Qualidade

| Dimensão | Pontuação |
|---|---:|
| Parseability | 100/100 |
| Plausibility | 93/100 |
| Causality | 100/100 |
| Timing | 95/100 |

## 6. Avaliação de Diversidade

Foram analisados 12.145 registros eCAR.

- Sistemas: 9
- Categorias de objetos: 7
- Tipos de ações: 11
- Combinações objeto/ação: 12

Os registros apresentam diferentes categorias de
atividades, com predominância de eventos de conexão.

## 7. Avaliação de Consistência

Na análise independente dos registros eCAR:

- Registros JSON inválidos: 0
- Campos obrigatórios ausentes: 0
- Identificadores duplicados: 0
- Timestamps inválidos: 0
- Inversões temporais: 0
- Eventos fora da janela: 0

## 8. Reprodutibilidade

A segunda execução produziu:

- 42.736 registros;
- 18 fontes;
- 40 arquivos de evidências;
- pontuação geral de 97/100.

A comparação com diff não identificou diferenças
entre os 40 arquivos de evidências.

Os arquivos GROUND_TRUTH.json também apresentaram
hashes SHA-256 idênticos.

## 9. Limitações

A avaliação independente concentrou-se nos registros
eCAR, não abrangendo todos os formatos gerados.

A conformidade estrutural e temporal não comprova,
isoladamente, realismo em relação a ambientes reais
ou utilidade para treinamento de SLMs.

A análise foi realizada com um único cenário oficial
e em um único ambiente computacional.

## 10. Conclusão

O experimento EF-01 demonstrou a possibilidade de
reproduzir o cenário branch-office-example no MacBook
M1, gerando evidências sintéticas e obtendo aprovação
nos critérios internos de qualidade do EvidenceForge.

Os resultados também demonstraram reprodutibilidade
dos arquivos de evidências e do Ground Truth nas
execuções comparadas.

As verificações independentes identificaram variedade
de objetos e ações, além de conformidade estrutural
e temporal básica dos registros eCAR analisados.

## 11. Referências

EvidenceForge — Cisco Talos.
https://github.com/Cisco-Talos/EvidenceForge



## 12. Procedimento de Reprodução

O experimento foi executado no macOS com Python 3.12.16,
uv 0.13.9 e EvidenceForge 2.1.2.

### 12.1. Preparação do ambiente

Clonar o repositório oficial:

```bash
git clone https://github.com/Cisco-Talos/EvidenceForge.git
cd EvidenceForge
```

Instalar e sincronizar as dependências:

```bash
uv python install 3.12
uv sync --python 3.12
```

### 12.2. Validação do cenário

```bash
PYTHONPATH="$PWD/src" uv run eforge validate scenarios/branch-office-example/scenario.yaml
```

### 12.3. Geração dos dados

```bash
PYTHONPATH="$PWD/src" uv run eforge generate scenarios/branch-office-example/scenario.yaml -o ./output-ef01
```

A pasta de saída deve estar ausente antes da execução,
para evitar sobrescrever resultados anteriores.

### 12.4. Avaliação da qualidade

```bash
PYTHONPATH="$PWD/src" uv run eforge eval ./output-ef01
```

### 12.5. Análise independente

O script analyze_ef01.py foi desenvolvido para
avaliar os registros eCAR.

Sua execução, a partir da raiz do repositório oficial
clonado na estrutura de diretórios do estudo, ocorre com:

```bash
uv run python ../../evidenceforge/scripts/analyze_ef01.py
```

O script produz o arquivo analysis_ef01.json.

### 12.6. Identificação do código utilizado

- Versão: EvidenceForge 2.1.2
- Commit: 79fcfcdf3726168dacfdede5a27aab2aa7a2f3d69

Durante a configuração, houve um problema na resolução
do pacote Python instalado em modo editável.

A execução foi viabilizada pela definição explícita
de PYTHONPATH para o diretório src.

A reprodução deve utilizar o mesmo commit e registrar
eventuais diferenças de dependências ou ambiente.


## 13. Artefatos do Experimento

Os resultados foram organizados no diretório:

results/evidenceforge/EF-01/

Arquivos:

- experiment-info.txt
- analysis_ef01.json
- GENERATION_MANIFEST.json
- OBSERVATION_MANIFEST.json
- COLLECTION_PROFILE.json
- GROUND_TRUTH.json
- RESOLVED_SCENARIO.yaml

O script de análise está localizado em:

evidenceforge/scripts/analyze_ef01.py

Os 40 arquivos de evidências permanecem no diretório
de saída da ferramenta.

O arquivo GROUND_TRUTH.json apresentou o seguinte
hash SHA-256 nas duas execuções:

c23c780c6daa9eda632759b876a8e1b7b9f4d28316deb892bbcb256ace099f6a

Os resultados apresentados correspondem à execução
do cenário branch-office-example.