# DL-01 — Experimento de Geração de Dados Sintéticos com Distilabel

## 1. Identificação do Experimento

**Identificador:** DL-01
**Ferramenta principal:** Distilabel 1.5.3
**Modelo de linguagem:** Qwen3 0.6B (`qwen3:0.6b`)
**Infraestrutura de inferência:** Ollama 0.40.17
**Linguagem de programação:** Python 3.12.16
**Sistema operacional:** macOS
**Data de execução:** 23 de novembro de 2026
**Área de aplicação:** Cibersegurança e geração de dados sintéticos
**Natureza do estudo:** Experimento exploratório de viabilidade técnica

O experimento integra o projeto *Experimentos de Geração de Dados Sintéticos para Cibersegurança*, destinado à investigação de abordagens de geração de dados sintéticos e à avaliação de características relacionadas à qualidade, consistência, diversidade e repetibilidade dos registros produzidos.

## 2. Objetivo

Avaliar exploratoriamente a utilização do Distilabel, integrado ao Ollama e ao modelo de linguagem Qwen3 0.6B, para a geração de registros sintéticos de eventos de segurança computacional.

O experimento investiga três abordagens de geração: produção textual livre, produção de respostas com formato JSON solicitado por instruções e produção condicionada por esquemas JSON explícitos.

A avaliação considera a conformidade estrutural dos registros, a validade dos campos, a coerência básica entre atributos, a ocorrência de duplicatas, a repetibilidade das execuções e aspectos de plausibilidade operacional.

Adicionalmente, busca identificar limitações técnicas e metodológicas relevantes para futuras investigações sobre a utilização de dados sintéticos em tarefas de cibersegurança.

## 3. Metodologia

O estudo foi conduzido em ambiente macOS, utilizando Python 3.12.16, Distilabel 1.5.3 e Ollama 0.40.17.

O modelo Qwen3 0.6B foi empregado como gerador de conteúdo, por meio da integração entre os Pipelines do Distilabel e a interface de inferência disponibilizada pelo Ollama.

Foram desenvolvidas três configurações experimentais:

**DL-01A — Geração textual livre:** utilização de instruções em linguagem natural para produzir exemplos fictícios de eventos de segurança, sem exigir que a saída correspondesse a um objeto JSON.

**DL-01B — Geração com JSON solicitado:** utilização de instruções direcionadas à produção de eventos em formato JSON, com posterior verificação da estrutura e dos campos gerados.

**DL-01C — Geração condicionada por JSON Schema:** utilização de esquemas explícitos para restringir a estrutura das respostas e permitir a validação automática com Pydantic.

O DL-01C contemplou três categorias de eventos: autenticação malsucedida (`failed_login`), bloqueio de conexão por firewall (`firewall_block`) e execução de processo (`process_execution`).

As execuções finais do DL-01C utilizaram temperatura igual a zero, semente de geração igual a 42, limite de 300 tokens e desabilitação explícita do cache do Pipeline por meio de `use_cache=False`.

Foram realizadas verificações de conformidade estrutural, tipos de dados, timestamps, endereços IP, identificadores de processos e coerência entre campos.

A avaliação de repetibilidade envolveu três execuções adicionais sob a mesma configuração, com preservação dos arquivos produzidos e comparação de assinaturas SHA-256.

Por fim, foi realizada uma análise exploratória de plausibilidade operacional, identificando características relevantes e limitações dos eventos sintéticos gerados.

## 4. Resultados da Geração

Foram realizadas três configurações experimentais para investigar a capacidade de geração de registros sintéticos de segurança utilizando Distilabel e Qwen3 0.6B.

Cada configuração produziu três registros, totalizando nove registros na avaliação inicial.

| Experimento | Abordagem | Registros gerados | Objetos JSON válidos |
|---|---|---:|---:|
| DL-01A | Geração textual livre | 3 | 0 |
| DL-01B | Geração com JSON solicitado | 3 | 3 |
| DL-01C | Geração condicionada por JSON Schema | 3 | 3 |

### 4.1. DL-01A — Geração Textual Livre

A primeira configuração utilizou instruções em linguagem natural para solicitar exemplos fictícios de eventos de segurança computacional.

O Pipeline gerou três respostas textuais contendo informações relacionadas a autenticação malsucedida, bloqueio de conexão por firewall e execução de processos.

Embora as respostas apresentassem conteúdos relacionados aos cenários solicitados, nenhuma delas correspondeu integralmente a um objeto JSON válido.

Esse resultado evidencia uma limitação da abordagem textual livre para situações que exigem processamento automatizado e padronização dos registros.

### 4.2. DL-01B — Geração com JSON Solicitado

A segunda configuração buscou obter registros estruturados em JSON por meio de instruções de geração.

Foram produzidos três registros representados por objetos JSON sintaticamente válidos.

Entretanto, a aplicação posterior de regras de validação identificou uma inconsistência de tipo no evento de firewall: o atributo `destination_port` foi representado como texto, embora o esquema exigisse um número inteiro.

Consequentemente, dois dos três registros atenderam integralmente às regras de validação implementadas.

### 4.3. DL-01C — Geração Condicionada por JSON Schema

A terceira configuração utilizou esquemas JSON explícitos para orientar a geração dos eventos.

Foram contempladas três categorias: login malsucedido, bloqueio de firewall e execução de processo.

Os três registros gerados apresentaram conformidade com os respectivos esquemas e foram aprovados na validação realizada com Pydantic.

O resultado indica que a utilização de esquemas explícitos foi eficaz para assegurar a conformidade estrutural dos exemplos produzidos nas condições avaliadas.

Entretanto, considerando o tamanho reduzido da amostra e as diferenças entre as configurações experimentais, os resultados não permitem afirmar superioridade geral da abordagem sobre as demais.

## 5. Avaliação de Qualidade

A avaliação de qualidade concentrou-se na conformidade estrutural, na validade dos tipos de dados e na consistência básica dos atributos produzidos.

Foram utilizados procedimentos automatizados de análise e validação, incluindo interpretação de JSON, modelos Pydantic e verificações específicas de domínio.

### 5.1. Conformidade Estrutural

Os resultados demonstraram diferenças entre as três abordagens experimentais.

| Indicador | DL-01A | DL-01B | DL-01C |
|---|---:|---:|---:|
| Registros gerados | 3 | 3 | 3 |
| Objetos JSON válidos | 0 | 3 | 3 |
| Registros aprovados nos esquemas | Não avaliado | 2 | 3 |
| Registros reprovados nos esquemas | Não avaliado | 1 | 0 |

A configuração DL-01C alcançou aprovação de 100% nos três registros avaliados.

Contudo, essa proporção representa exclusivamente a amostra exploratória utilizada, não constituindo uma estimativa robusta de desempenho em conjuntos de dados maiores.

### 5.2. Validação de Campos

Foram aplicadas verificações sobre atributos relevantes para registros de segurança computacional.

Entre os critérios examinados, destacam-se:

- Validade sintática dos timestamps.
- Validade dos endereços IPv4.
- Representação numérica das portas de destino.
- Utilização de identificadores positivos de processos.
- Consistência entre categorias e tipos de eventos.
- Presença de atributos obrigatórios.

Todos os registros do DL-01C atenderam aos critérios aplicáveis nas verificações realizadas.

### 5.3. Limites da Avaliação

A conformidade estrutural não equivale à qualidade integral de dados sintéticos.

Um registro pode apresentar campos válidos e, simultaneamente, conter informações pouco representativas de um ambiente operacional real.

Portanto, os resultados desta seção devem ser interpretados como evidências de qualidade estrutural e consistência técnica básica, sem comprovação de fidelidade estatística ou realismo operacional abrangente.

## 6. Avaliação de Diversidade

A avaliação exploratória de diversidade considerou a variedade de categorias representadas e a ocorrência de registros duplicados.

O experimento DL-01C produziu três eventos pertencentes a categorias distintas:

| Categoria | Tipo de evento | Quantidade |
|---|---|---:|
| Login | `failed_login` | 1 |
| Firewall | `firewall_block` | 1 |
| Processo | `process_execution` | 1 |
| **Total** | | **3** |

A análise dos eventos não identificou duplicatas exatas entre os três registros.

A distribuição observada decorre das instruções experimentais, que solicitaram explicitamente uma geração para cada categoria.

Consequentemente, a presença de três categorias distintas não demonstra, isoladamente, capacidade de produzir diversidade espontânea.

### 6.1. Diversidade Temporal

Os eventos apresentaram timestamps entre 5 e 15 de outubro de 2023.

A amplitude temporal observada foi de dez dias e trinta minutos.

Essa distribuição evidencia diferenças temporais entre os registros, mas não permite avaliar adequadamente variabilidade cronológica, sazonalidade ou padrões de ocorrência.

### 6.2. Limitações da Diversidade

O número reduzido de registros impede a realização de análises estatísticas representativas.

Não foram avaliadas sistematicamente distribuições de frequências, diversidade de usuários, variação de endereços IP, combinações de atributos ou correlações entre eventos.

Além disso, a existência de categorias diferentes foi determinada previamente pelo desenho experimental.

Portanto, a avaliação realizada confirma apenas a ausência de duplicatas exatas e a representação das três categorias solicitadas.

Investigações futuras deverão considerar amostras maiores e métricas específicas para diversidade de dados sintéticos.

## 7. Avaliação de Consistência

A avaliação de consistência investigou a compatibilidade entre atributos dos eventos sintéticos, suas categorias e as regras estabelecidas para o experimento DL-01C.

Foi desenvolvido o script `evaluate_dl01_semantics.py`, responsável pela aplicação de verificações determinísticas sobre os registros produzidos.

### 7.1. Coerência entre Campos

Foram examinadas três categorias de eventos:

| Categoria | Critérios examinados | Resultado |
|---|---|---|
| Login | Timestamp, tipo de evento, status, identificação do usuário e endereço IP | Aprovado |
| Firewall | Timestamp, tipo de evento, ação, porta e endereços IP | Aprovado |
| Processo | Timestamp, tipo de evento, identificação do processo e PID | Aprovado |

Os três registros atenderam às regras implementadas, correspondendo a uma taxa de aprovação de 100% na amostra avaliada.

Entretanto, parte dessas verificações reproduz restrições previamente estabelecidas nos esquemas de geração. Assim, a aprovação não representa uma avaliação semântica completamente independente.

### 7.2. Plausibilidade Operacional

Uma avaliação complementar foi realizada com o script `evaluate_dl01_realism.py`, considerando características relevantes para a interpretação dos eventos em contextos de cibersegurança.

No evento de login malsucedido, identificou-se a ausência de informações sobre tentativas anteriores de autenticação, o que limita análises de comportamentos recorrentes.

No evento de firewall, foram identificados os atributos de origem, destino, porta e ação. Os endereços utilizados foram classificados como não globais ou reservados, característica compatível com a construção de exemplos fictícios.

No evento de execução de processo, constatou-se a ausência de informações sobre o caminho do executável, a linha de comando e o processo pai, atributos relevantes para investigações de segurança mais detalhadas.

### 7.3. Interpretação

Os resultados indicam que o DL-01C produziu registros coerentes com as regras determinísticas definidas.

Entretanto, a consistência básica dos atributos não comprova a fidelidade operacional dos eventos, nem sua adequação a cenários complexos de investigação de incidentes.

A avaliação de plausibilidade foi descritiva e exploratória, sem aplicação de uma escala validada de realismo.

## 8. Reprodutibilidade

A avaliação de repetibilidade investigou a estabilidade dos registros produzidos pelo DL-01C em execuções sucessivas realizadas no mesmo ambiente experimental.

### 8.1. Configuração

As execuções utilizaram o modelo `qwen3:0.6b`, disponibilizado pelo Ollama 0.40.17 e integrado ao Distilabel 1.5.3.

Foram mantidos os seguintes parâmetros:

| Parâmetro | Valor |
|---|---|
| Modelo | `qwen3:0.6b` |
| Identificador do modelo | `7df6b6e09427` |
| Temperatura | 0 |
| Seed | 42 |
| `num_predict` | 300 |
| Cache do Pipeline | `use_cache=False` |
| Python | 3.12.16 |

O script de referência foi preservado em `reproducibility/pipeline_reference.py`.

Sua assinatura SHA-256 foi registrada para permitir a identificação da implementação utilizada.

### 8.2. Procedimento Experimental

Foram realizadas três execuções adicionais do Pipeline DL-01C, preservadas individualmente nos arquivos `run_01.json`, `run_02.json` e `run_03.json`.

Cada execução produziu três registros, correspondentes às categorias de login, firewall e processo.

Os arquivos foram analisados quanto à quantidade de registros, à aprovação nos esquemas e à identidade dos conteúdos gerados.

### 8.3. Resultados

| Execução | Registros | Aprovados | SHA-256 |
|---|---:|---:|---|
| Run 01 | 3 | 3 | `e3ac452c15c6...` |
| Run 02 | 3 | 3 | `e3ac452c15c6...` |
| Run 03 | 3 | 3 | `e3ac452c15c6...` |

Os três arquivos apresentaram a mesma assinatura SHA-256 completa:

`e3ac452c15c611a773db6810ce95e5d56ef1fb605a2f09b5aa1fb46470ba87cd`

As comparações entre as execuções também identificaram igualdade integral dos eventos validados.

A configuração `use_cache=False` indica que o mecanismo de cache do Pipeline foi explicitamente desabilitado.

### 8.4. Interpretação

Os resultados demonstram repetibilidade observada das saídas sob as condições experimentais utilizadas.

Entretanto, não permitem afirmar determinismo universal do modelo nem reprodutibilidade em ambientes computacionais distintos.

A avaliação foi limitada a três execuções, conduzidas com a mesma implementação, modelo e infraestrutura.

Investigações futuras poderão avaliar a estabilidade dos resultados em diferentes versões, dispositivos e configurações de inferência.

## 9. Limitações

O experimento apresenta limitações técnicas e metodológicas que devem ser consideradas na interpretação de seus resultados.

**Tamanho reduzido da amostra:** cada abordagem experimental produziu apenas três registros, impossibilitando generalizações estatísticas sobre a qualidade dos dados sintéticos.

**Diferenças entre as configurações:** as abordagens DL-01A, DL-01B e DL-01C utilizaram estratégias distintas de geração. Portanto, a comparação é exploratória e não constitui um experimento controlado capaz de isolar todos os fatores responsáveis pelas diferenças observadas.

**Utilização de um único modelo:** os experimentos foram executados com o Qwen3 0.6B. Não foram realizadas comparações com outros modelos de linguagem.

**Avaliação semântica limitada:** a consistência foi examinada por regras determinísticas, sem avaliação independente sistemática realizada por especialistas em cibersegurança.

**Ausência de avaliação estatística de diversidade:** não foram investigadas distribuições de atributos, cobertura de cenários ou correlações entre registros em amostras representativas.

**Realismo operacional:** os registros gerados contêm informações suficientes para representar eventos simples, mas não necessariamente apresentam a riqueza contextual encontrada em logs operacionais.

**Repetibilidade restrita ao ambiente:** a identidade das saídas foi observada em três execuções realizadas sob as mesmas condições. Não houve reprodução independente em outro ambiente computacional.

**Dependências e avisos de compatibilidade:** durante o desenvolvimento, foram observados avisos relacionados ao Pydantic e à integração entre os componentes. Esses avisos não impediram as execuções finais, mas devem ser considerados em futuras atualizações das dependências.

**Ausência de avaliação do desempenho de SLMs:** não foram realizados experimentos de treinamento, ajuste fino ou avaliação de modelos utilizando os registros produzidos.

Dessa forma, os resultados devem ser compreendidos como evidências exploratórias da viabilidade técnica da geração estruturada de dados sintéticos, e não como demonstração conclusiva de sua qualidade ou aplicabilidade em ambientes reais de segurança.

## 10. Conclusão

O experimento DL-01 investigou exploratoriamente a utilização do Distilabel, integrado ao Ollama e ao modelo Qwen3 0.6B, para gerar registros sintéticos de eventos de segurança computacional.

Foram avaliadas três abordagens: geração textual livre (DL-01A), geração com JSON solicitado por instruções (DL-01B) e geração condicionada por esquemas explícitos (DL-01C).

Os resultados evidenciaram diferenças na conformidade estrutural das saídas. Enquanto a geração textual livre produziu respostas não estruturadas, a abordagem com JSON solicitado apresentou uma inconsistência de tipo em um dos três registros. Por sua vez, os três registros produzidos com esquemas explícitos foram aprovados nas verificações estruturais implementadas.

A avaliação de repetibilidade do DL-01C identificou resultados idênticos em três execuções adicionais, realizadas sob a mesma configuração experimental, com temperatura zero, semente 42 e cache do Pipeline explicitamente desabilitado. A igualdade foi confirmada por comparações dos eventos e assinaturas SHA-256 dos arquivos preservados.

As avaliações complementares demonstraram conformidade com regras determinísticas de coerência básica, mas também identificaram limitações relacionadas à contextualização dos eventos e à representatividade operacional dos dados.

Dessa forma, os resultados sustentam a viabilidade técnica da geração de pequenos conjuntos de eventos sintéticos estruturados mediante a integração entre Distilabel, Ollama e Qwen3 0.6B, nas condições examinadas.

Entretanto, a quantidade reduzida de registros, a ausência de avaliação estatística representativa e a inexistência de uma avaliação sistemática de realismo impedem generalizações sobre a qualidade dos dados produzidos.

Como continuidade, recomenda-se ampliar a quantidade de amostras, investigar outras configurações e modelos, aplicar métricas de diversidade e fidelidade e avaliar a utilidade dos dados sintéticos em tarefas concretas de cibersegurança.

O experimento constitui, portanto, uma etapa exploratória de fundamentação técnica e metodológica para investigações posteriores sobre geração e utilização de dados sintéticos no domínio da segurança computacional.

## 11. Referências

ARGILLA. **Distilabel: Documentation**. Disponível em: https://distilabel.argilla.io/. Acesso em: 23 nov. 2026.

ARGILLA. **Distilabel: Source Code Repository**. GitHub. Disponível em: https://github.com/argilla-io/distilabel. Acesso em: 23 nov. 2026.

OLLAMA. **Ollama Documentation**. Disponível em: https://docs.ollama.com/. Acesso em: 23 nov. 2026.

OLLAMA. **Ollama Python Library**. GitHub. Disponível em: https://github.com/ollama/ollama-python. Acesso em: 23 nov. 2026.

PYDANTIC. **Pydantic Documentation**. Disponível em: https://docs.pydantic.dev/. Acesso em: 23 nov. 2026.

PYTHON SOFTWARE FOUNDATION. **Python 3.12 Documentation**. Disponível em: https://docs.python.org/3.12/. Acesso em: 23 nov. 2026.

QWEN TEAM. **Qwen3 Technical Report**. arXiv, 2025. Disponível em: https://arxiv.org/abs/2505.09388.

As referências documentam as tecnologias utilizadas e fornecem fontes para consulta sobre suas interfaces, funcionalidades e características técnicas.

## 12. Procedimento de Reprodução

Esta seção apresenta os principais procedimentos necessários para executar novamente o experimento DL-01C no ambiente utilizado.

### 12.1. Pré-requisitos

O experimento foi conduzido com os seguintes componentes:

- macOS;
- Python 3.12.16;
- Distilabel 1.5.3;
- Ollama 0.40.17;
- Modelo Qwen3 0.6B;
- Bibliotecas Python necessárias aos Pipelines.

A execução pressupõe que as dependências estejam instaladas e que o serviço Ollama esteja acessível.

### 12.2. Acessar o Ambiente

No Terminal:

```bash
cd ~/Documents/experimentos-dados-sinteticos/distilabel/distilabel
```

Verificar a versão do Python:

```bash
.venv/bin/python --version
```

Verificar o Distilabel:

```bash
uv pip show --python .venv/bin/python distilabel
```

Verificar o Ollama:

```bash
ollama --version
```

Verificar o modelo:

```bash
ollama list
```

### 12.3. Verificar a Disponibilidade do Ollama

Consultar a API local:

```bash
curl http://localhost:11434/api/tags
```

O resultado deverá apresentar o modelo `qwen3:0.6b` entre os modelos disponíveis.

### 12.4. Executar o Pipeline Principal

Executar:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01_schema_all.py
```

O script realiza a geração dos eventos das três categorias e executa as validações estruturais previstas.

O arquivo consolidado é armazenado em:

`results/distilabel/DL-01/generated_events_schema_all.json`

### 12.5. Executar a Avaliação de Consistência

```bash
.venv/bin/python ../scripts/evaluate_dl01_semantics.py
```

O procedimento gera o arquivo:

`results/distilabel/DL-01/semantic_evaluation.json`

### 12.6. Executar a Avaliação de Plausibilidade

```bash
.venv/bin/python ../scripts/evaluate_dl01_realism.py
```

O procedimento gera o arquivo:

`results/distilabel/DL-01/realism_evaluation.json`

### 12.7. Verificar a Integridade

Calcular o SHA-256:

```bash
shasum -a 256 \
  ../../results/distilabel/DL-01/generated_events_schema_all.json
```

A assinatura obtida poderá ser utilizada para comparar os arquivos produzidos em diferentes execuções.

Entretanto, uma assinatura distinta não implica necessariamente falha de reprodução, pois saídas generativas podem apresentar variações.

### 12.8. Repetibilidade

Para reproduzir a avaliação exploratória de repetibilidade, executar o Pipeline três vezes, preservando os resultados em arquivos separados.

Os resultados originais da avaliação foram armazenados em:

- `reproducibility/run_01.json`
- `reproducibility/run_02.json`
- `reproducibility/run_03.json`

A comparação deverá considerar tanto os arquivos completos quanto os eventos validados, permitindo distinguir diferenças de metadados de eventuais diferenças nos conteúdos gerados.

### 12.9. Considerações

A reprodução exige atenção às versões das dependências, à identificação do modelo, à disponibilidade do serviço Ollama e às configurações de inferência.

O procedimento descrito pressupõe um ambiente previamente configurado. O tutorial complementar deverá detalhar a instalação inicial das dependências, os problemas de compatibilidade encontrados e suas respectivas soluções.

## 13. Artefatos do Experimento

Os artefatos produzidos durante o experimento DL-01 foram organizados em diretórios específicos para permitir a rastreabilidade das configurações experimentais, das etapas de geração e das avaliações realizadas.

### 13.1. Scripts de Geração

| Arquivo | Finalidade |
|---|---|
| `pipeline_dl01.py` | Geração inicial de eventos em formato textual livre |
| `pipeline_dl01_structured.py` | Geração de registros com estrutura JSON solicitada por instruções |
| `pipeline_dl01_schema.py` | Experimentação inicial com geração condicionada por esquema |
| `pipeline_dl01_schema_all.py` | Geração estruturada das três categorias de eventos, com validação dos esquemas |

O arquivo `pipeline_dl01_schema_all.py` constitui a implementação principal utilizada na configuração experimental DL-01C.

### 13.2. Scripts de Análise e Validação

| Arquivo | Finalidade |
|---|---|
| `analyze_dl01.py` | Análise inicial dos registros produzidos |
| `compare_dl01.py` | Comparação entre as abordagens experimentais |
| `validate_dl01_structured.py` | Validação dos registros produzidos na abordagem DL-01B |
| `evaluate_dl01_semantics.py` | Verificação determinística de coerência básica entre campos |
| `evaluate_dl01_realism.py` | Avaliação descritiva de plausibilidade operacional |

### 13.3. Scripts Auxiliares

Foram desenvolvidos scripts para investigar o comportamento da integração entre Distilabel e Ollama, incluindo:

- `test_ollama_json.py`: investigação da geração de respostas JSON.
- `test_distilabel_no_think.py`: investigação do comportamento da geração com o modo de raciocínio desativado.
- `test_json_schema.py`: teste de geração condicionada por esquema JSON.

Também foram preservadas cópias de segurança utilizadas durante o desenvolvimento e a resolução de problemas de execução.

Esses arquivos auxiliares documentam decisões técnicas, mas não constituem resultados experimentais independentes.

### 13.4. Arquivos de Resultados

Os resultados foram armazenados no diretório:

`results/distilabel/DL-01/`

Entre os principais artefatos estão:

| Arquivo | Conteúdo |
|---|---|
| `generated_events_free.json` | Registros da geração textual livre |
| `generated_events_structured.json` | Registros da geração com JSON solicitado |
| `generated_events_schema_all.json` | Registros estruturados das três categorias |
| `analysis_dl01.json` | Análise inicial da geração |
| `validation_structured.json` | Resultado da validação da abordagem DL-01B |
| `comparison_dl01.json` | Comparação entre as abordagens experimentais |
| `semantic_evaluation.json` | Avaliação de coerência básica |
| `realism_evaluation.json` | Avaliação exploratória de plausibilidade operacional |

Além desses arquivos, foram preservados resultados de testes intermediários de integração e geração condicionada.

### 13.5. Artefatos de Repetibilidade

Os arquivos relacionados à avaliação de repetibilidade foram organizados em:

`results/distilabel/DL-01/reproducibility/`

Esse diretório contém o script de referência e os resultados das três execuções preservadas:

- `pipeline_reference.py`
- `run_01.json`
- `run_02.json`
- `run_03.json`

As três execuções apresentaram arquivos com conteúdo idêntico, verificado por meio de assinaturas SHA-256.

A preservação desses artefatos permite auditar os resultados obtidos no ambiente experimental, embora não substitua a necessidade de reprodução independente em outros ambientes.

### 13.6. Organização e Disponibilização

Os scripts, relatórios e resultados selecionados serão organizados para disponibilização no repositório GitHub do projeto *Experimentos de Geração de Dados Sintéticos para Cibersegurança*.

A publicação deverá preservar os artefatos necessários à compreensão e à reprodução dos experimentos, evitando a inclusão de ambientes virtuais, caches, dependências instaladas e cópias integrais de repositórios de terceiros.

A disponibilização também deverá considerar a identificação das versões utilizadas, a integridade dos arquivos publicados e a documentação das limitações experimentais.

Os resultados apresentados neste relatório constituem evidências exploratórias da utilização do Distilabel para geração estruturada de eventos sintéticos de cibersegurança.