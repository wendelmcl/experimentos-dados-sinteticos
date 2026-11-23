# Tutorial Técnico — Reprodução dos Experimentos com Distilabel

**Projeto:** Experimentos de Geração de Dados Sintéticos para Cibersegurança
**Experimento:** DL-01
**Ferramenta:** Distilabel 1.5.3
**Modelo:** Qwen3 0.6B
**Infraestrutura de inferência:** Ollama 0.40.17
**Python:** 3.12.16
**Sistema operacional:** macOS
**Data do experimento:** 23 de novembro de 2026

---

## 1. Apresentação

Este tutorial documenta os procedimentos técnicos utilizados na instalação, configuração, execução e avaliação dos experimentos de geração de dados sintéticos realizados com o Distilabel.

O objetivo é permitir a compreensão das etapas executadas e fornecer instruções para reproduzir os experimentos em um ambiente compatível.

O documento apresenta os comandos utilizados, suas respectivas funções, os principais problemas encontrados e as soluções adotadas.

Os experimentos foram organizados em três configurações:

- **DL-01A:** geração textual livre de eventos de segurança.
- **DL-01B:** geração de eventos com formato JSON solicitado por instruções.
- **DL-01C:** geração de eventos condicionada por esquemas JSON, com validação automatizada.

A documentação também contempla os procedimentos de avaliação estrutural, consistência semântica básica, plausibilidade operacional e repetibilidade.

Os resultados técnicos e científicos desses experimentos estão descritos separadamente no relatório `DL-01_Distilabel.md`.

## 2. Organização do Tutorial

O tutorial está organizado nas seguintes seções:

1. Apresentação.
2. Organização do Tutorial.
3. Requisitos e Preparação do Ambiente.
4. Obtenção do Código-fonte do Distilabel.
5. Configuração do Ambiente Virtual Python.
6. Instalação e Verificação das Dependências.
7. Instalação e Configuração do Ollama.
8. Preparação do Modelo Qwen3 0.6B.
9. Integração entre Distilabel e Ollama.
10. Desenvolvimento do Experimento DL-01A.
11. Desenvolvimento do Experimento DL-01B.
12. Desenvolvimento do Experimento DL-01C.
13. Validação Estrutural dos Dados.
14. Avaliação de Consistência Semântica.
15. Avaliação de Plausibilidade Operacional.
16. Avaliação de Repetibilidade.
17. Problemas Encontrados e Soluções.
18. Organização dos Artefatos Gerados.
19. Procedimento Resumido de Reprodução.
20. Considerações Finais.

## 3. Requisitos e Preparação do Ambiente

Os experimentos foram desenvolvidos em um computador com sistema operacional macOS.

O ambiente utilizado apresentou os seguintes componentes:

| Componente | Versão |
|---|---|
| Python | 3.12.16 |
| Distilabel | 1.5.3 |
| Ollama | 0.40.17 |
| Modelo de linguagem | Qwen3 0.6B |
| Gerenciador de pacotes Python | uv |

O projeto foi organizado no diretório:

`~/Documents/experimentos-dados-sinteticos/`

A estrutura principal contempla os diretórios destinados às ferramentas experimentais, aos resultados e à documentação.

O Distilabel foi utilizado como ferramenta de construção e execução de Pipelines, enquanto o Ollama disponibilizou a infraestrutura de inferência para o modelo Qwen3 0.6B.

O Pydantic foi utilizado na definição e validação dos esquemas de dados.

As etapas seguintes apresentam os procedimentos empregados para preparar esses componentes.

## 4. Obtenção do Código-fonte do Distilabel

O Distilabel é uma ferramenta de código aberto utilizada para construir Pipelines de geração e processamento de dados com modelos de linguagem.

Neste experimento, optou-se por obter o código-fonte diretamente do repositório oficial, permitindo consultar sua implementação e desenvolver scripts experimentais sem modificar diretamente os componentes originais.

### 4.1. Acessar o diretório do projeto

No Terminal:

```bash
cd ~/Documents/experimentos-dados-sinteticos/distilabel
```

**Função:** acessar o diretório reservado aos experimentos com Distilabel.

### 4.2. Clonar o repositório oficial

Executar:

```bash
git clone https://github.com/argilla-io/distilabel.git
```

**Função:** obter uma cópia local do código-fonte do Distilabel, incluindo exemplos, testes e arquivos de configuração.

Após a clonagem, foi criado o diretório:

`distilabel/distilabel/`

### 4.3. Acessar o repositório clonado

```bash
cd distilabel
```

**Função:** acessar a raiz do projeto original, onde estão localizados `pyproject.toml`, `src`, `examples` e os demais componentes.

### 4.4. Identificar a revisão utilizada

O comando:

```bash
git rev-parse HEAD
```

retornou:

```text
313fac85b1a2472dd88db1a31c2b754599f46476
```

Esse identificador representa a revisão do repositório consultada durante a preparação experimental.

Registrar a revisão é importante porque o código-fonte pode sofrer alterações ao longo do tempo.

### 4.5. Verificar os requisitos de Python

Foi utilizado:

```bash
grep "requires-python" pyproject.toml
```

O resultado indicou:

```text
requires-python = ">=3.9"
```

Portanto, o projeto consultado declarava compatibilidade com Python a partir da versão 3.9.

Para o experimento, foi selecionado o Python 3.12.16, disponível no ambiente macOS utilizado.

### 4.6. Organização do Repositório

O código original foi mantido separado dos scripts experimentais.

A estrutura utilizada foi:

```text
experimentos-dados-sinteticos/
├── distilabel/
│   ├── distilabel/
│   │   ├── src/
│   │   ├── examples/
│   │   ├── pyproject.toml
│   │   └── ...
│   └── scripts/
├── results/
│   └── distilabel/
│       └── DL-01/
└── reports/
```

O diretório `distilabel/distilabel/` foi posteriormente incluído no `.gitignore` do projeto principal, evitando incorporar uma cópia integral do repositório de terceiros à publicação dos experimentos.

## 5. Configuração do Ambiente Virtual Python

A execução dos experimentos foi realizada em um ambiente virtual Python, permitindo separar as dependências utilizadas das instalações globais do sistema.

### 5.1. Verificar as versões disponíveis

Durante a preparação, foi executado:

```bash
uv python list --only-installed
```

**Função:** apresentar as versões do Python disponíveis no computador.

Foram identificadas instalações das versões 3.9, 3.12 e 3.14.

Optou-se pela utilização do Python 3.12.16 no ambiente experimental.

### 5.2. Criar o ambiente virtual

A partir da raiz do código-fonte clonado, o ambiente pode ser criado com:

```bash
uv venv --python 3.12 .venv
```

**Função:** criar um ambiente virtual denominado `.venv` utilizando Python 3.12.

Este comando é apresentado como procedimento de reconstrução do ambiente, não como transcrição de uma saída histórica de criação.

Caso já exista um ambiente virtual configurado, não é necessário recriá-lo.

### 5.3. Verificar o interpretador

Foi utilizado:

```bash
.venv/bin/python --version
```

O resultado observado foi:

```text
Python 3.12.16
```

Isso confirmou que os experimentos utilizariam o interpretador Python selecionado.

### 5.4. Organização das Dependências

O ambiente virtual foi mantido no diretório:

`distilabel/distilabel/.venv/`

Os comandos de instalação e execução utilizaram explicitamente `.venv/bin/python`, evitando ambiguidades com outras versões do Python instaladas no computador.

O diretório `.venv` não deve ser publicado no GitHub. Em uma reprodução independente, recomenda-se criar um novo ambiente e instalar as dependências necessárias.

## 6. Instalação e Verificação das Dependências

Após a configuração do ambiente virtual, foram realizados procedimentos de instalação e verificação das bibliotecas necessárias.

### 6.1. Instalação do Distilabel

A partir da raiz do código-fonte clonado, foi executado:

```bash
uv pip install --python .venv/bin/python -e .
```

**Função:** instalar o projeto localmente em modo editável, permitindo utilizar o código-fonte do diretório clonado.

A instalação identificou a versão:

`distilabel==1.5.3`

### 6.2. Diagnóstico de Importação

Inicialmente, o comando:

```bash
.venv/bin/python -c "import distilabel; print(distilabel.__file__)"
```

produziu o erro:

```text
ModuleNotFoundError: No module named 'distilabel'
```

Apesar de a instalação constar nos metadados do ambiente, o interpretador não localizou o módulo naquele teste.

Foi verificada a presença do arquivo:

`src/distilabel/__init__.py`

Para confirmar o acesso ao código-fonte, utilizou-se:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python -c \
  "import distilabel; print(distilabel.__file__); print(distilabel.__version__)"
```

O comando identificou o módulo no diretório `src/distilabel/` e confirmou a versão 1.5.3.

A configuração de `PYTHONPATH` foi posteriormente utilizada na execução dos Pipelines.

### 6.3. Instalação da Biblioteca Requests

Durante os testes de importação dos componentes do Pipeline, foi identificado:

```text
ModuleNotFoundError: No module named 'requests'
```

O pacote foi instalado com:

```bash
uv pip install --python .venv/bin/python requests
```

A instalação disponibilizou a versão 2.34.2 do Requests no ambiente experimental.

A verificação foi realizada com:

```bash
.venv/bin/python -c "import requests; print(requests.__version__)"
```

### 6.4. Teste dos Componentes do Pipeline

Após a instalação, foram verificados os componentes:

- `Pipeline`
- `LoadDataFromDicts`
- `TextGeneration`

Foi executado o seguinte código:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python - <<'PY'
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration

print("Pipeline: OK")
print("LoadDataFromDicts: OK")
print("TextGeneration: OK")
PY
```

O teste apresentou:

```text
Pipeline: OK
LoadDataFromDicts: OK
TextGeneration: OK
```

Isso confirmou a disponibilidade dos componentes essenciais para os experimentos.

### 6.5. Dependências Complementares

Durante o desenvolvimento, também foram instaladas bibliotecas auxiliares.

Para disponibilizar a integração Python com o Ollama:

```bash
uv pip install --python .venv/bin/python ollama
```

A versão identificada foi `ollama==0.6.3`.

Para resolver uma dependência relacionada ao processamento de dados:

```bash
uv pip install --python .venv/bin/python beautifulsoup4
```

A instalação disponibilizou `beautifulsoup4==4.15.0`.

A ausência do módulo `bs4` foi identificada durante uma execução inicial do Pipeline.

### 6.6. Considerações sobre Compatibilidade

Durante os testes, foram observados avisos do Pydantic relacionados à utilização de atributos de campos e validadores.

Os avisos não impediram as execuções finais documentadas, mas indicam aspectos de compatibilidade que devem ser considerados em atualizações futuras.

Para reproduções posteriores, recomenda-se registrar as versões efetivamente instaladas e evitar atualizações indiscriminadas de dependências sem testes de regressão.

## 7. Instalação e Configuração do Ollama

O Ollama foi utilizado como infraestrutura de inferência para disponibilizar modelos de linguagem por meio de uma API local.

Essa abordagem permitiu integrar o Distilabel a um modelo executado no computador, sem depender de uma API comercial para o experimento principal.

### 7.1. Instalação do Ollama

O Ollama pode ser obtido em:

https://ollama.com/download

No macOS, a instalação pode ser realizada pelo aplicativo disponibilizado oficialmente.

Após a instalação, é necessário iniciar o aplicativo para disponibilizar o serviço de inferência.

### 7.2. Verificar a instalação

Durante a preparação experimental, foi executado:

```bash
ollama --version
```

Inicialmente, o Terminal apresentou:

```text
zsh: command not found: ollama
```

Esse erro indicou que o executável não estava disponível naquela sessão do Terminal.

Após a instalação e abertura de uma nova sessão, o comando foi executado novamente e retornou:

```text
ollama version is 0.40.17
```

Isso confirmou a disponibilidade do Ollama no ambiente.

### 7.3. Verificar os modelos disponíveis

Foi utilizado:

```bash
ollama list
```

O comando apresenta os modelos registrados no Ollama.

Durante o experimento, foram identificados:

- `qwen3:0.6b`: modelo local utilizado nas gerações.
- `glm-5.3-flash:cloud`: modelo remoto disponível na instalação, mas não utilizado nas avaliações principais.

### 7.4. Verificar o funcionamento da API

Foi executado:

```bash
curl http://localhost:11434/api/tags
```

**Função:** consultar o endpoint HTTP responsável por listar os modelos disponíveis no serviço Ollama.

O retorno foi um objeto JSON contendo os modelos registrados.

O endereço `localhost:11434` corresponde ao endpoint local padrão utilizado no experimento.

### 7.5. Considerações sobre o serviço

O Ollama precisa estar acessível durante a execução dos Pipelines.

Caso o endpoint não responda, deve-se verificar se o aplicativo está em execução e se a porta utilizada corresponde à configuração do serviço.

A disponibilidade do aplicativo e da API deve ser confirmada antes de executar os scripts experimentais.

## 8. Preparação do Modelo Qwen3 0.6B

O modelo selecionado para os experimentos foi o Qwen3 0.6B, um modelo de linguagem de pequeno porte disponibilizado por meio do Ollama.

A escolha permitiu realizar testes de geração sintética em um ambiente computacional local.

### 8.1. Obter o modelo

Para obter o modelo em uma nova instalação, pode-se executar:

```bash
ollama pull qwen3:0.6b
```

**Função:** baixar e registrar o modelo no Ollama.

Caso o modelo já esteja disponível, não é necessário repetir o download.

### 8.2. Confirmar a disponibilidade

Executar:

```bash
ollama list
```

Durante o experimento, foram identificadas as seguintes informações:

| Propriedade | Valor |
|---|---|
| Modelo | `qwen3:0.6b` |
| Identificador exibido | `7df6b6e09427` |
| Tamanho aproximado em disco | 522 MB |

Esses dados identificam o modelo utilizado na instalação experimental.

### 8.3. Executar um teste interativo

Foi utilizado:

```bash
ollama run qwen3:0.6b
```

O comando abriu uma interface interativa, identificada pelo indicador:

```text
>>>
```

Foi enviada uma solicitação em português para explicar o conceito de log de segurança.

O modelo retornou uma resposta textual, confirmando sua capacidade de processar instruções e gerar conteúdo no ambiente local.

### 8.4. Tentativa de desativação do raciocínio

Durante os testes interativos, foram experimentados os comandos:

```text
/ no_think
```

e:

```text
/no_think
```

A interface retornou mensagens indicando comandos desconhecidos.

Portanto, essas tentativas não desativaram o modo de raciocínio.

Posteriormente, a configuração foi investigada por meio da API Python do Ollama, utilizando o parâmetro `think=False`.

### 8.5. Verificar o processamento do modelo

Foi executado:

```bash
ollama ps
```

**Função:** apresentar os modelos carregados em execução e informações sobre os recursos utilizados.

O comando confirmou a presença do Qwen3 0.6B na memória, com processamento pela GPU.

### 8.6. Encerrar a sessão interativa

Para sair da interface do Ollama, foi utilizado:

```text
/bye
```

O encerramento da sessão interativa não implica necessariamente descarregar imediatamente o modelo da memória.

## 9. Integração entre Distilabel e Ollama

Após confirmar o funcionamento do Ollama e do Qwen3 0.6B, foram realizados testes para verificar a integração entre o modelo e os componentes do Distilabel.

### 9.1. Instalar o cliente Python do Ollama

Na raiz do código-fonte clonado do Distilabel, foi executado:

```bash
uv pip install --python .venv/bin/python ollama
```

O pacote instalado disponibilizou a interface Python utilizada para a comunicação com o serviço Ollama.

A instalação foi verificada com:

```bash
.venv/bin/python -c "import ollama; print('Cliente Python Ollama: OK')"
```

Resultado:

```text
Cliente Python Ollama: OK
```

### 9.2. Importar a integração do Distilabel

Foi utilizado:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python - <<'PY'
from distilabel.models.llms import OllamaLLM

print("OllamaLLM: OK")
PY
```

O teste confirmou a disponibilidade da classe `OllamaLLM`.

Durante a importação foram apresentados avisos do Pydantic, mas a classe foi carregada corretamente.

### 9.3. Configurar o modelo

Foi criada uma instância de `OllamaLLM` com a seguinte configuração:

```python
from distilabel.models.llms import OllamaLLM

llm = OllamaLLM(
    model="qwen3:0.6b",
    host="http://localhost:11434",
    timeout=120
)
```

Os parâmetros utilizados possuem as seguintes funções:

| Parâmetro | Função |
|---|---|
| `model` | Identifica o modelo que deverá ser utilizado |
| `host` | Define o endereço do serviço Ollama |
| `timeout` | Define o limite de espera configurado para a comunicação |

### 9.4. Verificar a conexão

Foi realizado o carregamento do modelo:

```python
llm.load()
```

Após a inicialização, o teste confirmou a conexão com o Ollama.

O procedimento foi encerrado com:

```python
llm.unload()
```

**Função:** liberar os recursos associados à instância do modelo no contexto da integração.

### 9.5. Testar a geração de texto

Foi executada uma chamada utilizando:

```python
resultado = llm.generate_outputs(
    inputs=[
        [
            {
                "role": "user",
                "content": (
                    "Explique em duas frases, em português, "
                    "o que é uma tentativa de login malsucedida."
                )
            }
        ]
    ],
    num_generations=1
)
```

O retorno apresentou uma lista contendo a resposta gerada e estatísticas de utilização de tokens.

O teste confirmou que a integração conseguia enviar instruções ao modelo e receber respostas por meio do Distilabel.

### 9.6. Investigar as dependências de inferência

Durante a preparação foram verificados os pacotes:

- `openai`
- `ollama`
- `mlx`
- `transformers`

Inicialmente, esses componentes não estavam disponíveis no ambiente virtual.

Para o experimento, optou-se pela integração com Ollama, dispensando a instalação dos demais mecanismos de inferência.

### 9.7. Resultado da integração

Os testes confirmaram que:

1. O serviço Ollama estava acessível localmente.
2. O modelo Qwen3 0.6B estava disponível.
3. A classe `OllamaLLM` foi importada corretamente.
4. O carregamento da integração foi realizado.
5. Uma solicitação de geração textual retornou conteúdo e estatísticas de tokens.

Com isso, o ambiente estava preparado para o desenvolvimento dos Pipelines experimentais.

## 10. Desenvolvimento do Experimento DL-01A

O experimento DL-01A investigou a capacidade do Distilabel, integrado ao modelo Qwen3 0.6B por meio do Ollama, de produzir descrições sintéticas de eventos de segurança computacional utilizando instruções em linguagem natural.

Nesta primeira configuração, não foram impostas estruturas JSON obrigatórias aos conteúdos gerados.

### 10.1. Objetivo

Avaliar a geração textual livre de registros sintéticos de segurança, observando a presença de informações solicitadas, a organização das respostas e a adequação dos conteúdos ao contexto de cibersegurança.

### 10.2. Implementação

O script principal foi armazenado em:

`distilabel/scripts/pipeline_dl01.py`

Para consultar sua implementação:

```bash
cd ~/Documents/experimentos-dados-sinteticos/distilabel/distilabel
```

```bash
sed -n '1,220p' ../scripts/pipeline_dl01.py
```

O Pipeline foi desenvolvido utilizando os componentes `Pipeline`, `LoadDataFromDicts` e `TextGeneration`.

A implementação utilizou instruções relacionadas a três categorias:

1. Tentativa de autenticação malsucedida.
2. Conexão de rede bloqueada por firewall.
3. Execução de processo em um endpoint.

Cada instrução solicitava a criação de um exemplo fictício de evento de segurança.

### 10.3. Execução

O procedimento de execução foi:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01.py
```

O parâmetro `PYTHONPATH` foi utilizado para garantir o acesso ao código-fonte do Distilabel presente no diretório `src`.

A execução empregou o modelo `qwen3:0.6b`, disponibilizado pelo Ollama.

### 10.4. Resultados

Foram gerados três registros textuais, armazenados em:

`results/distilabel/DL-01/generated_events_free.json`

Os registros apresentaram respostas em linguagem natural contendo informações relacionadas aos cenários solicitados.

Entretanto, as respostas incluíram explicações adicionais, formatação Markdown e interpretações narrativas que não correspondiam a objetos JSON diretamente utilizáveis.

### 10.5. Análise inicial

A análise automatizada foi realizada pelo script:

`distilabel/scripts/analyze_dl01.py`

A execução pode ser reproduzida com:

```bash
.venv/bin/python ../scripts/analyze_dl01.py
```

A avaliação identificou três registros com os campos externos esperados preenchidos.

Nenhuma das três respostas, entretanto, foi classificada como objeto JSON.

O resultado indicou que a geração textual livre é capaz de produzir conteúdos descritivos, mas não garante uma representação estruturada apropriada para integração direta com sistemas de processamento de logs.

### 10.6. Limitações

A avaliação foi realizada com apenas três registros.

O experimento não estabeleceu medidas quantitativas de realismo, diversidade estatística ou desempenho de modelos de linguagem treinados com os dados gerados.

Seus resultados representam uma avaliação exploratória inicial.

## 11. Desenvolvimento do Experimento DL-01B

O experimento DL-01B investigou a geração de eventos sintéticos por meio de instruções que solicitavam explicitamente respostas em formato JSON.

Essa configuração foi elaborada para superar as limitações estruturais identificadas no experimento DL-01A.

### 11.1. Objetivo

Verificar se instruções de geração mais restritivas, associadas à configuração do modelo, permitiriam produzir objetos JSON com campos adequados às diferentes categorias de eventos de cibersegurança.

### 11.2. Implementação

O script foi armazenado em:

`distilabel/scripts/pipeline_dl01_structured.py`

Para consultar sua implementação:

```bash
sed -n '1,240p' ../scripts/pipeline_dl01_structured.py
```

Foram utilizadas instruções que solicitavam objetos JSON contendo informações específicas dos eventos.

Durante o desenvolvimento, foram investigados mecanismos de controle de geração do Ollama, incluindo a utilização do parâmetro `think=False`.

### 11.3. Investigação do modo JSON

Inicialmente, foram realizados testes de geração para verificar se o modelo retornava objetos JSON válidos.

O script auxiliar utilizado foi:

`distilabel/scripts/test_ollama_json.py`

Os testes demonstraram que a simples solicitação de JSON não assegurava necessariamente a obtenção de conteúdo válido por meio da integração utilizada naquele momento.

Em uma das tentativas, o modelo retornou uma resposta vazia.

Posteriormente, foi realizada uma chamada direta à API Python do Ollama, configurando os seguintes parâmetros:

```python
format="json",
think=False,
stream=False,
options={
    "temperature": 0,
    "seed": 42,
    "num_predict": 350
}
```

Essa configuração produziu um objeto JSON contendo os campos solicitados.

### 11.4. Execução do experimento

O Pipeline estruturado foi executado com:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01_structured.py
```

Os resultados foram armazenados em:

`results/distilabel/DL-01/generated_events_structured.json`

### 11.5. Validação

Foi desenvolvido o script:

`distilabel/scripts/validate_dl01_structured.py`

O procedimento pode ser executado com:

```bash
.venv/bin/python \
  ../scripts/validate_dl01_structured.py
```

O resultado da avaliação apresentou:

| Indicador | Resultado |
|---|---:|
| Registros avaliados | 3 |
| Objetos JSON identificados | 3 |
| Registros aprovados | 2 |
| Registros reprovados | 1 |

A reprovação ocorreu em um evento de firewall porque o campo `destination_port` foi gerado como string, enquanto o esquema de validação exigia um inteiro.

### 11.6. Comparação com DL-01A

A comparação foi realizada pelo script:

`distilabel/scripts/compare_dl01.py`

O comando utilizado foi:

```bash
.venv/bin/python ../scripts/compare_dl01.py
```

A avaliação identificou:

- DL-01A: três respostas textuais e nenhum objeto JSON.
- DL-01B: três respostas JSON, sendo duas aprovadas nas regras de validação.

Esse resultado demonstrou uma melhoria na conformidade estrutural das respostas no conjunto analisado.

Entretanto, as configurações de geração não foram idênticas entre as abordagens, impedindo atribuir as diferenças observadas exclusivamente ao formato solicitado.

### 11.7. Limitações

A abordagem ainda apresentou inconsistência de tipos.

A validação foi realizada sobre uma amostra reduzida, e os resultados não comprovam que a geração de JSON seja estável em cenários mais amplos.

Essas limitações motivaram a investigação da geração condicionada por esquemas, desenvolvida no experimento DL-01C.

## 12. Desenvolvimento do Experimento DL-01C

O experimento DL-01C investigou a geração de eventos sintéticos de cibersegurança condicionada por esquemas JSON, utilizando o Distilabel, o Ollama e modelos de validação definidos com Pydantic.

Essa configuração constituiu a abordagem mais estruturada entre as três investigadas.

### 12.1. Objetivo

Avaliar a capacidade de produzir registros sintéticos estruturalmente válidos para diferentes categorias de eventos de segurança, utilizando esquemas específicos e validação automatizada.

### 12.2. Categorias de eventos

Foram utilizadas três categorias:

| Categoria | Tipo de evento | Informações principais |
|---|---|---|
| Login | `failed_login` | Timestamp, usuário, IP de origem e status |
| Firewall | `firewall_block` | Timestamp, IPs, porta de destino e ação |
| Processo | `process_execution` | Timestamp, hostname, processo, usuário e PID |

Cada categoria foi associada a um esquema que estabelecia os campos esperados e seus respectivos tipos.

### 12.3. Implementação

O script principal foi armazenado em:

`distilabel/scripts/pipeline_dl01_schema_all.py`

Sua implementação pode ser consultada com:

```bash
sed -n '1,240p' ../scripts/pipeline_dl01_schema_all.py
```

O código utilizou a classe `OllamaLLM` como base para uma integração adaptada à geração condicionada por esquema.

As configurações utilizadas incluíram:

```python
"temperature": 0,
"seed": 42,
"num_predict": 300
```

A execução também utilizou:

```python
pipeline.run(use_cache=False)
```

Essa configuração evitou reutilizar os resultados em cache do Pipeline.

### 12.4. Problema de multiprocessing no macOS

Durante as primeiras execuções, foi identificado um erro relacionado à inicialização de subprocessos.

O rastreamento apresentou uma exceção `EOFError` durante o mecanismo de multiprocessing do Python.

O problema foi associado à forma como o script principal era executado no macOS, utilizando o método `spawn`.

A implementação foi reorganizada para proteger a inicialização do programa e evitar a execução indevida de instruções principais durante a importação pelos subprocessos.

Após essa correção, os Pipelines foram executados com sucesso.

### 12.5. Execução do experimento

A partir da raiz do código-fonte do Distilabel, foi utilizado:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01_schema_all.py
```

O script executou as três categorias de eventos.

Os registros gerados foram armazenados em:

`results/distilabel/DL-01/generated_events_schema_all.json`

### 12.6. Resultado da geração

A execução final apresentou:

| Indicador | Resultado |
|---|---:|
| Categorias executadas | 3 |
| Registros gerados | 3 |
| Registros aprovados pelo esquema | 3 |
| Registros reprovados | 0 |

Os três eventos foram identificados como objetos JSON estruturalmente válidos.

### 12.7. Validação dos dados

A implementação utilizou modelos Pydantic específicos para as categorias de login, firewall e processo.

Os modelos verificaram a presença de campos obrigatórios, seus tipos e determinadas restrições de domínio.

Na categoria de firewall, por exemplo, a porta de destino foi representada como inteiro e validada dentro de limites previamente definidos.

### 12.8. Avaliação de consistência

Foram realizadas verificações adicionais relacionadas a:

- Estrutura dos registros.
- Formato dos timestamps.
- Validade dos endereços IP.
- Coerência de tipos e valores.
- Identificadores de processo.
- Presença de informações exigidas por categoria.

Os três registros passaram nas verificações determinísticas de consistência básica aplicadas.

### 12.9. Avaliação de plausibilidade operacional

A avaliação exploratória identificou limitações nos registros produzidos, incluindo:

- Endereços IP reservados ou não globais.
- Ausência de contexto adicional para tentativas de autenticação.
- Informações limitadas sobre a execução de processos.

Essas observações não invalidam automaticamente os eventos sintéticos, mas restringem sua interpretação como representações de situações operacionais reais.

### 12.10. Avaliação de repetibilidade

Foram realizadas três execuções independentes do procedimento experimental, com preservação dos resultados.

Os arquivos foram armazenados em:

`results/distilabel/DL-01/reproducibility/`

As três execuções apresentaram:

- Três registros por execução.
- Três registros aprovados por execução.
- Conteúdo idêntico nos arquivos JSON.
- Assinaturas SHA-256 coincidentes.

Esses resultados demonstram repetibilidade nas condições locais avaliadas.

Não estabelecem, entretanto, uma garantia geral de determinismo em outras versões de software, equipamentos ou ambientes de execução.

### 12.11. Conclusão do experimento

O DL-01C demonstrou a viabilidade de produzir eventos sintéticos estruturalmente válidos por meio da combinação de Distilabel, Ollama, geração condicionada por esquema e validação com Pydantic.

Em comparação com as abordagens anteriores, apresentou maior conformidade estrutural no conjunto exploratório analisado.

Entretanto, a aprovação estrutural e as verificações de consistência básica não são suficientes para estabelecer fidelidade estatística, realismo operacional ou adequação dos dados ao treinamento de SLMs.

Esses aspectos exigem avaliações adicionais com conjuntos mais amplos e critérios específicos.

## 13. Validação Estrutural dos Dados

A validação estrutural foi utilizada para verificar se os eventos sintéticos gerados apresentavam uma representação compatível com os esquemas definidos para cada categoria de segurança.

Essa etapa foi especialmente importante para identificar diferenças entre a geração textual livre, a solicitação de respostas JSON e a geração condicionada por esquemas.

### 13.1. Objetivo

Verificar a presença dos campos obrigatórios, os tipos de dados e determinadas restrições de domínio aplicáveis aos registros sintéticos.

A validação estrutural não determina se um evento ocorreu realmente ou se representa fielmente o comportamento de sistemas computacionais.

### 13.2. Validação do experimento DL-01A

A avaliação foi implementada no script:

`distilabel/scripts/analyze_dl01.py`

Para executá-lo, a partir do diretório `distilabel/distilabel/`:

```bash
.venv/bin/python ../scripts/analyze_dl01.py
```

O script analisou três registros, verificando os campos externos e o formato das respostas geradas.

Os resultados identificaram três registros completos quanto aos campos externos, mas nenhuma resposta classificada como objeto JSON.

### 13.3. Validação do experimento DL-01B

A validação foi realizada pelo script:

`distilabel/scripts/validate_dl01_structured.py`

Comando:

```bash
.venv/bin/python ../scripts/validate_dl01_structured.py
```

Os resultados foram armazenados em:

`results/distilabel/DL-01/validation_structured.json`

A análise apresentou:

| Indicador | Resultado |
|---|---:|
| Registros analisados | 3 |
| Registros válidos | 2 |
| Registros inválidos | 1 |
| Taxa de aprovação | 66,7% |

A reprovação ocorreu no evento de firewall, pois o campo `destination_port` apresentou um valor do tipo string, enquanto a validação exigia um inteiro.

Essa ocorrência demonstrou que uma resposta sintaticamente válida em JSON não necessariamente satisfaz os requisitos do esquema esperado.

### 13.4. Validação do experimento DL-01C

No DL-01C, foram utilizados modelos Pydantic para definir a estrutura dos eventos.

Cada categoria possuía seus próprios campos obrigatórios e restrições.

A implementação principal encontra-se em:

`distilabel/scripts/pipeline_dl01_schema_all.py`

O arquivo de resultados é:

`results/distilabel/DL-01/generated_events_schema_all.json`

Foram gerados três registros, correspondentes às categorias login, firewall e processo.

Todos foram aprovados na validação de esquema realizada pelo Pipeline.

| Categoria | Resultado |
|---|---|
| Login | Aprovado |
| Firewall | Aprovado |
| Processo | Aprovado |

A taxa de aprovação estrutural foi de 100% na amostra avaliada.

### 13.5. Verificação complementar

Os registros também foram submetidos a verificações de tipos e formatos, contemplando:

- Timestamps em representação ISO 8601.
- Endereços IP sintaticamente válidos.
- Portas de destino representadas como inteiros.
- Identificadores de processo com valores positivos.
- Campos obrigatórios conforme a categoria.

Essas verificações complementaram a validação estrutural inicial.

### 13.6. Interpretação

Os resultados evidenciaram diferenças entre as estratégias de geração utilizadas.

O DL-01A produziu conteúdo descritivo sem representação JSON. O DL-01B apresentou objetos JSON, mas registrou uma inconsistência de tipo. O DL-01C produziu três eventos aprovados pelos esquemas definidos.

Os resultados se restringem às configurações e amostras utilizadas e não permitem concluir que uma abordagem seja universalmente superior às demais.

## 14. Avaliação de Consistência Semântica

A avaliação de consistência semântica básica foi desenvolvida para complementar a validação estrutural dos registros gerados no experimento DL-01C.

Enquanto a validação estrutural verifica campos, tipos e restrições, a avaliação de consistência busca identificar possíveis contradições entre as informações presentes em um mesmo evento.

### 14.1. Objetivo

Verificar a coerência básica entre a categoria do evento, seus identificadores, seus valores e as informações complementares geradas.

A abordagem foi baseada em verificações determinísticas, sem empregar um avaliador humano ou outro modelo de linguagem como juiz.

### 14.2. Implementação

O script desenvolvido foi:

`distilabel/scripts/evaluate_dl01_semantics.py`

Para executar a avaliação:

```bash
.venv/bin/python ../scripts/evaluate_dl01_semantics.py
```

O script utiliza os registros presentes em:

`results/distilabel/DL-01/generated_events_schema_all.json`

O relatório produzido é armazenado em:

`results/distilabel/DL-01/semantic_evaluation.json`

### 14.3. Critérios avaliados

As verificações foram organizadas por categoria.

**Categoria Login**

Foram verificados:

- Validade do timestamp.
- Coerência do tipo de evento.
- Compatibilidade do status com uma autenticação malsucedida.
- Presença do identificador do usuário.
- Validade sintática do endereço IP de origem.

**Categoria Firewall**

Foram verificados:

- Validade do timestamp.
- Coerência do tipo de evento.
- Compatibilidade da ação com um bloqueio.
- Validade da porta de destino.
- Validade sintática dos endereços IP de origem e destino.

**Categoria Processo**

Foram verificados:

- Validade do timestamp.
- Coerência do tipo de evento.
- Presença do nome do processo.
- Validade do identificador do processo.

### 14.4. Resultados obtidos

O relatório apresentou:

| Categoria | Resultado |
|---|---|
| Login | Aprovado |
| Firewall | Aprovado |
| Processo | Aprovado |

Foram avaliados três registros, todos aprovados nas verificações implementadas.

A taxa de aprovação foi de 100% para os critérios determinísticos aplicados.

### 14.5. Interpretação

Os resultados demonstraram que os três eventos apresentavam coerência básica entre seus campos, segundo as regras programadas.

Entretanto, a avaliação não verificou se os eventos seriam representativos de sistemas operacionais reais ou de distribuições estatísticas encontradas em ambientes de produção.

Por exemplo, um evento de autenticação malsucedida pode apresentar campos coerentes e, ainda assim, não possuir informações suficientes para caracterizar uma campanha de ataques.

Portanto, a aprovação nessa etapa deve ser interpretada como evidência de consistência básica, não como comprovação de realismo semântico integral.

## 15. Avaliação de Plausibilidade Operacional

A avaliação de plausibilidade operacional foi conduzida para identificar características dos registros sintéticos que poderiam limitar sua utilização em cenários representativos de sistemas computacionais reais.

Diferentemente das verificações anteriores, essa etapa buscou examinar aspectos contextuais dos eventos de segurança.

### 15.1. Objetivo

Identificar possíveis limitações relacionadas à interpretação operacional dos eventos, considerando a disponibilidade de informações contextuais e a adequação dos valores utilizados.

A avaliação teve caráter exploratório e descritivo.

### 15.2. Implementação

Foi desenvolvido o script:

`distilabel/scripts/evaluate_dl01_realism.py`

O procedimento pode ser executado com:

```bash
.venv/bin/python ../scripts/evaluate_dl01_realism.py
```

O arquivo utilizado como entrada foi:

`results/distilabel/DL-01/generated_events_schema_all.json`

O relatório foi armazenado em:

`results/distilabel/DL-01/realism_evaluation.json`

### 15.3. Análise da categoria Login

O registro de login apresentou informações de autenticação malsucedida.

Entretanto, a avaliação identificou duas limitações:

1. O endereço IP utilizado era reservado ou não global.
2. O registro não apresentava informações adicionais sobre tentativas anteriores de autenticação.

A ausência dessas informações não torna o evento inválido, mas limita análises relacionadas a comportamentos recorrentes, ataques de força bruta ou padrões de autenticação.

### 15.4. Análise da categoria Firewall

O registro de firewall apresentou os seguintes elementos:

- Endereço IP de origem.
- Endereço IP de destino.
- Porta de destino.
- Ação de bloqueio.

A avaliação identificou que os endereços IP utilizados não eram globalmente roteáveis.

Esses endereços são adequados para determinados exemplos e ambientes de teste, mas exigem contextualização quando utilizados para representar tráfego operacional.

A presença dos campos permitiu caracterizar um evento de bloqueio, embora não demonstrasse a existência de uma política real de firewall.

### 15.5. Análise da categoria Processo

O evento de execução de processo apresentou:

- Timestamp.
- Hostname.
- Nome do processo.
- Usuário.
- Identificador do processo.

A principal limitação identificada foi a ausência de informações complementares, como:

- Caminho do executável.
- Linha de comando.
- Processo pai.

Esses atributos poderiam contribuir para análises mais detalhadas de execução de processos, especialmente em aplicações de monitoramento e detecção de comportamentos suspeitos.

### 15.6. Síntese das observações

| Categoria | Principal limitação |
|---|---|
| Login | Ausência de contexto adicional de autenticação |
| Firewall | Endereços IP não globais e contexto de rede limitado |
| Processo | Ausência de atributos adicionais de execução |

As observações representam limitações contextuais, e não necessariamente erros nos registros gerados.

### 15.7. Limitações da avaliação

A avaliação foi realizada por meio de regras automatizadas e análise descritiva dos campos.

Não foram utilizados conjuntos de dados reais como referência estatística.

Também não foram calculadas métricas validadas de fidelidade, cobertura de comportamentos operacionais ou capacidade de generalização.

Consequentemente, os resultados não permitem estabelecer uma pontuação quantitativa de realismo operacional.

### 15.8. Considerações

O experimento demonstrou que eventos estruturalmente válidos e coerentes podem apresentar limitações importantes quando interpretados sob a perspectiva operacional.

Essa distinção é relevante para o desenvolvimento de conjuntos de dados sintéticos destinados à cibersegurança.

A utilização dos registros em tarefas posteriores, especialmente no treinamento e avaliação de modelos de linguagem de pequeno porte, requer investigações adicionais sobre representatividade, diversidade e fidelidade dos dados.

## 16. Avaliação de Repetibilidade

A avaliação de repetibilidade foi realizada para verificar se diferentes execuções do experimento DL-01C, utilizando as mesmas configurações e o mesmo ambiente computacional, produziam resultados equivalentes.

### 16.1. Objetivo

Investigar a estabilidade dos registros sintéticos gerados pelo modelo Qwen3 0.6B por meio do Distilabel e do Ollama.

A avaliação considerou a quantidade de registros, a aprovação estrutural e a igualdade dos conteúdos produzidos.

### 16.2. Configuração experimental

As execuções utilizaram:

| Parâmetro | Configuração |
|---|---|
| Modelo | `qwen3:0.6b` |
| Temperature | `0` |
| Seed | `42` |
| Num predict | `300` |
| Cache do Pipeline | Desativado |
| Categorias | Login, firewall e processo |

A desativação do cache foi realizada com:

```python
pipeline.run(use_cache=False)
```

Essa configuração foi importante para evitar que o Distilabel reutilizasse diretamente resultados anteriores armazenados em cache.

### 16.3. Preservação do código experimental

O script principal foi copiado para o diretório de repetibilidade:

```bash
cp ../scripts/pipeline_dl01_schema_all.py \
  ../../results/distilabel/DL-01/reproducibility/pipeline_reference.py
```

**Função:** preservar uma referência da implementação utilizada nas execuções.

Em seguida, foi calculada sua assinatura SHA-256:

```bash
shasum -a 256 \
  ../../results/distilabel/DL-01/reproducibility/pipeline_reference.py
```

O cálculo do hash permite verificar posteriormente a integridade dos bytes do arquivo preservado.

### 16.4. Execuções independentes

O Pipeline foi executado três vezes, preservando os resultados em arquivos separados:

```text
reproducibility/
├── pipeline_reference.py
├── run_01.json
├── run_02.json
└── run_03.json
```

Em cada execução, foi utilizado o comando:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01_schema_all.py
```

Os arquivos foram armazenados separadamente para permitir a comparação posterior dos resultados.

As execuções ocorreram sequencialmente no mesmo ambiente local.

### 16.5. Verificação dos resultados

Cada execução apresentou três registros, todos aprovados na validação estrutural.

| Indicador | Execução 1 | Execução 2 | Execução 3 |
|---|---:|---:|---:|
| Registros gerados | 3 | 3 | 3 |
| Registros aprovados | 3 | 3 | 3 |
| Registros reprovados | 0 | 0 | 0 |

As saídas foram comparadas por meio de leitura dos arquivos JSON e análise dos campos `validated_event`.

A comparação indicou igualdade entre os conteúdos das três execuções.

### 16.6. Verificação por SHA-256

Também foram calculadas as assinaturas SHA-256 dos arquivos:

```bash
shasum -a 256 \
  ../../results/distilabel/DL-01/reproducibility/run_01.json \
  ../../results/distilabel/DL-01/reproducibility/run_02.json \
  ../../results/distilabel/DL-01/reproducibility/run_03.json
```

Os três arquivos apresentaram a mesma assinatura:

```text
e3ac452c15c611a773db6810ce95e5d56ef1fb605a2f09b5aa1fb46470ba87cd
```

Isso confirmou a igualdade dos bytes dos três arquivos preservados.

### 16.7. Interpretação

Os resultados demonstraram repetibilidade nas condições avaliadas.

A igualdade dos arquivos não foi atribuída à reutilização intencional do cache do Pipeline, uma vez que essa funcionalidade foi desativada nas execuções.

Entretanto, a avaliação não investigou alterações de hardware, versões de bibliotecas, sistemas operacionais ou configurações de inferência.

Portanto, os resultados não constituem uma garantia de determinismo universal do modelo ou da infraestrutura.

### 16.8. Limitações

A avaliação foi restrita a três execuções e três eventos por execução.

Não foram realizados testes extensivos com diferentes sementes, temperaturas, tamanhos de lote ou configurações computacionais.

Em trabalhos futuros, recomenda-se ampliar essas condições para investigar a estabilidade dos resultados em cenários experimentais mais abrangentes.

## 17. Problemas Encontrados e Soluções

Durante a preparação e execução dos experimentos, foram identificadas dificuldades relacionadas ao ambiente Python, às dependências, à integração com o Ollama e à execução dos Pipelines no macOS.

Esta seção reúne os principais problemas observados e os procedimentos utilizados para solucioná-los ou contorná-los.

### 17.1. Erro de importação do Distilabel

**Problema:**

```text
ModuleNotFoundError: No module named 'distilabel'
```

O erro ocorreu mesmo após a identificação do pacote nos metadados de instalação do ambiente virtual.

**Procedimento adotado:**

Foi verificada a existência do código-fonte em `src/distilabel/` e configurado explicitamente o caminho de importação:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python -c \
  "import distilabel; print(distilabel.__version__)"
```

O teste confirmou a versão 1.5.3.

Nos scripts posteriores, o `PYTHONPATH` foi mantido para assegurar que o interpretador utilizasse o código-fonte clonado.

### 17.2. Dependência Requests ausente

**Problema:**

```text
ModuleNotFoundError: No module named 'requests'
```

O erro foi identificado durante a importação dos componentes do Distilabel.

**Solução adotada:**

```bash
uv pip install --python .venv/bin/python requests
```

Após a instalação, os componentes `Pipeline`, `LoadDataFromDicts` e `TextGeneration` foram importados corretamente.

### 17.3. Executável Ollama indisponível

**Problema:**

```text
zsh: command not found: ollama
```

O comando não foi reconhecido inicialmente no Terminal.

**Procedimento adotado:**

A instalação e a disponibilidade do aplicativo Ollama foram verificadas.

Em uma nova sessão do Terminal, o comando:

```bash
ollama --version
```

passou a funcionar corretamente, identificando a versão 0.40.17.

### 17.4. Comandos interativos não reconhecidos

Durante os testes do Qwen3 0.6B, foram realizadas tentativas de utilização de comandos relacionados à desativação do raciocínio.

A interface respondeu com mensagens de comando desconhecido.

Posteriormente, foi investigada a configuração programática da API do Ollama.

Uma chamada direta utilizando `think=False` permitiu produzir uma resposta JSON no teste realizado.

### 17.5. Resposta vazia na geração JSON

Durante um teste de geração estruturada por meio da integração com Distilabel, o campo de resposta apresentou conteúdo vazio.

O teste não comprovou a geração de um objeto JSON válido naquela configuração.

**Procedimento adotado:**

Foi realizada uma chamada direta ao cliente Python do Ollama, utilizando parâmetros explícitos de formato e geração:

```python
format="json",
think=False,
stream=False,
options={
    "temperature": 0,
    "seed": 42,
    "num_predict": 350
}
```

O teste retornou um objeto JSON com os campos solicitados.

A investigação contribuiu para o desenvolvimento posterior da abordagem condicionada por esquemas.

### 17.6. Dependência Beautiful Soup ausente

Durante uma execução do Pipeline DL-01A, foi apresentada a mensagem:

```text
No module named 'bs4'
```

O pacote foi instalado com:

```bash
uv pip install --python .venv/bin/python beautifulsoup4
```

Após a instalação, o ambiente passou a disponibilizar o módulo necessário.

### 17.7. Inconsistência de tipos no DL-01B

A validação identificou que um evento de firewall apresentava o campo `destination_port` como string.

Entretanto, o esquema definido exigia um valor inteiro.

O registro foi corretamente reprovado.

Essa ocorrência motivou a investigação da geração condicionada por esquemas e da utilização de validação estrita.

### 17.8. Falha de multiprocessing no macOS

**Problema:**

Durante a execução de um script que processava as três categorias de eventos, foi identificada uma falha na inicialização de subprocessos.

O traceback apresentou uma exceção `EOFError` relacionada ao mecanismo de multiprocessing do Python.

**Causa provável:**

A execução de código principal durante a inicialização de subprocessos, associada ao método `spawn` utilizado no macOS.

**Procedimento adotado:**

A implementação foi reorganizada para proteger a execução principal:

```python
if __name__ == "__main__":
    main()
```

Nesse padrão, a função `main()` representa o ponto de entrada responsável por iniciar as operações experimentais.

A aplicação dessa proteção evita executar automaticamente a rotina principal quando o módulo é importado por subprocessos.

Após a reorganização, os três Pipelines foram executados com sucesso.

### 17.9. Avisos do Pydantic

Durante os testes, foram apresentados avisos relacionados a atributos de campos, validadores e compatibilidade entre classes.

Entre eles, foram observadas mensagens das categorias:

- `UnsupportedFieldAttributeWarning`
- `UserWarning` sobre validadores.
- Avisos relacionados à redefinição de atributos de classes.

Essas mensagens não impediram a execução final dos Pipelines.

Entretanto, indicam aspectos que devem ser examinados em futuras atualizações das bibliotecas e da implementação experimental.

### 17.10. Respostas HTTP 404 em consultas auxiliares

Durante as execuções do Distilabel, foram registradas solicitações HTTP do tipo `HEAD` para um caminho de armazenamento de datasets no Hugging Face.

As solicitações retornaram HTTP 404.

Apesar dessas mensagens, as execuções finais concluíram a geração e a validação dos registros previstos.

Os avisos foram mantidos como observações do ambiente, sem serem interpretados automaticamente como falhas dos eventos gerados.

### 17.11. Recomendações para novas execuções

Para reduzir dificuldades de reprodução, recomenda-se:

1. Confirmar a versão do Python antes de instalar as dependências.
2. Utilizar o interpretador do ambiente virtual explicitamente.
3. Verificar a disponibilidade do serviço Ollama e do modelo selecionado.
4. Executar testes de importação antes de iniciar os Pipelines.
5. Proteger a rotina principal de scripts que utilizam multiprocessing.
6. Validar os registros gerados antes de utilizá-los em análises posteriores.
7. Registrar versões, parâmetros, hashes e mensagens de erro relevantes.

Essas práticas contribuem para a rastreabilidade e a manutenção dos experimentos.

## 18. Organização dos Artefatos Gerados

Os artefatos experimentais foram organizados de maneira a separar os scripts de execução, os resultados produzidos, os arquivos auxiliares e a documentação técnica.

Essa estrutura permite identificar os componentes utilizados e preservar as evidências necessárias para auditoria e reprodução.

### 18.1. Estrutura geral do projeto

O repositório principal foi organizado da seguinte maneira:

```text
experimentos-dados-sinteticos/
├── .gitignore
├── README.md
├── evidenceforge/
├── distilabel/
│   ├── distilabel/
│   └── scripts/
├── results/
│   ├── evidenceforge/
│   └── distilabel/
│       └── DL-01/
└── reports/
    ├── EF-01_EvidenceForge.md
    ├── DL-01_Distilabel.md
    └── Tutorial_DL-01_Distilabel.md
```

O diretório `distilabel/distilabel/` contém o código-fonte original da ferramenta e não integra os arquivos destinados ao versionamento do projeto experimental.

### 18.2. Scripts experimentais

Os principais scripts foram armazenados em:

`distilabel/scripts/`

| Script | Finalidade |
|---|---|
| `pipeline_dl01.py` | Geração textual livre |
| `pipeline_dl01_structured.py` | Geração com JSON solicitado |
| `pipeline_dl01_schema.py` | Teste inicial de geração condicionada por esquema |
| `pipeline_dl01_schema_all.py` | Geração condicionada por esquema para três categorias |
| `analyze_dl01.py` | Análise inicial dos registros |
| `compare_dl01.py` | Comparação entre abordagens |
| `validate_dl01_structured.py` | Validação dos registros JSON |
| `evaluate_dl01_semantics.py` | Avaliação de consistência semântica básica |
| `evaluate_dl01_realism.py` | Avaliação exploratória de plausibilidade operacional |

Também foram desenvolvidos scripts auxiliares para investigar a integração com Ollama e os mecanismos de geração JSON.

### 18.3. Resultados experimentais

Os resultados foram armazenados em:

`results/distilabel/DL-01/`

Os principais arquivos são:

| Arquivo | Conteúdo |
|---|---|
| `generated_events_free.json` | Registros de geração textual livre |
| `generated_events_structured.json` | Registros com JSON solicitado |
| `generated_events_schema_all.json` | Registros gerados com esquemas |
| `analysis_dl01.json` | Análise inicial |
| `validation_structured.json` | Resultado da validação estrutural do DL-01B |
| `comparison_dl01.json` | Comparação das abordagens |
| `semantic_evaluation.json` | Avaliação de consistência básica |
| `realism_evaluation.json` | Avaliação exploratória de plausibilidade |

Outros arquivos de testes e execução foram preservados para fins de rastreabilidade.

### 18.4. Artefatos de repetibilidade

O diretório:

`results/distilabel/DL-01/reproducibility/`

contém:

```text
reproducibility/
├── pipeline_reference.py
├── run_01.json
├── run_02.json
└── run_03.json
```

Os arquivos `run_01.json`, `run_02.json` e `run_03.json` preservam os resultados utilizados na avaliação de repetibilidade.

O arquivo `pipeline_reference.py` registra uma cópia do código experimental utilizado.

### 18.5. Relatórios técnicos

Foram elaborados dois documentos com finalidades complementares.

**Relatório experimental:**

`reports/DL-01_Distilabel.md`

Apresenta a metodologia, os resultados, as avaliações, as limitações e as conclusões do estudo exploratório.

**Tutorial técnico:**

`reports/Tutorial_DL-01_Distilabel.md`

Documenta os procedimentos de preparação, configuração, implementação, execução e verificação dos experimentos.

### 18.6. Controle de versão

O projeto principal foi preparado para versionamento com Git.

O arquivo `.gitignore` foi configurado para excluir ambientes virtuais, arquivos temporários, o repositório original do Distilabel e cópias intermediárias de scripts.

Os scripts experimentais, os relatórios e os resultados selecionados permanecem disponíveis para inclusão no repositório principal.

Antes da publicação, recomenda-se verificar possíveis credenciais, informações sensíveis, arquivos desnecessários e consistência entre a documentação e os artefatos produzidos.

### 18.7. Integridade dos artefatos

Foram utilizadas assinaturas SHA-256 para verificar a integridade de determinados arquivos gerados.

O comando geral utilizado foi:
```bash
shasum -a 256 caminho
```

A assinatura permite identificar alterações nos bytes de um arquivo.

A igualdade entre assinaturas é útil na conferência de integridade, mas não substitui avaliações sobre a correção ou a qualidade dos conteúdos armazenados.

## 19. Procedimento Resumido de Reprodução

Esta seção consolida os procedimentos essenciais para reproduzir a geração de eventos sintéticos do experimento DL-01C.

Os procedimentos pressupõem um ambiente macOS com Git, Python 3.12, `uv` e Ollama disponíveis.

### 19.1. Obter o código-fonte

Acessar o diretório principal:

```bash
cd ~/Documents/experimentos-dados-sinteticos
```

Caso o repositório oficial do Distilabel ainda não esteja disponível, obtê-lo:

```bash
mkdir -p distilabel
cd distilabel
git clone https://github.com/argilla-io/distilabel.git
cd distilabel
```

Para reconstruir o ambiente com a revisão utilizada no experimento:

```bash
git checkout 313fac85b1a2472dd88db1a31c2b754599f46476
```

Essa operação posiciona a cópia local na revisão identificada durante a preparação experimental.

### 19.2. Preparar o ambiente Python

Criar o ambiente virtual, caso ainda não exista:

```bash
uv venv --python 3.12 .venv
```

Instalar o Distilabel a partir do código-fonte:

```bash
uv pip install --python .venv/bin/python -e .
```

Instalar as dependências complementares utilizadas:

```bash
uv pip install --python .venv/bin/python \
  requests ollama beautifulsoup4
```

Para uma reprodução rigorosa, devem ser utilizadas as versões registradas no ambiente experimental original. Os comandos apresentados não fixam todas as dependências transitivas.

### 19.3. Preparar o Ollama

Verificar a instalação:

```bash
ollama --version
```

Confirmar a disponibilidade do modelo:

```bash
ollama list
```

Caso necessário, obtê-lo:

```bash
ollama pull qwen3:0.6b
```

Verificar a API:

```bash
curl http://localhost:11434/api/tags
```

O serviço deve estar acessível antes da execução do Pipeline.

### 19.4. Verificar a integração

Na raiz do código-fonte clonado, executar:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python - <<'PY'
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromDicts
from distilabel.steps.tasks import TextGeneration
from distilabel.models.llms import OllamaLLM

print("Componentes importados com sucesso.")
PY
```

A execução bem-sucedida confirma a disponibilidade dos componentes necessários, mas não substitui um teste de geração.

### 19.5. Executar o experimento DL-01C

O script principal encontra-se em:

`distilabel/scripts/pipeline_dl01_schema_all.py`

A execução é realizada com:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python \
  ../scripts/pipeline_dl01_schema_all.py
```

O Pipeline processa três categorias de eventos:

- Login malsucedido.
- Bloqueio de conexão por firewall.
- Execução de processo.

Na execução experimental documentada, foram obtidos três registros aprovados na validação estrutural.

O arquivo principal produzido é:

`results/distilabel/DL-01/generated_events_schema_all.json`

### 19.6. Realizar as avaliações

A partir da raiz do código-fonte do Distilabel, executar a avaliação de consistência básica:

```bash
.venv/bin/python ../scripts/evaluate_dl01_semantics.py
```

Em seguida, executar a avaliação exploratória de plausibilidade operacional:

```bash
.venv/bin/python ../scripts/evaluate_dl01_realism.py
```

Os relatórios são armazenados no diretório de resultados do experimento.

### 19.7. Consultar os registros gerados

Para visualizar o arquivo JSON:

```bash
.venv/bin/python -m json.tool \
  ../../results/distilabel/DL-01/generated_events_schema_all.json
```

O comando permite verificar a estrutura sintática do arquivo armazenado.

### 19.8. Verificar a integridade

Calcular a assinatura SHA-256:

```bash
shasum -a 256 \
  ../../results/distilabel/DL-01/generated_events_schema_all.json
```

A assinatura pode ser comparada com aquela registrada durante o experimento original.

Uma assinatura diferente indica alteração nos bytes do arquivo, mas não demonstra, isoladamente, a existência de erros nos eventos gerados.

### 19.9. Cuidados durante a reprodução

A reprodução deve considerar:

1. Disponibilidade do mesmo modelo e das versões de software pertinentes.
2. Configuração equivalente dos parâmetros de geração.
3. Inicialização correta do Ollama.
4. Disponibilidade das dependências Python.
5. Proteção da rotina principal contra problemas de multiprocessing.
6. Desativação do cache quando forem necessárias novas gerações.
7. Preservação dos resultados e dos metadados de cada execução.

A obtenção de resultados idênticos não é garantida em ambientes diferentes.

### 19.10. Resultado esperado

Uma execução bem-sucedida deve produzir registros para as três categorias e apresentar os resultados das validações implementadas.

O experimento original obteve três registros estruturalmente aprovados.

Esse resultado serve como referência para a reprodução, não como garantia de que todas as execuções futuras apresentarão o mesmo comportamento.

## 20. Considerações Finais

Este tutorial apresentou os procedimentos utilizados na preparação, implementação, execução e avaliação exploratória de técnicas de geração de dados sintéticos para cibersegurança utilizando Distilabel, Ollama e o modelo Qwen3 0.6B.

O trabalho foi organizado em três abordagens experimentais: geração textual livre (DL-01A), geração com JSON solicitado (DL-01B) e geração condicionada por esquemas (DL-01C).

### 20.1. Principais resultados

No DL-01A, foram geradas três respostas textuais, sem obtenção de objetos JSON diretamente utilizáveis.

No DL-01B, foram obtidos três objetos JSON, dos quais dois atenderam às regras de validação aplicadas.

No DL-01C, foram gerados três eventos, todos aprovados na validação estrutural e nas verificações determinísticas de consistência básica.

A avaliação exploratória também identificou limitações relacionadas ao contexto operacional dos registros.

### 20.2. Contribuições técnicas

O estudo permitiu:

- Configurar o ambiente experimental do Distilabel.
- Integrar a ferramenta a um modelo de linguagem executado pelo Ollama.
- Implementar três estratégias de geração sintética.
- Aplicar esquemas específicos às categorias de eventos.
- Desenvolver procedimentos automatizados de validação.
- Investigar a repetibilidade dos resultados.
- Preservar os scripts, registros e relatórios técnicos.

A documentação dos erros encontrados e das soluções adotadas também contribui para facilitar novas reproduções.

### 20.3. Limitações gerais

O experimento possui limitações importantes.

A amostra foi composta por apenas três registros em cada abordagem principal.

As configurações de geração apresentaram diferenças, impedindo uma comparação experimental completamente controlada.

As avaliações concentraram-se na conformidade estrutural, na coerência básica e em observações exploratórias de plausibilidade operacional.

Não foram realizadas avaliações abrangentes de fidelidade estatística, distribuição de eventos, diversidade semântica ou utilidade dos dados para treinamento de modelos.

### 20.4. Possibilidades de continuidade

Como continuidade, recomenda-se:

1. Ampliar o número de registros gerados por categoria.
2. Utilizar conjuntos de dados reais como referência comparativa.
3. Definir métricas quantitativas de qualidade e diversidade.
4. Investigar diferentes parâmetros e modelos de linguagem.
5. Avaliar a robustez das estratégias de geração.
6. Examinar a utilidade dos dados sintéticos em tarefas de cibersegurança executadas por SLMs.
7. Realizar novas avaliações de repetibilidade e reprodutibilidade em ambientes distintos.

A ampliação dos experimentos deverá preservar o controle das configurações e a rastreabilidade dos resultados.

### 20.5. Encerramento

Os resultados demonstraram a viabilidade técnica da utilização do Distilabel com o Ollama para gerar registros sintéticos de eventos de segurança computacional.

A geração condicionada por esquemas apresentou resultados estruturalmente satisfatórios na amostra analisada.

Entretanto, a validade estrutural não deve ser confundida com realismo operacional, fidelidade estatística ou adequação para aplicações de aprendizado de máquina.

O conjunto de scripts, resultados e documentos produzidos estabelece uma base experimental inicial para futuras investigações sobre geração e avaliação de dados sintéticos aplicados à cibersegurança.