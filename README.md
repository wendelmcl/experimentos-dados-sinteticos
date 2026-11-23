# Experimentos de Geração de Dados Sintéticos para Cibersegurança

## Sobre o projeto

Este repositório reúne experimentos de reprodução e avaliação de técnicas de geração de dados sintéticos para cibersegurança.

O trabalho tem como objetivo investigar abordagens de geração de dados reais, sintéticos e híbridos, considerando sua qualidade, diversidade, consistência, reprodutibilidade e potencial de utilização em modelos de linguagem de pequeno porte (SLMs).

## Projetos selecionados

| Projeto | Técnica | Situação |
|---|---|---|
| EvidenceForge | Simulação baseada em cenários e regras | Experimento EF-01 reproduzido |
| Distilabel | Geração e avaliação com modelos de linguagem | Pendente |
| CTGAN Network | Geração adversarial de dados tabulares | Pendente |

## Experimento EF-01 — EvidenceForge

O cenário oficial `branch-office-example` foi reproduzido em um MacBook com processador Apple M1 e 8 GB de memória.

### Principais resultados

- 42.736 registros sintéticos.
- 18 fontes de evidências.
- 40 arquivos gerados.
- Pontuação de qualidade: 97/100.
- Avaliação interna: PASS.
- Reprodutibilidade dos arquivos de evidências e do Ground Truth confirmada nas execuções comparadas.

### Análise independente

Foram analisados 12.145 registros eCAR, identificando:

- 7 categorias de objetos.
- 11 tipos de ações.
- 12 combinações objeto/ação.
- Nenhum registro JSON inválido.
- Nenhum identificador duplicado.
- Nenhuma inversão temporal nos arquivos analisados.
- Nenhum evento fora da janela de simulação.

### Documentação

- Relatório: `reports/EF-01_EvidenceForge.md`
- Script: `evidenceforge/scripts/analyze_ef01.py`
- Resultados: `results/evidenceforge/EF-01/`

## Reprodutibilidade

Os experimentos utilizam projetos de código aberto. As versões, os commits, os procedimentos de execução e as configurações utilizadas são documentados nos respectivos relatórios técnicos.

Os códigos originais dos projetos não são redistribuídos neste repositório.

## Limitações

Os resultados correspondem aos cenários e ambientes efetivamente testados. A qualidade estrutural e a reprodutibilidade dos dados sintéticos não comprovam, isoladamente, sua equivalência com dados reais ou melhoria no desempenho de SLMs.

## Referências

- EvidenceForge: https://github.com/Cisco-Talos/EvidenceForge
- Distilabel: https://github.com/argilla-io/distilabel
- CTGAN Network: https://github.com/czentamayo/ctgan_network_dataset_generation