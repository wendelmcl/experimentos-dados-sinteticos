# Tutorial Técnico — Reprodução do Experimento EF-01 com EvidenceForge

**Projeto:** Experimentos de Geração de Dados Sintéticos para Cibersegurança  
**Experimento:** EF-01  
**Ferramenta:** EvidenceForge 2.1.2 (Cisco Talos)  
**Cenário:** `branch-office-example`  
**Ambiente registrado:** macOS, Apple M1, 8 GB RAM, Python 3.12.16, `uv` 0.13.9  
**Referência principal:** [`EF-01_EvidenceForge.md`](EF-01_EvidenceForge.md)

> **Rastreabilidade.** Os comandos de `git clone`, `uv`, `eforge validate`, `eforge generate`, `eforge eval` e execução de `analyze_ef01.py` constam do relatório EF-01. Os demais comandos deste tutorial são **comandos auxiliares propostos para reprodução e inspeção**, e não devem ser interpretados como transcrições literais da execução original. O ZIP consultado não contém o checkout original do EvidenceForge, o arquivo YAML resolvido nem os 40 arquivos brutos de evidência; portanto, não é possível auditar integralmente as saídas originais apenas com esse material.

---

## 1. Apresentação

Este tutorial orienta a preparação, execução, verificação e documentação do experimento EF-01, desenvolvido com o EvidenceForge para gerar evidências sintéticas de cibersegurança. O cenário oficial `branch-office-example` simula atividades e observações em um ambiente de filial, com diferentes fontes de registros.

O objetivo experimental descrito no relatório é reproduzir o cenário oficial e avaliar **qualidade, diversidade, consistência e reprodutibilidade**. O tutorial explica a função de cada comando, apresenta resultados observados e separa procedimentos comprovados por arquivos do repositório daqueles sugeridos para uma nova execução.

## 2. Organização do tutorial

1. Apresentação.
2. Organização do tutorial.
3. Estrutura do projeto e requisitos.
4. Obtenção do código-fonte e revisão de referência.
5. Preparação do Python e do `uv`.
6. Instalação das dependências.
7. Reconhecimento do cenário e dos comandos.
8. Validação do YAML.
9. Geração de evidências sintéticas.
10. Avaliação de qualidade com `eforge eval`.
11. Inspeção dos artefatos.
12. Análise independente de registros eCAR.
13. Verificação de diversidade.
14. Verificação de consistência e integridade temporal.
15. Reprodutibilidade por segunda execução.
16. Comparação do Ground Truth e hashes.
17. Problemas identificados e soluções.
18. Preservação de resultados e metadados.
19. Procedimento resumido de reprodução.
20. Limitações e considerações finais.

## 3. Estrutura do projeto e requisitos

O repositório do estudo está organizado, nos caminhos relevantes, da seguinte forma:

```text
experimentos-dados-sinteticos/
├── evidenceforge/
│   ├── scripts/
│   │   └── analyze_ef01.py
│   └── EvidenceForge/            # clone oficial, não incluído no ZIP
│       ├── scenarios/
│       └── output-ef01/          # gerado localmente, não incluído no ZIP
├── results/
│   └── evidenceforge/
│       └── EF-01/
│           ├── COLLECTION_PROFILE.json
│           ├── GENERATION_MANIFEST.json
│           ├── GROUND_TRUTH.json
│           ├── OBSERVATION_MANIFEST.json
│           ├── analysis_ef01.json
│           └── experiment-info.txt
└── reports/
    ├── EF-01_EvidenceForge.md
    └── Tutorial_EF-01_EvidenceForge.md
```

**Requisitos do ambiente documentado:** macOS, Python 3.12.16, `uv` 0.13.9, EvidenceForge 2.1.2 e Git. A arquitetura de hardware e a versão do gerenciador não são pré-requisitos universais, mas registrar diferenças ajuda a interpretar eventuais divergências de resultado.

**Comando auxiliar — verificar ferramentas instaladas:**

```bash
python3 --version
git --version
uv --version
```

**Função:** imprimir as versões disponíveis antes da preparação. Se `uv` não estiver instalado, utilize o procedimento de instalação indicado na [documentação oficial do uv](https://docs.astral.sh/uv/getting-started/installation/); o arquivo do experimento não registra qual método de instalação foi adotado originalmente.

## 4. Obtenção do código-fonte e revisão de referência

A partir da raiz do estudo:

```bash
cd ~/Documents/experimentos-dados-sinteticos
mkdir -p evidenceforge
cd evidenceforge
```

**Função:** entrar na pasta reservada ao experimento. O caminho `~/Documents/...` reflete a organização documentada; ajuste caso tenha clonado o projeto em outro local.

**Comando registrado — obter o repositório oficial:**

```bash
git clone https://github.com/Cisco-Talos/EvidenceForge.git
cd EvidenceForge
```

**Função:** baixar o código-fonte original e entrar no diretório do projeto upstream. Não se deve confundir o repositório experimental com o repositório original da ferramenta.

**Comandos auxiliares — conferir revisão e situação do Git:**

```bash
git rev-parse HEAD
git status --short
```

**Função:** identificar o commit efetivamente selecionado e verificar se existem modificações locais.

**Atenção à revisão do experimento.** O arquivo `experiment-info.txt` registra o identificador de 40 caracteres:

```text
79fcfcdf3726168dacfede5a27aab2aa7a2f3d69
```

Entretanto, a seção 12.6 do relatório `EF-01_EvidenceForge.md` contém uma cadeia diferente, com **41 caracteres** (`79fcfcdf3726168dacfdede5a27aab2aa7a2f3d69`). Trata-se de uma inconsistência documental. **Não foi possível confirmar qual revisão está correta sem consultar o checkout original.**

**Comando auxiliar — tentar selecionar a revisão registrada no `experiment-info.txt`:**

```bash
git checkout 79fcfcdf3726168dacfede5a27aab2aa7a2f3d69
git rev-parse HEAD
```

**Função:** tentar reproduzir a revisão informada pelo registro ambiental. **Execute somente após confirmar que o hash existe no repositório**; caso o `checkout` falhe, interrompa a reprodução e confirme o commit correto. Não substitua silenciosamente por `main` ou por uma revisão atualizada.

## 5. Preparação do Python e do `uv`

**Comandos registrados:**

```bash
uv python install 3.12
uv sync --python 3.12
```

**Função do primeiro comando:** disponibilizar uma instalação Python da família 3.12 gerenciada pelo `uv`.  
**Função do segundo:** sincronizar o ambiente virtual e as dependências conforme as definições do projeto do EvidenceForge, usando Python 3.12.

**Comandos auxiliares — verificar o interpretador do ambiente:**

```bash
uv run python --version
uv run python -c 'import sys; print(sys.executable)'
```

**Função:** confirmar a versão e o executável utilizados pelos comandos executados via `uv`.

> O comando `uv python install 3.12` não garante, sozinho, que instalações futuras usem exatamente o patch **3.12.16**. A versão deve ser verificada e registrada na nova execução.

## 6. Instalação e verificação das dependências

O procedimento principal de instalação registrado no experimento é `uv sync --python 3.12`, executado na **raiz do clone oficial**. Não há no ZIP um `requirements.txt` adicional do EF-01 que deva ser instalado separadamente.

**Comandos auxiliares — examinar o projeto e as dependências instaladas:**

```bash
ls -lh pyproject.toml
uv pip list
```

**Função:** confirmar a presença da configuração Python do upstream e listar os pacotes do ambiente do projeto. A listagem pode variar conforme o checkout e o arquivo de lock utilizado.

O relatório documenta EvidenceForge 2.1.2, enquanto `GENERATION_MANIFEST.json` também indica `evidenceforge_version: 2.1.2`.

## 7. Reconhecimento do cenário oficial

O arquivo utilizado é:

```text
scenarios/branch-office-example/scenario.yaml
```

**Comandos auxiliares — verificar que o cenário existe e examinar seu início:**

```bash
ls -lh scenarios/branch-office-example/scenario.yaml
sed -n '1,100p' scenarios/branch-office-example/scenario.yaml
```

**Função:** confirmar a localização e inspecionar o conteúdo YAML antes de executar a geração. Não altere o cenário oficial se a intenção for comparar os resultados ao EF-01.

Os metadados arquivados mostram `generation_seed: 42`, janela de coleta de **2024-05-14T12:00:00Z** a **2024-05-14T18:00:00Z** e perfil de observação `complete`. Esses valores foram lidos nos manifests preservados; a configuração YAML integral não está disponível no ZIP fornecido.

## 8. Validação do cenário YAML

**Comando registrado:**

```bash
PYTHONPATH="$PWD/src" uv run eforge validate scenarios/branch-office-example/scenario.yaml
```

**Função:** executar a validação do cenário com a CLI `eforge`. A variável `PYTHONPATH` faz o Python considerar o diretório `src` do repositório atual na resolução dos módulos.

**Por que usar `PYTHONPATH`?** O relatório registra um problema de resolução do pacote instalado em modo editável; definir `src` explicitamente permitiu executar a CLI. Essa solução é específica do ambiente observado e não deve ser tratada como obrigatória em toda instalação.

**Resultado esperado:** conclusão da validação sem erro impeditivo. O ZIP não preserva o texto exato do terminal dessa etapa.

## 9. Geração de evidências sintéticas

**Comando registrado:**

```bash
PYTHONPATH="$PWD/src" uv run eforge generate scenarios/branch-office-example/scenario.yaml -o ./output-ef01
```

**Função:** gerar as evidências sintéticas do cenário e gravá-las em `output-ef01` dentro da raiz do clone oficial.

**Cuidado:** o relatório informa que a pasta de saída **deve estar ausente antes da geração**, para evitar sobreposição de dados. Não remova uma saída anterior sem preservá-la.

**Comando auxiliar — verificar previamente a pasta:**

```bash
if [ -e output-ef01 ]; then
  echo 'A pasta output-ef01 já existe; preserve-a antes de gerar novamente.'
else
  echo 'Pasta output-ef01 ainda não existe; a geração pode ser iniciada.'
fi
```

**Função:** evitar sobrescrever artefatos já produzidos. Esse comando apenas inspeciona: não apaga nenhum arquivo.

**Resultados registrados:** **42.736 registros**, **18 fontes de evidência** e **40 arquivos de evidência**, conforme o relatório EF-01. Não confunda os 40 arquivos de evidência com a quantidade de arquivos de metadados e manifestos.

## 10. Avaliação da qualidade pelo EvidenceForge

**Comando registrado:**

```bash
PYTHONPATH="$PWD/src" uv run eforge eval ./output-ef01
```

**Função:** executar a avaliação de qualidade interna da ferramenta sobre a saída gerada.

**Resultado registrado:** aprovação `PASS` e qualidade geral de **97/100**.

| Critério | Pontuação registrada |
|---|---:|
| Parseability | 100/100 |
| Plausibility | 93/100 |
| Causality | 100/100 |
| Timing | 95/100 |

Essas pontuações são resultados internos da ferramenta e não demonstram, isoladamente, fidelidade estatística a redes reais ou adequação a aplicações de aprendizagem de máquina.

## 11. Inspeção dos artefatos produzidos

**Comandos auxiliares — listar a saída:**

```bash
find output-ef01 -maxdepth 2 -type f | sort | head -80
find output-ef01/data -type f | wc -l
```

**Função:** visualizar alguns caminhos criados e contar arquivos sob `data`. A segunda contagem **não** deve ser automaticamente interpretada como número de arquivos de evidência, pois a organização do diretório pode incluir outros arquivos.

O ZIP do estudo conserva, em `results/evidenceforge/EF-01/`, os seguintes arquivos:

| Artefato | Finalidade |
|---|---|
| `GENERATION_MANIFEST.json` | Identificação da geração, versão, seed, formatos e hashes de artefatos |
| `COLLECTION_PROFILE.json` | Perfil de coleta e estimativas do cenário |
| `OBSERVATION_MANIFEST.json` | Manifesto da observabilidade e fontes da simulação |
| `GROUND_TRUTH.json` | Referência estruturada dos eventos e da narrativa simulada |
| `analysis_ef01.json` | Resultado da análise independente de eCAR |
| `experiment-info.txt` | Resumo do ambiente e resultado do EF-01 |

**Comando auxiliar — visualizar JSON formatado:**

```bash
python3 -m json.tool output-ef01/GENERATION_MANIFEST.json | head -80
```

**Função:** conferir a sintaxe JSON e inspecionar o cabeçalho do manifesto, caso o arquivo esteja nessa posição na saída. A localização deve ser confirmada com `find` se a revisão produzir outra organização.

## 12. Análise independente dos registros eCAR

O repositório experimental inclui o script:

```text
evidenceforge/scripts/analyze_ef01.py
```

**Comando registrado**, executado na raiz do **clone oficial** (`evidenceforge/EvidenceForge/`):

```bash
uv run python ../../evidenceforge/scripts/analyze_ef01.py
```

**Função:** analisar os arquivos `ecar.json` gerados e produzir `results/evidenceforge/EF-01/analysis_ef01.json` no repositório do estudo.

O script determina o caminho dos dados relativamente à localização do próprio arquivo:

```python
BASE = Path(__file__).resolve().parents[2]
DATA_DIR = BASE / "evidenceforge/EvidenceForge/output-ef01/data"
RESULT_DIR = BASE / "results/evidenceforge/EF-01"
```

Por isso, a disposição dos diretórios é importante. Se o clone oficial ou o diretório de saída estiverem em outro lugar, ajuste as referências **de maneira explícita e documentada** antes de executar a análise.

O script percorre arquivos chamados `ecar.json` em subdiretórios, lê registros JSON por linha e calcula contagens por sistema, objetos, ações e pares objeto/ação. Além disso, verifica campos ausentes, identificadores repetidos, timestamps e limites temporais.

**Comando auxiliar — conferir o relatório produzido:**

```bash
python3 -m json.tool ../../results/evidenceforge/EF-01/analysis_ef01.json
```

**Função:** validar a sintaxe e apresentar o resultado da análise, usando o caminho relativo à raiz do clone oficial.

## 13. Verificação de diversidade dos dados eCAR

A análise independente preservada no repositório identificou **12.145 registros eCAR** distribuídos por **9 sistemas**.

| Dimensão observada | Quantidade |
|---|---:|
| Objetos distintos | 7 |
| Ações distintas | 11 |
| Combinações objeto/ação | 12 |
| Arquivos `ecar.json` | 9 |

As categorias de objeto incluem `FLOW`, `PROCESS`, `MODULE`, `USER_SESSION`, `REGISTRY`, `FILE` e `THREAD`. `FLOW` foi a mais frequente (7.752 registros); a ação `CONNECT` também ocorreu 7.752 vezes. Isso evidencia variedade de classes, mas distribuição desbalanceada.

**Comando auxiliar — ler essas contagens diretamente do resultado salvo, a partir da raiz do estudo:**

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path('results/evidenceforge/EF-01/analysis_ef01.json')
d = json.loads(p.read_text(encoding='utf-8'))
print('Registros eCAR:', d['registros_validos'])
print('Sistemas:', len(d['registros_por_sistema']))
print('Objetos:', len(d['objetos']))
print('Ações:', len(d['acoes']))
print('Pares objeto/ação:', len(d['combinacoes_objeto_acao']))
PY
```

**Função:** recomputar o resumo de diversidade a partir do JSON arquivado, sem executar novamente o EvidenceForge.

## 14. Verificação de consistência e integridade temporal

O script `analyze_ef01.py` verifica as presenças de `timestamp_ms`, `id`, `hostname`, `object` e `action` e testa a interpretação de cada linha como objeto JSON.

Também conta IDs duplicados, timestamps inválidos, inversões cronológicas dentro de cada arquivo e eventos fora da janela UTC de 14 de maio de 2024, das 12h às 18h.

**Resultados preservados:**

| Indicador | Valor |
|---|---:|
| Registros JSON inválidos | 0 |
| Campos obrigatórios ausentes | 0 |
| Registros sem ID | 0 |
| IDs duplicados | 0 |
| Timestamps inválidos | 0 |
| Inversões temporais | 0 |
| Registros fora da janela | 0 |

O primeiro evento analisado ocorreu às **12:00:02.717 UTC** e o último às **17:59:56.478 UTC**.

**Comando auxiliar — examinar os indicadores, a partir da raiz do estudo:**

```bash
python3 - <<'PY'
import json
from pathlib import Path
d = json.loads(Path('results/evidenceforge/EF-01/analysis_ef01.json').read_text(encoding='utf-8'))
for chave in ('registros_invalidos', 'campos_ausentes', 'ids_duplicados',
              'timestamps_invalidos', 'inversoes_temporais', 'registros_fora_janela',
              'primeiro_evento_utc', 'ultimo_evento_utc'):
    print(f'{chave}: {d[chave]}')
PY
```

**Limite metodológico:** os testes são verificações determinísticas de sintaxe, campos e cronologia. Eles não verificam toda a semântica operacional dos eventos, nem substituem uma avaliação contra dados reais.

## 15. Reprodutibilidade por segunda execução

O relatório EF-01 informa que uma segunda geração produziu novamente **42.736 registros, 18 fontes, 40 arquivos de evidência e avaliação 97/100**, com nenhuma diferença detectada entre os 40 arquivos de evidência comparados. Os comandos exatos da segunda rodada não constam integralmente dos arquivos preservados.

**Procedimento auxiliar proposto para uma nova reprodução**, a partir do clone oficial e **sem sobrescrever a primeira saída**:

```bash
PYTHONPATH="$PWD/src" uv run eforge generate \
  scenarios/branch-office-example/scenario.yaml \
  -o ./output-ef01-repeticao

PYTHONPATH="$PWD/src" uv run eforge eval ./output-ef01-repeticao
```

**Função:** gerar um segundo conjunto de evidências e avaliá-lo de maneira independente. O nome `output-ef01-repeticao` é uma convenção **proposta neste tutorial**, não um caminho confirmado da execução histórica.

**Comandos auxiliares — comparar apenas o conteúdo dos diretórios de evidência:**

```bash
diff -rq output-ef01/data output-ef01-repeticao/data
```

**Função:** identificar arquivos ausentes e diferenças byte a byte sob `data`. Ausência de saída no `diff` com código de retorno 0 indica igualdade dos conteúdos e estrutura encontrados nesses diretórios. Arquivos de manifesto podem incluir metadados variáveis entre execuções e devem ser tratados separadamente.

```bash
echo $?
```

**Função:** consultar imediatamente o código de saída do último comando (`0` normalmente indica que não houve diferenças no `diff`). Não execute outros comandos entre o `diff` e o `echo` se quiser preservar esse diagnóstico.

## 16. Comparação do Ground Truth e hashes SHA-256

O relatório informa que os dois arquivos `GROUND_TRUTH.json` comparados apresentaram o mesmo SHA-256:

```text
c23c780c6daa9eda632759b876a8e1b7b9f4d28316deb892bbcb256ace099f6a
```

**Comandos auxiliares — calcular os hashes das duas saídas (a partir do clone oficial):**

```bash
shasum -a 256 output-ef01/GROUND_TRUTH.json
shasum -a 256 output-ef01-repeticao/GROUND_TRUTH.json
```

**Função:** calcular as assinaturas SHA-256 dos arquivos e permitir comparação dos bytes. A localização indicada corresponde ao formato de saída descrito no relatório; confirme-a previamente com `find` se necessário.

**Comando auxiliar — comparação direta:**

```bash
cmp -s output-ef01/GROUND_TRUTH.json output-ef01-repeticao/GROUND_TRUTH.json
echo $?
```

**Função:** retornar `0` se os arquivos forem idênticos byte a byte. Executar `echo $?` imediatamente após `cmp` é necessário para consultar o status correto.

**Importante:** igualdade de hashes comprova igualdade byte a byte dos artefatos comparados, não igualdade de validade científica ou realismo dos eventos. A verificação histórica consta do relatório, mas o ZIP não inclui os arquivos de ambas as execuções para auditoria independente.

## 17. Problemas identificados e soluções

### 17.1. Resolução do pacote em modo editável

**Problema registrado:** falha de resolução do pacote Python no ambiente de instalação editável.

**Solução registrada:** prefixar as operações da CLI com:

```bash
PYTHONPATH="$PWD/src"
```

**Função:** incluir o código localizado em `src` no caminho de importação Python durante a execução. No procedimento efetivo, esse prefixo é usado junto a `uv run eforge ...`.

### 17.2. Pasta de saída preexistente

**Risco documentado:** executar geração em diretório que já contém resultados.

**Prevenção proposta:** usar saída vazia e separada para cada tentativa. Verifique a existência da pasta antes da execução e preserve as rodadas comparadas.

### 17.3. Diferença de revisão e ambiente

**Risco:** usar uma revisão, versão Python ou dependências diferentes, reduzindo a comparabilidade.

**Prevenção proposta:** registrar `git rev-parse HEAD`, `uv run python --version`, `uv --version` e manifests gerados. Resolver antes a divergência de hash indicada na Seção 4.

### 17.4. Script eCAR não encontra os dados

**Causa provável segundo o código preservado:** o script usa um caminho fixo baseado na raiz do repositório experimental (`evidenceforge/EvidenceForge/output-ef01/data`).

**Verificação auxiliar:**

```bash
find output-ef01/data -name ecar.json -type f
```

**Função:** localizar os arquivos que o script tentará analisar. Se os arquivos estiverem ausentes, verifique o cenário, a pasta de saída e a estrutura utilizada, em vez de alterar os resultados esperados.

## 18. Preservação de resultados e metadados

O experimento manteve um conjunto compacto de resultados verificáveis em `results/evidenceforge/EF-01/`, enquanto os arquivos brutos de evidência permaneceram na saída local da ferramenta.

**Comandos auxiliares propostos — copiar artefatos de referência após a execução (a partir da raiz do estudo):**

```bash
mkdir -p results/evidenceforge/EF-01
cp evidenceforge/EvidenceForge/output-ef01/GENERATION_MANIFEST.json \
   results/evidenceforge/EF-01/
cp evidenceforge/EvidenceForge/output-ef01/GROUND_TRUTH.json \
   results/evidenceforge/EF-01/
```

**Função:** preservar manifestos e Ground Truth em uma área controlada do estudo. **Não execute essas cópias sobre arquivos já arquivados sem criar uma versão ou backup**, porque isso pode alterar os artefatos históricos.

**Comandos auxiliares — validar JSONs preservados:**

```bash
python3 -m json.tool results/evidenceforge/EF-01/GENERATION_MANIFEST.json > /dev/null
python3 -m json.tool results/evidenceforge/EF-01/analysis_ef01.json > /dev/null
```

**Função:** testar a sintaxe JSON dos arquivos sem despejar todo o conteúdo no Terminal. Aprovação sintática não equivale a validação completa de esquema.

**Comando auxiliar — identificar modificações antes de versionar:**

```bash
git status --short
```

**Função:** verificar arquivos adicionados, alterados e não rastreados na raiz do repositório experimental, evitando incluir dados sensíveis, caches, backups ou grandes saídas brutas inadvertidamente.

## 19. Procedimento resumido de reprodução

Os passos abaixo condensam os comandos centrais **registrados** no relatório, assumindo que o projeto experimental já existe na pasta `~/Documents/experimentos-dados-sinteticos/` e que Git e `uv` estão disponíveis.

```bash
# Acessar a pasta do experimento
cd ~/Documents/experimentos-dados-sinteticos/evidenceforge

# Obter o código-fonte oficial, se ainda não existir
git clone https://github.com/Cisco-Talos/EvidenceForge.git
cd EvidenceForge

# Confirmar o commit correto antes da reprodução
# (há divergência documental; ver Seção 4)
git rev-parse HEAD

# Preparar Python e dependências
uv python install 3.12
uv sync --python 3.12

# Validar o cenário
PYTHONPATH="$PWD/src" uv run eforge validate scenarios/branch-office-example/scenario.yaml

# Gerar dados em uma pasta ainda inexistente
PYTHONPATH="$PWD/src" uv run eforge generate scenarios/branch-office-example/scenario.yaml -o ./output-ef01

# Avaliar os dados gerados
PYTHONPATH="$PWD/src" uv run eforge eval ./output-ef01

# Analisar independentemente os registros eCAR
uv run python ../../evidenceforge/scripts/analyze_ef01.py
```

> **Pré-condições:** o clone de EvidenceForge não deve existir antes do `git clone`, a saída `output-ef01` não deve existir antes da geração, a revisão exata deve ter sido confirmada e a versão do ambiente precisa ser registrada. Os comandos foram extraídos da documentação preservada; não foram executados novamente durante a elaboração deste tutorial.

Para repetir a geração, utilize a saída separada indicada na Seção 15, compare as evidências e registre os hashes conforme a Seção 16.

## 20. Limitações e considerações finais

No EF-01, o EvidenceForge gerou **42.736 registros**, organizados em **18 fontes** e **40 arquivos de evidências**, com qualidade geral **97/100** e resultado **PASS**. A análise independente de **12.145 registros eCAR** não identificou erros estruturais ou temporais segundo os critérios automatizados empregados. O relatório informa ainda que a segunda execução produziu evidências e Ground Truth idênticos nas comparações realizadas.

Esses resultados dão suporte à **reprodução controlada de um cenário oficial** e à consistência básica dos artefatos analisados. Não constituem demonstração de equivalência com telemetria real, de validade estatística geral ou de utilidade para treinamento de modelos de linguagem pequenos (SLMs).

Para uma nova reprodução com rigor de rastreabilidade, recomenda-se: (i) resolver a divergência no identificador de commit; (ii) fixar e registrar versões e dependências; (iii) conservar os arquivos brutos e os manifests de cada execução; e (iv) repetir as análises e comparações mantendo as saídas separadas.

### Referências

- Cisco Talos. **EvidenceForge**. Repositório oficial: https://github.com/Cisco-Talos/EvidenceForge
- Relatório técnico EF-01: [`reports/EF-01_EvidenceForge.md`](EF-01_EvidenceForge.md)
- Script de análise eCAR: [`evidenceforge/scripts/analyze_ef01.py`](../evidenceforge/scripts/analyze_ef01.py)
- Resultados arquivados: [`results/evidenceforge/EF-01/`](../results/evidenceforge/EF-01/)

---

**Nota de elaboração:** este tutorial foi produzido a partir dos arquivos disponibilizados no ZIP `experimentos-dados-sinteticos-main.zip`. Todos os resultados numéricos apresentados foram extraídos da documentação e dos JSONs nele contidos. Os procedimentos auxiliares foram expressamente identificados como propostas de inspeção e reprodução, sem atribuir sua execução ao experimento original.
