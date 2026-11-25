# Experimentos de Geração de Dados Sintéticos para Cibersegurança

## Sobre o projeto

Este repositório reúne experimentos de **reprodução e avaliação de técnicas de geração de dados sintéticos para cibersegurança**, com ênfase em qualidade, diversidade, consistência e reprodutibilidade.

Os experimentos integram um estudo exploratório sobre a produção de evidências e eventos sintéticos de segurança computacional e suas possibilidades de utilização futura em pesquisas envolvendo **modelos de linguagem de pequeno porte (SLMs)**. **Não foi realizada, nesta etapa, uma avaliação do impacto desses dados no treinamento ou desempenho de SLMs.**

## Experimentos realizados

| Identificador | Projeto | Abordagem | Situação |
|---|---|---|---|
| **EF-01** | [EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge) | Simulação baseada em cenários e regras, com geração de evidências e *ground truth* | **Executado, avaliado e documentado** |
| **DL-01** | [Distilabel](https://github.com/argilla-io/distilabel) | Geração de eventos sintéticos com LLM, instruções e esquemas JSON | **Executado, avaliado e documentado** |

O escopo experimental atualmente documentado neste repositório compreende **EvidenceForge e Distilabel**. As duas ferramentas adotam estratégias diferentes e foram avaliadas com procedimentos e volumes de dados distintos; portanto, os resultados **não constituem uma comparação direta de desempenho** entre elas.

## EF-01 — EvidenceForge

O experimento EF-01 reproduziu o cenário oficial `branch-office-example` com o **EvidenceForge 2.1.2**, em um MacBook com **Apple M1 e 8 GB de RAM**, utilizando **Python 3.12.16**.

### Resultados principais

| Indicador | Resultado |
|---|---:|
| Registros sintéticos gerados | **42.736** |
| Fontes de evidência | **18** |
| Arquivos de evidência | **40** |
| Qualidade geral na avaliação interna | **97/100** |
| Resultado da avaliação interna | **PASS** |
| Registros eCAR examinados na análise independente | **12.145** |
| Registros JSON inválidos na amostra eCAR analisada | **0** |

A análise dos registros eCAR identificou **9 sistemas**, **7 categorias de objetos**, **11 tipos de ações** e **12 combinações objeto/ação**. Nas verificações implementadas, não foram observados identificadores duplicados, timestamps inválidos, inversões temporais ou eventos fora da janela de simulação.

A reprodução controlada descrita no relatório técnico preservou a contagem de registros e a pontuação interna. A comparação dos **40 arquivos de evidência** não identificou diferenças e os arquivos `GROUND_TRUTH.json` comparados apresentaram assinaturas SHA-256 idênticas.

**Limite da evidência:** a análise independente concentrou-se no formato eCAR e o estudo abrangeu um cenário oficial em um ambiente computacional. A pontuação interna não comprova, isoladamente, fidelidade a dados de produção.

**Artefatos:**

- [Relatório técnico EF-01](reports/EF-01_EvidenceForge.md)
- [Tutorial de reprodução EF-01](reports/Tutorial_EF-01_EvidenceForge.md)
- [Script de análise EF-01](evidenceforge/scripts/analyze_ef01.py)
- [Resultados preservados do EF-01](results/evidenceforge/EF-01/)

## DL-01 — Distilabel

O experimento DL-01 integrou **Distilabel 1.5.3**, **Ollama 0.40.17** e o modelo **Qwen3 0.6B (`qwen3:0.6b`)**, em ambiente **macOS com Python 3.12.16**, para gerar eventos fictícios de segurança computacional.

Foram investigadas três configurações de geração:

| Configuração | Estratégia | Registros gerados | Objetos JSON válidos | Aprovação nas regras de esquema |
|---|---|---:|---:|---|
| **DL-01A** | Geração textual livre | 3 | 0 | Não avaliada |
| **DL-01B** | JSON solicitado por instrução | 3 | 3 | **2 de 3** |
| **DL-01C** | Geração condicionada por JSON Schema | 3 | 3 | **3 de 3** |

O DL-01C contemplou três categorias de eventos: **falha de autenticação** (`failed_login`), **bloqueio de firewall** (`firewall_block`) e **execução de processo** (`process_execution`). Os três registros passaram pelas verificações estruturais e de coerência básica aplicadas. A inspeção exploratória também identificou limitações de contexto e plausibilidade operacional.

Na avaliação de repetibilidade do DL-01C, **três execuções adicionais** produziram três registros aprovados cada uma, com **conteúdo dos eventos idêntico** nas comparações efetuadas. As configurações finais incluíram **temperatura 0**, **semente 42**, **limite de 300 tokens** e execução com `use_cache=False`.

**Limite da evidência:** a amostra inicial tem apenas **três registros por configuração**. A aprovação nos esquemas e a repetibilidade observada não demonstram realismo operacional abrangente, diversidade estatística ou superioridade geral de uma estratégia de geração.

**Artefatos:**

- [Relatório técnico DL-01](reports/DL-01_Distilabel.md)
- [Tutorial de reprodução DL-01](reports/Tutorial_DL-01_Distilabel.md)
- [Scripts do DL-01](distilabel/scripts/)
- [Resultados preservados do DL-01](results/distilabel/DL-01/)

## Organização do repositório

```text
experimentos-dados-sinteticos/
├── README.md
├── .gitignore
├── evidenceforge/
│   └── scripts/
│       └── analyze_ef01.py
├── distilabel/
│   └── scripts/                 # Pipelines, testes e avaliações do DL-01
├── reports/
│   ├── EF-01_EvidenceForge.md
│   ├── Tutorial_EF-01_EvidenceForge.md
│   ├── DL-01_Distilabel.md
│   └── Tutorial_DL-01_Distilabel.md
└── results/
    ├── evidenceforge/EF-01/   # Metadados, manifestos, ground truth e análises
    └── distilabel/DL-01/      # Saídas, validações e testes de repetibilidade
```

Os diretórios acima representam os **artefatos próprios do estudo**. Os repositórios completos das ferramentas de terceiros e os ambientes virtuais locais não são redistribuídos aqui.

## Como reproduzir os experimentos

Os **tutoriais específicos** descrevem os pré-requisitos, a preparação do ambiente, os comandos utilizados, os procedimentos de validação e as limitações de cada estudo:

1. **EvidenceForge:** [Tutorial EF-01](reports/Tutorial_EF-01_EvidenceForge.md) — cenário `branch-office-example`, geração de evidências, avaliação interna e análise eCAR.
2. **Distilabel:** [Tutorial DL-01](reports/Tutorial_DL-01_Distilabel.md) — integração com Ollama/Qwen3, três abordagens de geração, JSON Schema, validações e repetibilidade.

Para avaliar os resultados sem executar novamente as ferramentas, consulte os [relatórios técnicos](reports/) e os arquivos preservados em `results/`.

## Limitações e próximos passos

- Os experimentos apresentam **escopos, amostras e critérios de avaliação diferentes**; não é adequado comparar seus números como se fossem métricas equivalentes.
- A validade estrutural dos registros e os testes de repetibilidade não demonstram, isoladamente, **fidelidade estatística ou operacional** em relação a logs reais.
- A contribuição dos dados gerados para o treinamento ou a avaliação de **SLMs** ainda não foi medida.
- Como continuidade de pesquisa, podem ser planejadas avaliações com amostras maiores, cenários adicionais e critérios de qualidade comparáveis entre abordagens.

## Referências dos projetos

- **EvidenceForge (Cisco Talos):** https://github.com/Cisco-Talos/EvidenceForge
- **Distilabel (Argilla):** https://github.com/argilla-io/distilabel
